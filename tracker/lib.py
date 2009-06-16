from django.template.defaultfilters import slugify
from django.conf import settings
from django.core.mail import EmailMessage
from django.template import loader, Context, RequestContext
from django.shorcuts import render_to_response
from django.contrib.sites.models import RequestSite, Site
import os
import re

def response(request, template, dictionary, *args, **kwargs):
	kwargs['context_instance'] = RequestContext(request)
	
	dictionary['site'] = _get_site_name(request)
	
	return render_to_response(template, dictionary, *args, **kwargs)
	
def _get_site_name(request):
	try:
		return Site.objects.get(pk=settings.SITE_ID).name
	except:
		try:
			return settings.SITE_NAME
		except:
			return RequestSite(request).name

def send_templated_email(template_name, email_context, recipients, sender=None, bcc=None, fail_silently=False, files=None):
	from tracker.models import EmailTemplate
	
	context = Context(email_context)
	
	template = EmailTemplate.objects.get(name__iexact=template_name)
	
	if not sender:
		sender = settings.DEFAULT_FROM_EMAIL
		
	text = loader.get_template_from_string(template.message).render(context)
	subject = loader.get_template_from_string("{{ ticket.get_ticket_slug }} {{ ticket.title }} %s" % template.subject).render(context)
	
	if type(recipients) != list:
		recipients = [recipients,]
		
	email = EmailMessage(subject, text, sender, recipients, bcc=bcc)
	
	if files:
		if type(files) != list:
			files = [files,]
			
		for file in files:
			email.attach_file(file)
			
	return email.send(fail_silently)

RE_SLUG_STRIP = re.compile(r'^-+|-+$')

def unique_slugify(instance, value, slug_field_name='slug', queryset=None):
	slug_field = instance._meta.get_field(slug_field_name)
	
	slug = getattr(instance, slug_field.attname)
	slug_len = slug_field.max_length
	
	slug = slugify(value)
	if slug_len:
		slug = slug[:slug_len]
	slug = RE_SLUG_STRIP.sub('', slug)
	original_slug = slug
	
	if not queryset:
		queryset = instance.__class__._default_manager.all()
		if instance.pk:
			queryset = queryset.exclude(pk=instance.pk)
	
	next = 2
	while not slug or queryset.filter(**{slug_field_name: slug}):
		slug = original_slug
		end = '-%s' % next
		if slug_len and len(slug) + len(end) > slug_len:
			slug = slug[:slug_len - len(end)]
			slug = RE_SLUG_STRIP.sub('', slug)
		slug = '%s%s' % (slug, end)
		next += 1
		
	setattr(instance, slug_field.attname, slug)