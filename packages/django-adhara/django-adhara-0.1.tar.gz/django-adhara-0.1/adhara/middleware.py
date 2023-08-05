import json
from urllib.parse import unquote

from django.middleware.csrf import CsrfViewMiddleware
from django.utils.deprecation import MiddlewareMixin

from .request import AdharaRequest, APIMethods
from .response_utils import ApiResponse
from .session import Session
from .thread_local import ThreadLocal
import datetime
import logging


logger = logging.getLogger(__name__)


class ThreadLocalMiddleware(MiddlewareMixin):
    """ Simple middleware that adds the request object in thread local storage. """
    def process_request(self, request):
        ThreadLocal.set_request(request)

    def process_response(self, request, response):
        ThreadLocal._del_request()
        return response

    def process_exception(self, request, exception):
        ThreadLocal._del_request()


class DebugMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.ADHARA_DEBUG = {
            "start_time": datetime.datetime.now()
        }

    def process_response(self, request, response):
        logger.info(
            "request {0} took {1} ms".format(
                request.path,
                datetime.datetime.now()-request.ADHARA_DEBUG["start_time"]
            )
        )
        return response


class AdharaMiddleware(MiddlewareMixin):

    def __call__(self, request):

        path = request.path
        app = path.strip('/').split('/')[0]

        # TODO enhance
        if app == "api":
            if not Session.is_logged_in(request):
                return ApiResponse.error("Not logged in")
        try:
            self.process_request(request)
        except ValueError as ve:
            print(ve)
            return ApiResponse.error("invalid json received")
        except TypeError as te:
            print(te)
            return ApiResponse.error("input format not supported")
        except StopIteration as se:
            print(request.method, "not allowed")
            return ApiResponse.error("Method not allowed")
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    @staticmethod
    def process_request(request):
        ct = request.META['CONTENT_TYPE']
        input_json = {}
        if request.method == 'GET':
            qs = unquote(request.META['QUERY_STRING'])
            query_params = {}
            qs = qs.split('&')
            if not ((len(qs) == 1) and (qs[0].strip() == '')):
                for q in qs:
                    q = q.split('=')
                    try:
                        query_params[q[0]] = json.loads(q[1])
                    except ValueError:
                        query_params[q[0]] = q[1]
                input_json = query_params
        if request.method == 'POST':
            if ct == "application/json":
                rb = request.body.decode('utf-8')
                if rb.strip():
                    input_json = json.loads(rb)
            elif ct == "application/x-www-form-urlencoded":
                input_json = json.loads(json.dumps(request.POST))
            elif ct.startswith("multipart/form-data"):
                pass
            else:
                raise TypeError
        if request.method == 'PUT':
            if ct == "application/json":
                rb = request.body.decode('utf-8')
                if rb.strip():
                    input_json = json.loads(rb)
            else:
                raise TypeError
        if request.method == 'DELETE':
            if ct == "application/json":
                rb = request.body.decode('utf-8')
                if rb.strip():
                    input_json = json.loads(rb)
            else:
                raise TypeError

        if input_json and 'csrfmiddlewaretoken' in input_json:
            del input_json['csrfmiddlewaretoken']
        method = getattr(APIMethods, APIMethods(request.method).name)
        request.adhara_request = AdharaRequest(request, method, input_json)
        return None


class AdharaTokenMiddleware(CsrfViewMiddleware):

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if request.META.get('HTTP_APIKEY'):
            return
        else:
            return super(AdharaTokenMiddleware, self).process_view(request, callback, callback_args, callback_kwargs)
