from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime
from lib import unique_slugify

class Queue(models.Model):
	"""
	A queue is a collection of ticket into what could be a certain area, project or product (e.g. Support, Bug, ...).
	
	Queues contain all information related to that area and could allow the creation of new tickets in it from email.
	"""
	
	title = models.CharField('title', max_length=250)
	slug = models.SlugField('slug', blank=True, help_text='A unique name for this queue. If empty this is generated from the title.')
	email_address = models.EmailField('e-mail address', blank=True, null=True, help_text='All outgoing e-mails for this queue will be sent from this address. If you plan on importing e-mails from a POP3 or IMAP mailbox, the e-mails will be imported from this e-mailaddress.')
	allow_public_submission = models.BooleanField('allow public submission?', default=True, blank=True, help_text='Allow tickets from non logged-in users?')
	allow_email_submission = models.BooleanField('allow e-mail submission?', default=False, blank=True, help_text='Allow the creation of tickets from e-mails?')
	active = models.BooleanField('active?', default=True, blank=True, help_text='Is this queue active? An inactive queue is visible but does not allow the creation of new tickets.')
	escalate_days = models.IntegerField('escalation days', blank=True, default=0, null=True, help_text='The number of days before a ticket is auto escalated to a higher priority. This only applies to tickets that are currently not on hold. Set to 0 to disable auto escaltion.')
	new_ticket_cc = models.EmailField('new ticket CC address', blank=True, null=True, help_text='An e-mail address to receive notificiation of any new tickets being created in this queue.')
	
	email_box_type = models.CharField('e-mail box type', max_length=5, choices=(('imap', 'IMAP'), ('pop3', 'POP3')), blank=True, null=True, help_text='E-mail server type for the mailbox used in auto ticket creation from e-mail.')
	email_box_host = models.CharField('e-mail box host', max_length=250, blank=True, null=True, help_text='E-mail server host for the mailbox used in auto ticket creation from e-mail.')
	email_box_port = models.IntegerField('e-mail box port', blank=True, null=True, help_text='E-mail server port for the mailbox used in auto ticket creation from e-mail. Default ports are 110 for POP3 and 143 for IMAP. Leave blank to use defaults.')
	email_box_ssl = models.BooleanField('use SSL for e-mail?', default=False, blank=True, help_text='Use SSL for connection to the e-mail server? Default ports are 995 for POP3 and 993 for IMAP when using SSL.')
	email_box_user = models.CharField('e-mail username', max_length=200, blank=True, null=True, help_text='The username used for the connection to the mailbox.')
	email_box_password = models.CharField('e-mail password', max_length=200, blank=True, null=True, help_text='The password used for the connection to the mailbox.')
	email_box_imap_folder = models.CharField('IMAP folder', max_length=100, blank=True, null=True, help_text='When connection to an IMAP server, the name of the mail folder to process email from. Default is INBOX.')
	email_box_interval = models.IntegerField('e-mail check interval', blank=True, null=True, default=5, help_text='How often does this mailbox need to be checked (in minutes)?')
	email_box_last_checked = models.DateTimeField('last check', blank=True, null=True, editable=False)
	
	def _from_address(self):
		"""Short property to provide a sender address in SMTP format."""
		if not self.email_address:
			return 'NO QUEUE EMAIL ADDRESS DEFINED <%s>' % settings.DEFAULT_FROM_EMAIL
		else:
			return '%s <%s>' % (self.title, self.email_address)
	from_address = property(_from_address)
	
	def __unicode__(self):
		return self.title
	
	class Meta:
		ordering = ['title']
	
	def save(self, *args, **kwargs):
		self.title = self.title.lower().capitalize()
		
		if not self.slug:
			unique_slugify(self, self.title, 'slug')
		
		if self.email_box_type == 'imap' and not self.email_box_imap_foder:
			self.email_box_imap_folder = 'INBOX'
			
		if not self.email_box_port:
			if self.email_box_type == 'pop3':
				if self.email_box_ssl:
					self.email_box_port = 995
				else:
					self.email_box_port = 110
			elif self.email_box_type == 'imap':
				if self.email_box_ssl:
					self.email_box_port = 993
				else:
					self.email_box_port = 143
					
		super(Queue, self).save(*args, **kwargs)
		
class Ticket(models.Model):
	"""
	Tickets represent the basic problems. Each ticket can be assigned to a person, but that is not necessairy so. Unassigned tickets will always be
	displayed on the dashboard.
	"""
	
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
	title = models.CharField('title', max_length=250)
	created = models.DateTimeField('created', auto_now_add=True)
	modified = models.DateTimeField('modified', auto_now=True)
	submitter_email = models.EmailField('submitter e-mail', blank=True, null=True, help_text='The e-mail from the person who submitted the ticket. This person will receive an e-mail on every change to this ticket.')
	assigned_to = models.ForeignKey(User, related_name='assigned_to', blank=True, null=True)
	status = models.IntegerField('status', choices=STATUS_CHOICES, default=NEW_STATUS)
	on_hold = models.BooleanField('on hold', blank=True, help_text='A ticket that is on hold will not be auto escalated.')
	description = models.TextField('description', blank=True, null=True, help_text='A description of the problem.')
	resolution = models.TextField('resolution', blank=True, null=True, help_text='The resolution provided as an answer to the problem.')
	priority = models.IntegerField('priority', default=3, choices=PRIORITY_CHOICES, help_text='The priority of this ticket, 1 is the highest, 5 the lowest priority.')
	last_escalation = models.DateTimeField(blank=True, null=True, editable=False)
	
	def _get_assigned_to(self):
		"""Checks the person to which this ticket is assigned to. If it's not assigned to anybody, we return Unassigned."""
		if not self.assigned_to:
			return 'Unassigned'
		else:
			if self.assigned_to.get_full_name():
				return self.assigned_to.get_full_name()
			else:
				return self.assigned_to
	get_assigned_to = property(_get_assigned_to)
	_get_assigned_to.short_description = 'Assigned to'
	
	def _get_ticket(self):
		"""Returns a user friendly ticket ID."""
		return '[%s]'  % self.ticket_for_url
	get_ticket = property(_get_ticket)
	
	def _get_ticket_for_url(self):
		"""Returns URL friendly ticket ID."""
		return '%s - %s' % (self.queue.slug, self.id)
	ticket_for_url = property(_get_ticket_for_url)
	
	def _get_priority(self):
		"""A HTML <span> providing a CSS styled representation of the priority."""
		from django.utils.safestring import mark_safe
		return mark_safe('<span class="priority%s">%s</span>' % (self.priority, self.priority))
	get_priority = property(_get_priority)
	
	def _get_status(self):
		"""Returns the ticket status, displaying a on hold message if necessairy."""
		held_msg = ''
		if self.on_hold:
			held_msg = ' - on hold'
			
		return '%s%s' % (self.get_status_display(), held_msg)
	get_status = property(_get_status)
	
	def _get_public_url(self):
		"""Returns a ticket URL for the public."""
		pass
	get_public_url = property(_get_public_url)
	
	def _get_staff_url(self):
		"""Returns a ticket URL for staff members."""
		pass
	get_staff_url = property(_get_staff_url)
	
	def __unicode__(self):
		return self.title
	
	class Meta:
		get_latest_by = 'created'
		ordering = ['-created']
		
	@models.permalink
	def get_absolute_url(self):
		pass