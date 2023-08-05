import os
import platform

def check_runserver():
    from sys import argv
    _argv_count = len(argv)
    if _argv_count > 1:
        for i in range(1, _argv_count):
            _argv = argv[i].lower()
            if _argv.startswith('runserver'):
                return True
    return False


def get_dirs_name_by_path(path):
    result = []
    for dirpath, dirnames, filenames in os.walk(path):
        for dir in dirnames:
            result.append(dir)
        break
    return result
def get_project_setting_path():
    sysstr = platform.system()

    local_path = os.getcwd()
    dirs = get_dirs_name_by_path(local_path)
    for _dir in dirs:
        if sysstr.lower() == 'windows':
            filename = local_path + '\\' + _dir + '\\settings.py'
            if os.path.exists(filename):
                return _dir
        else:
            filename = local_path + '/' + _dir + '/settings.py'
            if os.path.exists(filename):
                return _dir

os.environ.setdefault("DJANGO_SETTINGS_MODULE", get_project_setting_path() + ".settings")
from django.conf import settings
# settings.LOGIN_URL = '/anon/geely-sso/login'
# settings.LOGOUT_URL = '/anon/geely-sso/logout'
settings.INSTALLED_APPS.append('AGFramework.data_models')
settings.INSTALLED_APPS.append('AGFramework.agadmin')
settings.AUTH_PROFILE_MODULE = 'AGFramework.data_models.UserPlus'
settings.MIDDLEWARE.insert(0,'AGFramework.django_middleware.tracker.request_tracker')

if check_runserver():
    from rest_framework import response
    import AGFramework.extend.response_plus

    response.Response = AGFramework.extend.response_plus.Response
    from rest_framework import mixins
    import AGFramework.extend.mixins_plus

    mixins.ListModelMixin = AGFramework.extend.mixins_plus.ListModelMixin
    mixins.RetrieveModelMixin = AGFramework.extend.mixins_plus.RetrieveModelMixin
    mixins.DestroyModelMixin = AGFramework.extend.mixins_plus.DestroyModelMixin
    mixins.CreateModelMixin = AGFramework.extend.mixins_plus.CreateModelMixin

    import AGFramework.extend.api_view_plus

    from rest_framework import views
    import AGFramework.extend.view_plus

    views.exception_handler = AGFramework.extend.view_plus.exception_handler
    import AGFramework.extend.swagger_plus
    import AGFramework.setting


    if os.environ.get("RUN_MAIN") == "true":
        import AGFramework.scheduler
        import AGFramework.core.statistics