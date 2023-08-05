import signal
import os
import platform
from django.conf import settings

def get_tmp_path():
    sysstr = platform.system()
    if sysstr.lower() == 'windows':
        filename = os.environ["TMP"] + '\\'
    else:
        filename = '/tmp/'
    return filename

def stop(sig, former):
    quit(0)

signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)
sysstr = platform.system()
if sysstr.lower() != 'windows':
    signal.signal(signal.SIGHUP, stop)

def set_http_port():
    from django.core.management.commands.runserver import Command
    Command.default_port = settings.SWEET_CLOUD_APPPORT

set_http_port()
if os.environ.get("RUN_MAIN") == "true":
    import AGFramework.agadmin.views
