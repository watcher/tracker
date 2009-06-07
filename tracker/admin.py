from django.contrib import admin
from tracker.models import Queue

class QueueAdmin(admin.ModelAdmin):
	fieldsets = (
		('General information', {'fields': ('title', 'slug', 'email_address', 'new_ticket_cc', 'allow_public_submission', 'active', 'escalate_days'), 'classes': ('wide', 'extrapretty')}),
	)
	list_display = ('title', 'slug', 'email_address', 'new_ticket_cc', 'active')
	list_display_links = ('title',)
	list_filter = ('active',)
	list_per_page = 25
	search_fields = ['title', 'email_address', 'new_ticket_cc']

admin.site.register(Queue, QueueAdmin)