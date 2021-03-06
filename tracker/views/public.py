from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from tracker.lib import response
from tracker.forms import PublicTicketForm, FollowUpForm
from tracker.models import Ticket, Queue

def index(request):
	if request.method == "POST":
		form = PublicTicketForm(request.POST, request.FILES)
		
		if form.is_valid():
			ticket = form.save()
			
			return HttpResponseRedirect('%s?email=%s' % (reverse('tracker-public-view-ticket', args=[ticket.queue.slug, ticket.id]), ticket.submitter_email))
			
	else:
		form = PublicTicketForm()
	
	return response(request, 'tracker/public/index.html', {'form': form})
	
def view_ticket(request, queue, id):
	try:
		ticket = Ticket.objects.get(pk=id, queue__slug__iexact=queue)
	except Ticket.DoesNotExist:
		ticket = None
		
		
	if ticket is not None:
		if not request.GET.get('email', '') == ticket.submitter_email:
			if ticket.status == Ticket.NEW_STATUS:
				error = 'This ticket has not yet been reviewed by a member of staff and can only be viewed by a member of staff or the original submitter of the ticket. If you are the original submitter of the ticket and would like to view this ticket, please check your mailbox to find your personal link to access this ticket.'
				return response(request, 'tracker/public/error.html', {'error': error})
				
			if not ticket.public:
				error = 'This ticket has been made non-public by a member of staff. This could be because this ticket either contains confidential information or because the person who submitted the ticket requested it. If you are the person who submitted this ticket, please check your mailbox to find your personal link to access this ticket.'
				return response(request, 'tracker/public/error.html', {'error': error})
			
		if request.method == 'POST' and ticket.is_public:
			form = FollowUpForm(request.POST, request.FILES)
			
			if form.is_valid():
				t = form.save()
				
				return HttpResponseRedirect('%s' % (reverse('tracker-public-view-ticket', args=[t.queue.slug, t.id])))
		else:
			form = FollowUpForm(initial={'ticket': ticket.id})
		
		return response(request, 'tracker/public/view_ticket.html', {'ticket': ticket, 'form': form})
	
	else:
		error = 'The requested ticket can not be found in our database. Please check your URL and try again.'
		return response(request, 'tracker/public/error.html', {'error': error})
		
def find_ticket(request):
	if request.method == "POST":
		id = request.POST.get('id', 0)
		if id == '':
			id = 0
		
		email = request.POST.get('email', '')
		
		try:
			ticket = Ticket.objects.get(pk=id, submitter_email__iexact=email)
		except Ticket.DoesNotExist:
			error = 'The ID and / or email you entered where not correct. Please check and try again.'
			
			return response(request, 'tracker/public/find_ticket.html', {'error': error, 'post': request.POST})
		
		return HttpResponseRedirect('%s?email=%s' % (reverse('tracker-public-view-ticket', args=[ticket.queue.slug, ticket.id]), ticket.submitter_email))
	else:
		return response(request, 'tracker/public/find_ticket.html', {})
		
def browse_tickets(request):
	tickets = []
	
	for q in Queue.objects.all():
		tickets.append({'queue': q, 'tickets': q.ticket_set.filter(public=True).filter(status__gt=Ticket.NEW_STATUS).filter(status__lt=Ticket.CLOSED_STATUS)})
		
	return response(request, 'tracker/public/browse_tickets.html', {'tickets': tickets})