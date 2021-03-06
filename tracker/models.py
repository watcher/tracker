from django.db import models
from django.contrib.auth.models import User
from tracker.lib import unique_slugify
from tracker.managers import FollowUpManager

class Queue(models.Model):
	title = models.CharField('Title', max_length=250)
	slug = models.SlugField('Slug', blank=True)
	email_address = models.EmailField('E-Mail address')
	allow_public_submission = models.BooleanField('Allow the submission of tickets from non-logged in users?', default=True)
	active = models.BooleanField('Active queue?', default=True)
	escalate_days = models.IntegerField('Escalation days', default=0, blank=True, null=True)
	new_ticket_cc = models.EmailField('New ticket CC e-mail address', blank=True, null=True)
	
	def __unicode__(self):
		return self.title
		
	class Meta:
		ordering = ['title']
		
	def save(self, *args, **kwargs):
		self.title = self.title.capitalize()
		
		if not self.slug:
			unique_slugify(self, self.title, 'slug')
			
		super(Queue, self).save(*args, **kwargs)
		
class Ticket(models.Model):
	NEW_STATUS = 1
	OPEN_STATUS = 2
	REOPENED_STATUS = 3
	RESOLVED_STATUS = 4
	CLOSED_STATUS = 5
	
	STATUS_CHOICES = (
		(NEW_STATUS, 'New'),
		(OPEN_STATUS, 'Open'),
		(REOPENED_STATUS, 'Reopened'),
		(RESOLVED_STATUS, 'Resolved'),
		(CLOSED_STATUS, 'Closed'),
	)
	
	PRIORITY_CHOICES = (
		(1, '1. Critical'),
		(2, '2. High'),
		(3, '3. Normal'),
		(4, '4. Low'),
		(5, '5. Very low'),
	)
	
	queue = models.ForeignKey(Queue)
	title = models.CharField('Title', max_length=250)
	description = models.TextField('Description', blank=True, null=True)
	resolution = models.TextField('Resolution', blank=True, null=True)
	public = models.BooleanField('Public ticket?', default=False)
	submitter_email = models.EmailField('Submitter e-mail', blank=True, null=True)
	assigned_to = models.ForeignKey(User, verbose_name='Assigned to', blank=True, null=True)
	status = models.IntegerField('Status', choices=STATUS_CHOICES, default=NEW_STATUS)
	on_hold = models.BooleanField('On hold?', default=False)
	priority = models.IntegerField('Priority', choices=PRIORITY_CHOICES, default=3)
	last_escalation = models.DateTimeField('Last escalation date', blank=True, editable=False, null=True)
	allow_comments = models.BooleanField('Allow comments?', default=True)
	created = models.DateTimeField('Created', auto_now_add=True)
	modified = models.DateTimeField('Modified', auto_now=True)
	
	def _get_assigned_to(self):
		if not self.assigned_to:
			return 'Unassigned'
		else:
			if self.assigned_to.get_full_name():
				return self.assigned_to.get_full_name()
			else:
				return self.assigned_to
	_get_assigned_to.short_description = 'Assigned to'
	get_assigned_to = property(_get_assigned_to)
	
	def _get_ticket_slug(self):
		return "[%s - %s]" % (self.queue.slug, self.id)
	get_ticket_slug = property(_get_ticket_slug)
	
	def _get_status(self):
		held_msg = ''
		if self.on_hold:
			held_msg = ' - on hold'
		
		return "%s%s" % (self.get_status_display().lower(), held_msg)
	get_status = property(_get_status)
	
	def _is_public(self):
		return self.public and not self.status == self.NEW_STATUS and self.allow_comments
	is_public = property(_is_public)
	
	def __unicode__(self):
		return self.title
		
	class Meta:
		get_latest_by = 'created'
		ordering = ['-created']
		
	@models.permalink
	def get_absolute_url(self):
		return ('tracker-public-view-ticket', (), {'queue': self.queue.slug, 'id': str(self.id)})
		
class FollowUp(models.Model):
	ticket = models.ForeignKey(Ticket)
	date = models.DateTimeField('Date', auto_now_add=True)
	title = models.CharField('Title', max_length=200, blank=True, null=True)
	comment = models.TextField('Comment', blank=True, null=True)
	public = models.BooleanField('Public?', default=True)
	user = models.ForeignKey(User, blank=True, null=True)
	objects = FollowUpManager()
	
	def __unicode__(self):
		return self.title
		
	class Meta:
		ordering = ['date']
		
	def save(self, *args, **kwargs):
		self.ticket.save()
		
		super(FollowUp, self).save(*args, **kwargs)
		
class TicketChange(models.Model):
	followup = models.ForeignKey(FollowUp)
	field = models.CharField('Field', max_length=200)
	old_value = models.CharField('Old value', max_length=200, blank=True, null=True)
	new_value = models.CharField('New value', max_length=200, blank=True, null=True)
	
	def __unicode__(self):
		string = "%s " % self.field
		
		if not self.new_value:
			str += 'removed'
		elif not self.old_value:
			str += "set to %s" % self.new_value
		else:
			str += "changed from %s to %s" % (self.old_value, self.new_value)
			
		return str
		
def attachment_path(instance, filename):
	from django.conf import settings
	import os
	
	os.umask(0)
	path = "tracker/attachments/%s-%s/%s" % (instance.followup.ticket.queue.slug, instance.followup.ticket.id, instance.followup.id)
	att_path = os.path.join(settings.MEDIA_ROOT, path)
	
	if not os.path.exists(att_path):
		os.makedirs(att_path, 0777)
		
	return os.path.join(path, filename)
		
class Attachment(models.Model):
	followup = models.ForeignKey(FollowUp)
	file = models.FileField('File', upload_to=attachment_path)
	filename = models.CharField('Filename', max_length=250)
	mime_type = models.CharField('MIME type', max_length=30)
	size = models.IntegerField('Size')
	
	def get_upload_to(self, field_attname):
		if not self.id:
			return ''
		return "tracker/attachments/%s-%s/%s" % (self.followup.ticket.queue.slug, self.followup.ticket.id, instance.followup.id)
		
	def __unicode__(self):
		return self.filename
		
	class Meta:
		ordering = ['filename']