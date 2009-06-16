from django.conf.urls.defaults import *

urlpatterns = patterns('tracker.views_public',
	url(r'^$', 'index', name='tracker_public_index'),
)