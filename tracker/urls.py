from django.conf.urls.defaults import *

urlpatterns = patterns('tracker.views.public',
	url(r'^$', 'index', name='tracker-public-index'),
	url(r'^ticket/find/$', 'find_ticket', name='tracker-public-find-ticket'),
	url(r'^ticket/browse/$', 'browse_tickets', name='tracker-public-browse-tickets'),
	url(r'^ticket/(?P<queue>\w+)/(?P<id>\d+)/$', 'view_ticket', name='tracker-public-view-ticket'),
)