from django.contrib import admin
from tracker.models import Queue, Ticket

class QueueAdmin(admin.ModelAdmin):
	fieldsets = (
		('General information', {'fields': ('title', 'slug', 'email_address', 'new_ticket_cc', 'allow_public_submission', 'active', 'escalate_days'), 'classes': ('wide', 'extrapretty')}),
	)
	list_display = ('title', 'slug', 'email_address', 'new_ticket_cc', 'active')
	list_display_links = ('title',)
	list_filter = ('active',)
	list_per_page = 25
	search_fields = ['title', 'email_address', 'new_ticket_cc']
	actions = ['deactivate_queues', 'activate_queues']
	
	def deactivate_queues(self, request, queryset):
		queryset.update(active=False)
	deactivate_queues.short_description = 'Mark selected queues as inactive'
	
	def activate_queues(self, request, queryset):
		queryset.update(active=True)
	activate_queues.short_description = 'Mark selected queues as active'
	
class TicketAdmin(admin.ModelAdmin):
	fieldsets = (
		('General information', {'fields': ('queue', 'title', 'description', 'public', 'submitter_email'), 'classes': ('wide', 'extrapretty')}),
		('Advanced informtion', {'fields': ('status', 'priority', 'on_hold', 'assigned_to'), 'classes': ('wide', 'extrapretty')}),
		('Resolution', {'fields': ('resolution',), 'classes': ('wide', 'extrapretty')}),
	)
	list_display = ('title', 'id', 'queue', 'public', 'submitter_email', 'status', 'priority', 'on_hold', '_get_assigned_to')
	list_display_links = ('title',)
	list_per_page = 25
	list_filter = ('modified', 'status', 'priority', 'on_hold', 'queue')
	search_fields = ['title', 'submitter_email', 'assigned_to__first_name', 'assigned_to__last_name', 'description']
	date_hierarchy = 'created'
	raw_id_fields = ['assigned_to']

admin.site.register(Queue, QueueAdmin)
admin.site.register(Ticket, TicketAdmin)