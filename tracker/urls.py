from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^$', 'tracker.views.index', name='public_index'),
)