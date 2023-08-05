from collections import namedtuple
from django.conf import settings
from .session import is_logged_in, fill_user_id, get_user_criteria
from django.views.decorators.http import require_http_methods
from .restview import RestView
from .models.event_models import FirebaseEvents
from django.views.decorators.csrf import ensure_csrf_cookie
from .response_utils import ApiResponse

StaticFiles = namedtuple("StaticFiles", ["CSS", "JS"])
_CSS = settings.ADHARA["CSS"] if "CSS" in settings.ADHARA else {}
_JS = settings.ADHARA["JS"] if "JS" in settings.ADHARA else {}


def _get_for_context(contexts):
    if type(contexts) is str:
        contexts = [contexts]
    css_files = []
    js_files = []
    for context in contexts:
        css_files.extend(_CSS[context])
        js_files.extend(_JS[context])
    return StaticFiles(css_files, js_files)


def include_static_contexts(contexts):
    def ret(fn):
        def req_incl_fn(request, *args, **kwargs):
            kwargs['static_files'] = _get_for_context(contexts)
            return fn(request, *args, **kwargs)
        return req_incl_fn
    return ret


class AdharaView:
    pass


@require_http_methods(["GET"])
@ensure_csrf_cookie
def get_csrf_token(request):
    from django.middleware.csrf import get_token
    return ApiResponse.success(get_token(request))


@require_http_methods(["POST", "DELETE"])
@is_logged_in
@fill_user_id
def register_firebase_event(request):
    rv = RestView(request, FirebaseEvents)
    rv.set_custom_criteria(get_user_criteria(request))
    if request.method == "POST":
        return rv.put_or_create()
    return rv.execute()
