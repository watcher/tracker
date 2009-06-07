from django.db import models
from tracker.lib import unique_slugify

class Queue(models.Model):
	title = models.CharField('Title', max_length=250)
	slug = models.SlugField('Slug', blank=True)
	email_address = models.EmailField('E-Mail address')
	allow_public_submission = models.BooleanField('Allow the submission of tickets from non-logged in users?', default=True)
	active = models.BooleanField('Active queue?', default=True)
	escalate_days = models.IntegerField('Escalation days', default=0, blank=True)
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