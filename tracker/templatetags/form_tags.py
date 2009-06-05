from django import template

register = template.Library()

@register.inclusion_tag('templatetags/display_field.html')
def display_field(field, alt_label=''):
	"""Print HTML for a newform field. You can supply a new label which overrides the default label generated for the form."""
	
	if alt_label:
		field.label = alt_label
		
	return {'field': field}