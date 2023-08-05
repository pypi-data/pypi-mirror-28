# -------------------------------------------------------------------------------
# Copyright IBM Corp. 2017
# 
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------------
import ast
import io
import os
import nbformat
import astunparse
from traitlets.config.configurable import SingletonConfigurable
from traitlets import Unicode, default
from tornado import gen
from tornado.concurrent import Future
from tornado.log import app_log
from tornado.util import import_object
from .pixieGatewayApp import PixieGatewayApp
from .managedClient import ManagedClientPool
from IPython.core.getipython import get_ipython

def ast_parse(code):
    try:
        return ast.parse(code)
    except SyntaxError:
        #transform the code first to handle notebook syntactic sugar like magic and system
        return ast.parse(
            get_ipython().input_transformer_manager.transform_cell(code)
        )

class NotebookFileLoader():
    def load(self, path):
        return io.open(path)

class NotebookMgr(SingletonConfigurable):
    notebook_dir = Unicode(None, config=True, allow_none=True,
                           help="""Path containing the notebook with Runnable PixieApp""")

    notebook_loader = Unicode(None, config=True, help="Notebook content loader")

    @default('notebook_dir')
    def notebook_dir_default(self):
        pixiedust_home = os.environ.get("PIXIEDUST_HOME", os.path.join(os.path.expanduser('~'), "pixiedust"))
        return self._ensure_dir( os.path.join(pixiedust_home, 'gateway') )

    def _ensure_dir(self, parentLoc):
        if not os.path.isdir(parentLoc):
            os.makedirs(parentLoc)
        return parentLoc

    @default('notebook_loader')
    def notebook_loader_default(self):
        return 'pixiegateway.notebookMgr.NotebookFileLoader'

    def __init__(self, **kwargs):
        kwargs['parent'] = PixieGatewayApp.instance()
        super(NotebookMgr, self).__init__(**kwargs)
        # Read the notebooks
        self.ns_counter = 0
        self.pixieapps = {}
        self.loader = import_object(self.notebook_loader)()
        self._readNotebooks()

    def next_namespace(self):
        self.ns_counter += 1
        return "ns{}_".format(self.ns_counter)

    def notebook_pixieapps(self):
        return list(self.pixieapps.values())

    @gen.coroutine
    def publish(self, name, notebook):
        full_path = os.path.join(self.notebook_dir, name)
        pixieapp_def = self.read_pixieapp_def(notebook)
        log_messages = ["Validating Notebook... Looking for a PixieApp"]
        if pixieapp_def is not None and pixieapp_def.is_valid:
            log_messages.append("PixieApp {} found. Proceeding with Publish".format(pixieapp_def.name))
            pixieapp_def.location = full_path
            self.pixieapps[pixieapp_def.name] = pixieapp_def
            with io.open(full_path, 'w', encoding='utf-8') as f:
                nbformat.write(notebook, f, version=nbformat.NO_CONVERT)
            log_messages.append("Successfully stored notebook file {}".format(name))
            yield ManagedClientPool.instance().on_publish(pixieapp_def, log_messages)
            pixieapp_model = {"log":log_messages}
            pixieapp_model.update(pixieapp_def.to_dict())
            raise gen.Return(pixieapp_model)
        else:
            log_messages.append("Invalid notebook or no PixieApp found")
            raise Exception("Invalid notebook or no PixieApp found")

    def get_notebook_pixieapp(self, pixieAppName):
        """
        Return the pixieapp definition associeted with the given name, None if doens't exist
        Parameters
        ----------
        pixieAppName: str
            Name of the app

        Returns
        -------
        PixieappDef
            PixieApp definition object
        """
        return self.pixieapps.get(pixieAppName, None)

    def _readNotebooks(self):
        app_log.debug("Reading notebooks from notebook_dir %s", self.notebook_dir)
        if self.notebook_dir is None:
            app_log.warning("No notebooks to load")
            return
        for path in os.listdir(self.notebook_dir):
            if path.endswith(".ipynb"):
                full_path = os.path.join(self.notebook_dir, path)
                nb_contents = self.loader.load(full_path)
                if nb_contents is not None:
                    with nb_contents:
                        app_log.debug("loading Notebook: %s", full_path)
                        notebook = nbformat.read(nb_contents, as_version=4)
                        #Load the pixieapp definition if any
                        pixieapp_def = self.read_pixieapp_def(notebook)
                        if pixieapp_def is not None and pixieapp_def.is_valid:
                            pixieapp_def.location = full_path
                            self.pixieapps[pixieapp_def.name] = pixieapp_def
                        else:
                            app_log.info("Skipping Notebook %s because no valid pixieapp was found", full_path)

    def read_pixieapp_def(self, notebook):
        #Load the warmup and run code
        warmup_code = ""
        run_code = None
        for cell in notebook.cells:
            if cell.cell_type == "code":
                if 'tags' in cell.metadata and "pixieapp" in [t.lower() for t in cell.metadata.tags]:
                    run_code = cell.source
                    break
                elif get_symbol_table(ast_parse(cell.source)).get('pixieapp_root_node', None) is not None:
                    run_code = cell.source
                    break
                else:
                    warmup_code += "\n" + cell.source

        if run_code is not None:
            pixieapp_def = PixieappDef(self.next_namespace(), warmup_code, run_code, notebook)
            return pixieapp_def if pixieapp_def.is_valid else None

def get_symbol_table(rootNode, ctx_symbols=None):
    lookup = VarsLookup(ctx_symbols)
    lookup.visit(rootNode)
    return lookup.symbol_table

class PixieappDef():
    def __init__(self, namespace, warmup_code, run_code, notebook):
        self.raw_warmup_code = warmup_code
        self.raw_run_code = run_code
        self._warmup_code = None
        self._run_code = None
        self.namespace = namespace
        self.location = None
        pixiedust_meta = notebook.get("metadata",{}).get("pixiedust",{})
        self.title = pixiedust_meta.get("title",None)
        self.deps = pixiedust_meta.get("imports", {})
        self.pref_kernel = pixiedust_meta.get("kernel", None)

        #validate and process the code
        self.symbols = get_symbol_table(ast_parse(self.raw_warmup_code + "\n" + self.raw_run_code))
        pixieapp_root_node = self.symbols.get('pixieapp_root_node', None)
        self.name = pixieapp_root_node.name if pixieapp_root_node is not None else None
        self.description = ast.get_docstring(pixieapp_root_node) if pixieapp_root_node is not None else None

    @property
    def warmup_code(self):
        if self._warmup_code is not None:
            return self._warmup_code
        if not self.is_valid:
            raise Exception("Trying to access warmup_code but not a valid pixieapp notebook")
        if self.symbols is not None and self.raw_warmup_code != "":
            rewrite = RewriteGlobals(self.symbols, self.namespace)
            new_root = rewrite.visit(ast_parse(self.raw_warmup_code))
            self._warmup_code = astunparse.unparse(new_root)
            app_log.debug("New warmup code: %s", self._warmup_code)
        else:
            self._warmup_code = ""
        return self._warmup_code

    @property
    def run_code(self):
        if self._run_code is not None:
            return self._run_code
        if not self.is_valid:
            raise Exception("Trying to access run_code but not a valid pixieapp notebook")
        if self.symbols is not None and self.raw_run_code != "":
            rewrite = RewriteGlobals(self.symbols, self.namespace)
            new_root = rewrite.visit(ast_parse(self.raw_run_code))
            self._run_code = astunparse.unparse(new_root)
            app_log.debug("new run code: %s", self._run_code)
        else:
            self._run_code = ""
        return self._run_code

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "warmup_code": self.warmup_code,
            "run_code": self.run_code
        }

    @property
    def is_valid(self):
        return self.name is not None

    @gen.coroutine
    def warmup(self, managed_client):
        exc = managed_client.get_app_stats(self, 'warmup_exception')
        if exc is not None:
            raise exc
        warmup_future = managed_client.get_app_stats(self, 'warmup_future')
        if warmup_future is None:
            warmup_future = Future()
            managed_client.set_app_stats(self, 'warmup_future', warmup_future)
            if self.warmup_code == "":
                warmup_future.set_result("")
            else:
                app_log.debug("Running warmup code: %s", self.warmup_code)
                with (yield managed_client.lock.acquire()):
                    try:
                        yield managed_client.execute_code(self.warmup_code)
                        warmup_future.done()
                    except Exception as exc:
                        app_log.exception(exc)
                        managed_client.set_app_stats(self, 'warmup_exception', exc)
                        raise exc
        raise gen.Return(warmup_future)

    def get_run_code(self, session, run_id):
        pars = ast.parse(self.run_code)
        vl = RewriteGlobals(get_symbol_table(pars), session.namespace)
        vl.visit(pars)
        run_code = """
from pixiedust.display.app import pixieapp
try:
    pixieapp.pixieAppRunCustomizer.gateway = '{}'
    {}
finally:
    pixieapp.pixieAppRunCustomizer.gateway = 'true'
        """.format(run_id, astunparse.unparse(pars).strip().replace('\n', '\n    '))
        print("Run code: {}".format(run_code))
        return run_code
    
class VarsLookup(ast.NodeVisitor):
    def __init__(self, ctx_symbols=None):
        self.symbol_table = {"vars":set(), "functions":set(), "classes":set(), "pixieapp_root_node":None}
        self.ctx_symbols = ctx_symbols
        self.level = 0

    def is_in_ctx(self, name):
        if self.ctx_symbols is None:
            return None
        return name in self.ctx_symbols["vars"] or name in self.ctx_symbols["functions"] or name in self.ctx_symbols["classes"]
    
    #pylint: disable=E0213,E1102
    def onvisit(func):
        def wrap(self, node):
            if self.level > 0:
                if self.level == 1:
                    app_log.debug("\n")
                app_log.debug("%s Level %s: %s", "\t" * (self.level - 1), self.level, ast.dump(node))
            elif self.level < 0:
                app_log.debug("GOT A NON ZERO LEVEL %s", ast.dump(node))
            ret_node = func(self, node)
            self.level += 1
            try:
                cutoff_level = 2 if isinstance(node, ast.Assign) else 1
                if self.level <= cutoff_level:
                    super(VarsLookup, self).generic_visit(node)
                return ret_node
            finally:
                self.level -= 1
        return wrap

    @onvisit
    def visit_Name(self, node):
        if hasattr(node, "ctx") and isinstance(node.ctx, ast.Store) and not self.is_in_ctx(node.id):
            self.symbol_table["vars"].add(node.id)
    @onvisit    
    def visit_FunctionDef(self, node):
        self.symbol_table["functions"].add(node.name)
    
    @onvisit
    def visit_ClassDef(self, node):
        for dec in node.decorator_list:
            if isinstance(dec, ast.Name) and dec.id == "PixieApp":
                self.symbol_table["pixieapp_root_node"] = node
        self.symbol_table["classes"].add(node.name)
        
    @onvisit
    def generic_visit(self, node):
        pass

class RewriteGlobals(ast.NodeTransformer):    
    def __init__(self, symbols, namespace):
        self.symbols = symbols
        self.namespace = namespace
        self.level = 0
        self.localTables = []
        self.pixieApp = None
        self.pixieAppRootNode = None
        
    def isGlobal(self, name):
        #Check the local context first
        if len(self.localTables) > 1:
            for table in reversed(self.localTables[2:]):
                if name in table["vars"] or name in table["functions"] or name in table["classes"]:
                    return False
        ret = name in self.symbols["vars"] or name in self.symbols["functions"] or name in self.symbols["classes"]
        return ret

    #pylint: disable=E0213,E1102    
    def onvisit(fn):
        def wrap(self, node):
            if self.level > 0:
                if self.level == 1:
                    app_log.debug("\n")
                app_log.debug("%s Level %s: %s", "\t" * (self.level - 1), self.level, ast.dump(node))
            elif self.level < 0:
                app_log.debug("GOT A NON ZERO LEVEL %s", ast.dump(node))
            ret_node = fn(self,node)
            self.level += 1
            self.localTables.append( get_symbol_table(node, self.symbols) )
            try:
                super(RewriteGlobals, self).generic_visit(node)
                return ret_node or node
            finally:
                self.level -= 1
                self.localTables.pop()
        return wrap
    
    @onvisit
    def visit_FunctionDef(self, node):
        if self.level == 1 and self.isGlobal(node.name):
            node.name = self.namespace + node.name
        return node

    @onvisit
    def visit_ClassDef(self, node):
        for dec in node.decorator_list:
            if isinstance(dec, ast.Name) and dec.id == "PixieApp":
                self.pixieApp = node.name
                self.pixieAppRootNode = node
        if self.pixieApp != node.name and self.level == 1 and self.isGlobal(node.name):
            node.name = self.namespace + node.name
        return node

    @onvisit
    def visit_Name(self, node):
        if hasattr(node, "ctx"):
            if self.pixieApp != node.id and isinstance(node.ctx, ast.Load) and self.isGlobal(node.id):
                node.id = self.namespace + node.id
            elif isinstance(node.ctx, ast.Store) and self.isGlobal(node.id):
                node.id = self.namespace + node.id
        return node

    @onvisit
    def generic_visit(self, node):
        return node
