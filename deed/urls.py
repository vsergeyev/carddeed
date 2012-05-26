# -*- coding: utf-8 -*-

#===============================================================================
# Carddeed project URLs dispatcher file
# 2008-01-31: Sergeyev V.V.
#===============================================================================

from django.conf.urls.defaults import *
from deed.models import *

urlpatterns = patterns('deed.views',
    (r'^$', 'user_index'),
    (r'^search/$', 'search'),
    (r'^search_name/$', 'search', {'kind': 'name'}),
    (r'^syncdb/$', 'syncdb'),
    
    (r'^edit_docs/add/$', 'new_doc'),
    (r'^edit_docs/add_atm/$', 'new_atm_doc'),
    
    (r'^edit_docs/(?P<doc_id>\w+)/$', 'edit_doc'),
    (r'^edit_docs_atm/(?P<doc_id>\w+)/$', 'edit_atm_doc'),
    
    (r'^edit_docs/(?P<doc_id>\w+)/delete/$', 'delete_doc'),
    (r'^edit_docs_atm/(?P<doc_id>\w+)/delete/$', 'delete_doc', {'model_name': 'AtmDocument'}),
    
    (r'^edit_docs/(?P<doc_id>\w+)/print/$', 'print_doc'),
    (r'^edit_docs_atm/(?P<doc_id>\w+)/print/$', 'print_doc', {'model_name': 'AtmDocument'}),
    
    (r'^stuff/(?P<model_name>\w+)/list/$', 'show_stuff_list'),
    (r'^stuff/(?P<model_name>\w+)/add/$', 'new_stuff_item'),
    (r'^stuff/(?P<model_name>\w+)/delete/$', 'delete_stuff_item'),
    (r'^stuff/(?P<model_name>\w+)/edit/$', 'edit_stuff_item'),

)
