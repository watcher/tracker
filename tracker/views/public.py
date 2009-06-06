from tracker.models import Queue, Ticket
from tracker.forms import PublicTicketForm
from tracker.lib import response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def index(request):
	if request.user.is_staff:
		# this will need to redirect to the personal dashboard of the user
		pass
	
	if request.method == "POST":
		form = PublicTicketForm(request.POST, request.FILES)
		form.fields['queue'].choices = [[q.id, q.title] for q in Queue.objects.filter(allow_public_submission=True)]
		if form.is_valid():
			ticket = form.save()
			
			return HttpResponseRedirect('%s?email=%s' % (reverse('tracker-public-view-ticket', args=[ticket.queue.slug, ticket.id]), ticket.submitter_email))
		
	else:
		form = PublicTicketForm()
		form.fields['queue'].choices = [[q.id, q.title] for q in Queue.objects.filter(allow_public_submission=True)]
		
	return response(request, 'tracker/public/index.html', locals())
	
def view_ticket(request, queue, id):
	email = request.GET.get('email', '')
	error_message = ''
	
	if email:
		try:
			ticket = Ticket.objects.get(pk=id, queue__slug__iexact=queue, submitter_email__iexact=email)
		except Ticket.DoesNotExist:
			ticket = False
			error_message = 'Invalid ticket ID or e-mail address. Please try again.'
			
		if ticket:
			return response(request, 'tracker/public/view_ticket.html', locals())
	
	return response(request, 'tracker/public/404.html', locals())