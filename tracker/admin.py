from django.contrib import admin
from tracker.models import Queue, Ticket, FollowUp, TicketChange, Attachment

class QueueAdmin(admin.ModelAdmin):
	fieldsets = (
		('General information', {'fields': ('title', 'slug', 'email_address', 'new_ticket_cc', 'allow_public_submission', 'active', 'public', 'escalate_days'), 'classes': ('wide', 'extrapretty')}),
	)
	list_display = ('title', 'slug', 'email_address', 'new_ticket_cc', 'active', 'public')
	list_display_links = ('title',)
	list_filter = ('active', 'public', 'allow_public_submission')
	list_per_page = 25
	search_fields = ['title', 'email_address', 'new_ticket_cc']
	
class TicketAdmin(admin.ModelAdmin):
	fieldsets = (
		('General information', {'fields': ('queue', 'title', 'description', 'public', 'submitter_email'), 'classes': ('wide', 'extrapretty')}),
		('Advanced informtion', {'fields': ('status', 'priority', 'on_hold', 'assigned_to'), 'classes': ('wide', 'extrapretty')}),
		('Resolution', {'fields': ('resolution',), 'classes': ('wide', 'extrapretty')}),
	)
	list_display = ('title', 'id', 'queue', 'public', 'submitter_email', 'status', 'priority', 'on_hold', 'get_assigned_to')
	list_display_links = ('title',)
	list_per_page = 25
	list_filter = ('modified', 'status', 'priority', 'on_hold', 'queue')
	search_fields = ['title', 'submitter_email', 'assigned_to__first_name', 'assigned_to__last_name', 'description']
	date_hierarchy = 'created'
	raw_id_fields = ['assigned_to']
	
class TicketChangeInline(admin.TabularInline):
	model = TicketChange
	extra = 3
	
class AttachmentInline(admin.TabularInline):
	model = Attachment
	extra = 3
	
class FollowUpAdmin(admin.ModelAdmin):
	fieldsets = (
		('General information', {'fields': ('ticket', 'title', 'comment', 'user', 'public'), 'classes': ('wide', 'extrapretty')}),
	)
	list_display = ('title', 'ticket', 'date', 'user', 'public')
	list_per_page = 25
	list_filter = ('public',)
	search_fields = ['title', 'comment', 'ticket', 'user__first_name', 'user__last_name']
	date_hierarchy = 'date'
	raw_id_fields = ['user', 'ticket']
	inlines = [TicketChangeInline, AttachmentInline]

admin.site.register(Queue, QueueAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(FollowUp, FollowUpAdmin)