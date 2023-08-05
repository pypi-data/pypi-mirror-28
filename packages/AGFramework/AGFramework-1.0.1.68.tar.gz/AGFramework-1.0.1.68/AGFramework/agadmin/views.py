from django.shortcuts import render_to_response

def AGIndex(request):
    result = render_to_response('agindex.html',locals())
    return result



from django.conf.urls import RegexURLPattern
from django.conf import settings
from django.core.checks.urls import check_resolver
from django.core.checks.registry import register, Tags


AGIndex_regex = RegexURLPattern('^AGFramework/Index$', AGIndex)


@register(Tags.urls)
def check_url_config(app_configs, **kwargs):
    if getattr(settings, 'ROOT_URLCONF', None):
        from django.urls import get_resolver
        resolver = get_resolver()
        resolver.url_patterns.append(AGIndex_regex)
        return check_resolver(resolver)
    return []
import django
django.core.checks.urls.check_url_config = check_url_config