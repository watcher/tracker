from django.template.defaultfilters import slugify
import re

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