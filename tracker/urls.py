from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^$', 'tracker.views.public.index', name='tracker-public-index'),
)