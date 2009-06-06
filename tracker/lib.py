from django.template.defaultfilters import slugify
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.sites.models import RequestSite, Site
from django.conf import settings
import re

def response(request, template, dictionary, *args, **kwargs):
	"""Wraps the render_to_response call and make sure there is always a RequestContext passed allong."""
	kwargs['context_instance'] = RequestContext(request)
	
	dictionary['site'] = _get_site_name(request)
	
	return render_to_response(template, dictionary, *args, **kwargs)
	
def _get_site_name(request):
	"""Returns either the current site object, or else the name defined in settings.py. As a last resort it gets the name from the request object."""
	try:
		return Site.objects.get(pk=settings.SITE_ID).name
	except:
		try:
			return settings.SITE_NAME
		except:
			return RequestSite(request).name

RE_SLUG_STRIP = re.compile(r'^-+|-+$')

def unique_slugify(instance, value, slug_field_name='slug', queryset=None):
	"""
	Calculates a unique slug of ``value`` for an instance.

	``slug_field_name`` should be a string matching the name of the field to
	store the slug in (and the field to check against for uniqueness).

	``queryset`` usually doesn't need to be explicitly provided - it'll default
	to using the ``.all()`` queryset from the model's default manager.
	"""
	slug_field = instance._meta.get_field(slug_field_name)

	slug = getattr(instance, slug_field.attname)
	slug_len = slug_field.max_length

	# Sort out the initial slug. Chop its length down if we need to.
	slug = slugify(value)
	if slug_len:
		slug = slug[:slug_len]
	slug = RE_SLUG_STRIP.sub('', slug)
	original_slug = slug

	# Create a queryset, excluding the current instance.
	if not queryset:
		queryset = instance.__class__._default_manager.all()
		if instance.pk:
			queryset = queryset.exclude(pk=instance.pk)

	# Find a unique slug. If one matches, at '-2' to the end and try again
	# (then '-3', etc).
	next = 2
	while not slug or queryset.filter(**{slug_field_name: slug}):
		slug = original_slug
		end = '-%s' % next
		if slug_len and len(slug) + len(end) > slug_len:
			slug = slug[:slug_len-len(end)]
			slug = RE_SLUG_STRIP.sub('', slug)
		slug = '%s%s' % (slug, end)
		next += 1

	setattr(instance, slug_field.attname, slug)