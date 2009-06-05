from tracker.models import Queue, Ticket
from tracker.forms import PublicTicketForm
from tracker.lib import response

def index(request):
	if request.user.is_staff:
		# this will need to redirect to the personal dashboard of the user
		pass
	
	if request.method == "POST":
		# saving and creating the new ticket
		pass
	else:
		form = PublicTicketForm()
		form.fields['queue'].choices = [[q.id, q.title] for q in Queue.objects.filter(allow_public_submission=True)]
		
		return response(request, 'tracker/public/index.html', locals())