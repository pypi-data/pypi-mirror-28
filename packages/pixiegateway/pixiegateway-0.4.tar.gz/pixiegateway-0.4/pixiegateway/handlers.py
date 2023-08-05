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
# pylint: disable=W0223

import traceback
import json
import inspect
import os
import re
import base64
from uuid import uuid4
from collections import OrderedDict, deque
import nbformat
import tornado
from tornado import gen, web
from tornado.log import app_log
from tornado.util import import_object
from six import PY3, iteritems
from six.moves.urllib import parse
from .session import SessionManager
from .notebookMgr import NotebookMgr
from .managedClient import ManagedClientPool
from .chartsManager import SingletonChartStorage
from .utils import sanitize_traceback
from .pixieGatewayApp import PixieGatewayApp
from .exceptions import CodeExecutionError

class BaseHandler(tornado.web.RequestHandler):
    """Base class for all PixieGateway handler"""
    def initialize(self):
        self.output_json_error = False

    def _handle_request_exception(self, exc):
        html_error = "<div>Unexpected error:</div><pre>{}</pre>".format(
            str(exc) if isinstance(exc, CodeExecutionError) else traceback.format_exc()
        )
        if self.output_json_error:
            msg = {
                "buffers": [],
                "channel": "iopub",
                "content": {
                    "data": {
                        "text/html": html_error
                    },
                    "metadata": {},
                    "transient": {}
                },
                "header": {
                    "username": "pixiegateway",
                    "msg_type": "display_data",
                    "msg_id": uuid4().hex,
                    "version": "5.2"
                },
                "metadata": {},
                "msg_id": "",
                "msg_type":"display_data",
                "parent_header": {}
            }
            self.write(json.dumps([msg]))
        else:
            self.write(html_error)
        self.finish()

    def get_template_path(self):
        return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

    def prepare(self):
        """
        Retrieve session for current user
        """
        self.session = SessionManager.instance().get_session(self)
        app_log.debug("session %s", self.session)

    def get_current_user(self):
        return self.get_secure_cookie("pd_user")

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

class TemplateDispatcherHandler(BaseHandler):
    """
    Generic handler that renders through a template
    """
    def initialize(self, template_name):
        self.template_name = template_name

    def get(self):
        self.render(self.template_name)

class LoginHandler(BaseHandler):
    def get(self):
        self.render("template/login.html")
    def validate_credentials(self, userid, password):
        return userid == self.settings.get("admin_user_id","admin") and password == self.settings.get("admin_password")
    def post(self):
        if not self.validate_credentials(self.get_argument("userid"), self.get_argument("password")):
            return self.render("template/login.html", error="Incorrect userid or password")
        self.set_secure_cookie("pd_user", self.get_argument("userid"))
        self.redirect(self.get_argument("next"))

class ExecuteCodeHandler(BaseHandler):
    """
Common Base Tornado Request Handler class.
Implement generic kernel code execution routine
    """
    def initialize(self):
        self.output_json_error = True

    @gen.coroutine
    def post(self, *args, **kwargs):
        run_id = args[0]
        #First check if it's a kernel_id (admin mode)
        managed_client = ManagedClientPool.instance().get_by_kernel_id(run_id)
        if managed_client is not None:
            yield self.admin_mode_execute_code(managed_client)
        else:
            managed_client = yield self.session.get_managed_client_by_run_id(run_id)
            yield self.execute_code(managed_client)

    @gen.coroutine
    @tornado.web.authenticated
    def admin_mode_execute_code(self, managed_client):
        yield self.execute_code(managed_client)

    @gen.coroutine
    def execute_code(self, managed_client):
        with (yield managed_client.lock.acquire()):
            try:
                response = yield managed_client.execute_code(self.request.body.decode('utf-8'))
                self.write(response)
                self.finish()
            except Exception as exc:
                self._handle_request_exception(exc)

class PixieAppHandler(BaseHandler):
    """
    Entry point for running a PixieApp
    """
    @gen.coroutine
    def get(self, *args, **kwargs):
        clazz = args[0]

        #check the notebooks first
        pixieapp_def = NotebookMgr.instance().get_notebook_pixieapp(clazz)
        code = None
        managed_client = yield self.session.get_managed_client(self, pixieapp_def, True)
        if pixieapp_def is not None:
            yield pixieapp_def.warmup(managed_client)
            code = pixieapp_def.get_run_code(
                self.session,
                self.session.get_pixieapp_run_id(self, pixieapp_def)
            )
        else:
            instance_name = self.session.getInstanceName(clazz)
            code = """
def my_import(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod
clazz = "{clazz}"

{instance_name} = my_import(clazz)()
{instance_name}.run()
            """.format(clazz=args[0], instance_name=instance_name)

        with (yield managed_client.lock.acquire()):
            response = yield managed_client.execute_code(code, self.result_extractor)
            self.render("template/main.html", response=response, title=pixieapp_def.title if pixieapp_def is not None else None)

    def result_extractor(self, result_accumulator):
        res = []
        for msg in result_accumulator:
            if msg['header']['msg_type'] == 'stream':
                res.append(msg['content']['text'])
            elif msg['header']['msg_type'] == 'display_data':
                if "data" in msg['content'] and "text/html" in msg['content']['data']:
                    res.append(msg['content']['data']['text/html'])
                else:
                    app_log.warning("display_data msg not processed: %s", msg)                    
            elif msg['header']['msg_type'] == 'error':
                error_name = msg['content']['ename']
                error_value = msg['content']['evalue']
                trace = sanitize_traceback(msg['content']['traceback'])
                return 'Error {}: {}\n{}\n'.format(error_name, error_value, trace)
            else:
                app_log.warning("Message type not processed: %s", msg['header']['msg_type'])
        return ''.join(res)

class PixieDustHandler(BaseHandler):
    def initialize(self, loadjs):
        self.loadjs = loadjs

    def get(self):
        from pixiedust.display.display import Display
        class PixieDustDisplay(Display):
            def doRender(self, handlerId):
                pass
        self.set_header('Content-Type', 'text/javascript' if self.loadjs else 'text/css')
        disp = PixieDustDisplay({"gateway":"true"}, None)
        disp.callerText = "display(None)"
        self.write(disp.renderTemplate("pixiedust.js" if self.loadjs else "pixiedust.css"))
        self.finish()

class PixieAppListHandler(BaseHandler):
    def get(self):
        self.redirect("/admin/apps")

class AdminHandler(BaseHandler):
    def fetch_logs(self):
        with open( PixieGatewayApp.instance().log_path) as log_file:
            return "\n".join(deque(log_file, 100))
    @tornado.web.authenticated
    def get(self, tab_id):
        tab_definitions = OrderedDict([
            ("apps", {"name": "PixieApps", "path": "admin/pixieappList.html", "description": "Published PixieApps",
                      "args": lambda: {"pixieapp_list":NotebookMgr.instance().notebook_pixieapps()}}),
            ("charts", {"name": "Charts", "path": "admin/chartsList.html", "description": "Shared Charts"}),
            ("stats", {
                "default": {"name": "Kernel Stats", "path": "admin/adminStats.html", "description": "PixieGateway Statistics"},
                "app": {
                    "name": "PixieApp Details", "path": "admin/pixieappDetails.html", 
                    "description": "PixieApp Details", "manager":"pixiegateway.admin.AppController"
                },
                "kernel":{
                    "name": "Kernel Details", "path": "admin/kernelDetails.html",
                    "description": "Kernel Details", "manager": "pixiegateway.admin.KernelController"
                }
            }
            ),
            ("logs", {"name": "Server Logs", "path": "admin/adminLogs.html", "description": "Server logs",
                      "args": lambda: {"logs": self.fetch_logs()}})
        ])
        tab_id, content_definition = self.compute_tab_id(tab_definitions, tab_id or "apps")
        self.render(
            "template/admin/adminConsole.html",
            tab_definitions=tab_definitions,
            selected_tab_id=tab_id,
            content_definition=content_definition
        )

    def compute_tab_id(self, tab_definitions, tab_id):
        parts = tab_id.split("/")
        tab_id = parts[0]
        if tab_id not in tab_definitions:
            raise Exception("Invalid url")

        content_definition = tab_definitions[tab_id]
        if "default" in content_definition:
            content_definition = content_definition[parts[1] if len(parts) > 1 else 'default']
            if len(parts) > 2:
                parts = parts[1:]
                if len(parts) % 2 != 0:
                    raise Exception("Invalid url")
                content_definition = content_definition.copy()
                orgs_arg_callable = content_definition.get("args", None)
                def args_wrapper():
                    results = orgs_arg_callable() if orgs_arg_callable is not None else {}
                    ite = iter(parts)
                    results.update({p:next(ite) for p in ite})
                    if "manager" in content_definition:
                        results['manager'] = import_object(content_definition['manager'])(results)
                    return results
                content_definition["args"] = args_wrapper
        return tab_id, content_definition

class PixieAppPublishHandler(BaseHandler):
    @gen.coroutine
    def post(self, name):
        payload = self.request.body.decode('utf-8')
        try:
            notebook = nbformat.from_dict(json.loads(payload))
            pixieapp_model = yield NotebookMgr.instance().publish(name, notebook)
            self.set_status(200)
            self.write(json.dumps(pixieapp_model))
            self.finish()
        except Exception as exc:
            app_log.error(traceback.print_exc())
            raise web.HTTPError(400, u'Publish PixieApp error: {}'.format(exc))

class ChartShareHandler(BaseHandler):
    @gen.coroutine
    def post(self, chart_id):
        payload = json.loads(self.request.body.decode('utf-8'))
        try:
            chart_model = yield gen.maybe_future(SingletonChartStorage.instance().store_chart(payload))
            self.set_status(200)
            self.write(json.dumps(chart_model))
            self.finish()
        except Exception as exc:
            app_log.error(traceback.print_exc())
            raise web.HTTPError(400, u'Share Chart error: {}'.format(exc))

    @gen.coroutine
    def get(self, chart_id):
        chart_model = yield gen.maybe_future(SingletonChartStorage.instance().get_chart(chart_id))
        if chart_model is None:
            self.set_status(404)
            self.write("Chart not found {}".format(chart_id))
            self.finish()

        fmt = self.get_query_argument("format", "")
        if fmt == "thumbnail":
            thumbnail = chart_model.get("THUMBNAIL", None)
            if thumbnail is None:
                from .chartThumbnail import Thumbnail
                thumbnail = yield Thumbnail.instance().get_screenshot_as_png(chart_model)
            else:
                thumbnail = base64.b64decode(thumbnail)
            self.set_header('Content-Type', 'image/png')
            self.write(thumbnail)
            self.finish()
        else:
            self.render("template/showChart.html", chart_model=chart_model)

class ChartEmbedHandler(BaseHandler):
    @gen.coroutine
    def get(self, chart_id, width, height):
        chart_model = yield gen.maybe_future(SingletonChartStorage.instance().get_chart(chart_id))
        if chart_model is not None:
            if 'RENDERERID' in chart_model:
                content = chart_model['CONTENT']
                if chart_model['RENDERERID'] == 'bokeh':
                    if width:
                        regex = re.compile('(("|\')plot_width("|\')\s*:\s*[0-9]+)')
                        content = re.sub(regex, '"plot_width":' + str(int(width) - 25), content)
                    if height:
                        regex = re.compile('(("|\')plot_height("|\')\s*:\s*[0-9]+)')
                        content = re.sub(regex, '"plot_height":' + str(int(height) - 40), content)
                if chart_model['RENDERERID'] == 'matplotlib':
                    size = ';'
                    if width:
                        size += 'width:' + str(int(width) - 25) + 'px;'
                    if height:
                        size += 'height:' + str(int(height) - 40) + 'px;'
                    regex = re.search('(<img.*)(?P<style_tag>style="[^"]+)([^<]*>)', content)
                    if regex and regex.group('style_tag'):
                        content = content.replace(regex.group('style_tag'), regex.group('style_tag') + size)
                chart_model['CONTENT'] = content
            self.render("template/embedChart.html", chart_model=chart_model)
        else:
            self.set_status(404)
            self.write("Chart not found")
            self.finish()

class OEmbedChartHandler(BaseHandler):
    def get(self):
        url = self.get_query_argument("url")
        server = self.request.protocol + "://" + self.request.host
        match = re.match("/chart/(?P<chartid>.*)", parse.urlparse(url).path)
        if match is None:
            self.set_status(404)
            return self.write("Invalid url {}".format(url))
        chartid = match.group('chartid')
        width = 600
        height = 400
        height_ratio = min(int(self.get_query_argument("maxheight", height)), height)/height
        width_ratio = min(int(self.get_query_argument("maxwidth", width)), width)/width

        width = int(width * min(height_ratio, width_ratio))
        height = int(height * min(height_ratio, width_ratio))
        html = """
        <object type="text/html" data="{server}/embed/{chartid}/{width}/{height}" width="{width}" height="{height}">
            <a href="{server}/embed/{chartid}">View Chart</a>' +
        </object>
        """.format(server=server, chartid=chartid, width=width, height=height)
        payload = {
            "version": "1.0",
            "type": "rich",
            "html": html,
            "width": width,
            "height": height,
            "title": "Title",
            "url": url,
            "author_name": "username",
            "provider_name": "PixieGateway",
            "provider_url": "https://github.com/ibm-watson-data-lab/pixiegateway"
        }
        self.write(payload)
        self.set_header('Content-Type', 'application/json')

class ChartsHandler(BaseHandler):
    @gen.coroutine
    def get(self, page_num=0, page_size=10):
        payload = yield gen.maybe_future(SingletonChartStorage.instance().get_charts(int(page_num), int(page_size)))
        self.write(payload)
        self.finish()

class StatsHandler(BaseHandler):
    """
    Provides various stats about the running kernels
    """
    @gen.coroutine
    def get(self, command):
        if command == "kernels":
            specs = yield gen.maybe_future( ManagedClientPool.instance().list_kernel_specs() )
            specs = {k:v for k,v in iteritems(specs) if v['spec']['language'] == 'python'}
            for key, value in iteritems(specs):
                value['default'] = True if key == ('python3' if PY3 else 'python2') else False
            self.write(specs)
            self.finish()
        else:
            yield self._process_command(command)

    @gen.coroutine
    @tornado.web.authenticated
    def _process_command(self, command):
        if command is None:
            stats = yield gen.maybe_future(ManagedClientPool.instance().get_stats())
            for mc_id in stats:
                stats[mc_id]['users'] = SessionManager.instance().get_users_stats(mc_id)
            self.write(stats)
            self.finish()
        else:
            raise web.HTTPError(400, u'Unknown stat command: {}'.format(command))

class PixieDustLogHandler(BaseHandler):
    """
    Access the PixieDust Logs
    """
    @gen.coroutine
    def get(self):
        self.set_header('Content-Type', 'text/html')
        self.set_status(200)
        code = """
import pixiedust
%pixiedustLog -l debug
        """
        managed_client = yield ManagedClientPool.instance().get()
        with (yield managed_client.lock.acquire()):
            try:
                response = yield managed_client.execute_code(code, self.result_extractor)
                self.write(response)
            except:
                traceback.print_exc()
            finally:
                self.finish()

    def result_extractor(self, result_accumulator):
        res = []
        for msg in result_accumulator:
            if msg['header']['msg_type'] == 'stream':
                res.append( msg['content']['text'])
            elif msg['header']['msg_type'] == 'display_data':
                if "data" in msg['content'] and "text/html" in msg['content']['data']:
                    res.append( msg['content']['data']['text/html'] )                    
            elif msg['header']['msg_type'] == 'error':
                error_name = msg['content']['ename']
                error_value = msg['content']['evalue']
                trace = sanitize_traceback(msg['content']['traceback'])
                return 'Error {}: {}\n{}\n'.format(error_name, error_value, trace)

        return '<br/>'.join([w.replace('\n', '<br/>') for w in res])