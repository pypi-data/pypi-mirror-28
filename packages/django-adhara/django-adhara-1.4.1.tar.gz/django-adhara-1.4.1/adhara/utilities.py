from django.conf import settings
import importlib

setting_name = "ADHARA"

try:
    SCOPE = getattr(settings, setting_name)
except AttributeError:
    SCOPE = None


def _get(lookup_scope, path_list):
    try:
        path_var = path_list.pop(0)
        lookup_scope = lookup_scope[path_var]
        if len(path_list):
            return _get(lookup_scope, path_list)
        else:
            return lookup_scope
    except KeyError:
        return None


def get_config(config_path):
    if not SCOPE:
        return None
    return _get(SCOPE, config_path.split("."))


def get_user_model():
    name = get_config("USER_MODEL.MODULE")
    package = get_config("USER_MODEL.PACKAGE")
    if not name or not package:
        name = "User"
        package = "django.contrib.auth.models"
    return getattr(importlib.import_module(package), name)


def get_user_id_field():
    return get_config("USER_MODEL.ID_FIELD") or "user_id"
