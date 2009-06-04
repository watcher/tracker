from django.contrib import admin
from models import Queue, Ticket, FollowUp, TicketChange

class QueueAdmin(admin.ModelAdmin):
	fieldsets = (
		('Default options', {'fields': ('title', 'slug', 'email_address', 'allow_public_submission', 'allow_email_submission', 'active'), 'classes': ('wide', 'extrapretty')}),
		('Advanced options', {'fields': ('escalate_days', 'new_ticket_cc'), 'classes': ('wide', 'extrapretty')}),
		('E-mail options', {'fields': ('email_box_type', 'email_box_host', 'email_box_port', 'email_box_ssl', 'email_box_user', 'email_box_password', 'email_box_imap_folder', 'email_box_interval'), 'classes': ('wide', 'extrapretty', 'collapse')}),
	)
	list_display = ('title', 'slug', 'email_address', 'active', 'new_ticket_cc')
	list_filter = ('active', 'email_box_type')
	list_per_page = 25
	search_fields = ['title', 'email_address', 'new_ticket_cc', 'email_box_user', 'email_box_host']
	
class TicketAdmin(admin.ModelAdmin):
	fieldsets = (
		('Default information', {'fields': ('title', 'queue', 'submitter_email', 'assigned_to', 'status', 'priority', 'on_hold'), 'classes': ('wide', 'extrapretty')}),
		('Ticket information', {'fields': ('description', 'resolution'), 'classes': ('wide', 'extrapretty')}),
	)
	list_display = ('title', 'status', 'priority', '_get_assigned_to', 'queue', 'on_hold', 'submitter_email')
	list_filter = ('status', 'priority', 'on_hold', 'queue')
	list_per_page = 25
	search_fields = ['title', 'submitter_email', 'description', 'resolution', 'assigned_to__first_name', 'assigned_to__last_name']
	date_hierarchy = 'created'
	raw_id_fields = ['assigned_to']
	
class TicketChangeInline(admin.StackedInline):
	model = TicketChange
	
class FollowUpAdmin(admin.ModelAdmin):
	fieldsets = (
		('Default information', {'fields': ('ticket', 'title', 'comment', 'public', 'user', 'new_status'), 'classes': ('wide', 'extrapretty')}),
	)
	list_display = ('title', 'user', 'public', 'new_status')
	list_filter = ('new_status', 'public')
	list_per_page = 25
	search_fields = ('title', 'comment', 'user__first_name', 'user__last_name')
	raw_id_fields = ['user']
	inlines = [TicketChangeInline]
	
admin.site.register(Queue, QueueAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(FollowUp, FollowUpAdmin)