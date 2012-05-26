from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': 'django.conf'}),
    (r'^appmedia/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    
    (r'', include('deed.urls')),
)
