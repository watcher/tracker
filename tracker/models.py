from django.db import models

class Queue(models.Model):
	"""
	A queue is a collection of ticket into what could be a certain area, project or product (e.g. Support, Bug, ...).
	
	Queues contain all information related to that area and could allow the creation of new tickets in it from email.
	"""
	
	title = models.CharField('title', max_length=250)
	slug = models.SlugField('slug', help_text='A unique name for this queue. If empty this is generated from the title.')
	email_address = models.EmailField('e-mail address', blank=True, null=True, help_text='All outgoing e-mails for this queue will be sent from this address. If you plan on importing e-mails from a POP3 or IMAP mailbox, the e-mails will be imported from this e-mailaddress.')
	allow_public_submission = models.BooleanField('allow public submission?', default=True, blank=True, help_text='Allow tickets from non logged-in users?')
	allow_email_submission = models.BooleanField('allow e-mail submission?', default=False, blank=True, help_text='Allow the creation of tickets from e-mails?')
	active = models.BooleanField('active?', default=True, blank=True, help_text='Is this queue active? An inactive queue is visible but does not allow the creation of new tickets.')
	escalate_days = models.IntegerField('escalation days', blank=True, default=0, null=True, help_text='The number of days before a ticket is auto escalated to a higher priority. This only applies to tickets that are currently not on hold. Set to 0 to disable auto escaltion.')
	new_ticket_cc = models.EmailField('new ticket CC address', blank=True, null=True, help_text='An e-mail address to receive notificiation of any new tickets being created in this queue.')
	
	email_box_type = models.CharField('e-mail box type', max_length=5, choices=(('imap', 'IMAP'), ('pop3', 'POP3')), blank=True, null=True, help_text='E-mail server type for the mailbox used in auto ticket creation from e-mail.')
	email_box_host = models.CharField('e-mail box host', max_length=250, blank=True, null=True, help_text='E-mail server host for the mailbox used in auto ticket creation from e-mail.')
	email_box_port = models.IntegerField('e-mail box port', blank=True, null=True, help_text='E-mail server port for the mailbox used in auto ticket creation from e-mail. Default ports are 110 for POP3 and 143 for IMAP. Leave blank to use defaults.')
	email_box_sll = models.BooleanField('use SSL for e-mail?', default=False, blank=True, help_text='Use SSL for connection to the e-mail server? Default ports are 995 for POP3 and 993 for IMAP when using SSL.')
	email_box_user = models.CharField('e-mail username', max_length=200, blank=True, null=True, help_text='The username used for the connection to the mailbox.')
	email_box_password = models.CharField('e-mail password', max_length=200, blank=True, null=True, help_text='The password used for the connection to the mailbox.')
	email_box_imap_folder = models.CharField('IMAP folder', max_length=100, blank=True, null=True, help_text='When connection to an IMAP server, the name of the mail folder to process email from. Default is INBOX.')
	email_box_interval = models.IntegerField('e-mail check interval', blank=True, null=True, default=5, help_text='How often does this mailbox need to be checked (in minutes)?')
	email_box_last_checked = models.DateTimeField('last check', blank=True, null=True, editable=False)