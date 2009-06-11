from django.core.mail import send_mail
from tracker.lib import send_templated_email

def new_ticket(sender, **kwargs):
	if kwargs['created']:
		t = kwargs['instance']
		
		context = {
			'ticket': t,
			'queue': t.queue,
		}
		
		if t.queue.new_ticket_cc:
			send_templated_email('new_ticket_cc', context, recipients=t.queue.new_ticket_cc, sender=t.queue.email_address, fail_silently=True)
			
		if t.submitter_email:
			send_templated_email('new_ticket_owner', context, recipients=t.submitter_email, sender=t.queue.email_address, fail_silently=True)
			
def new_followup(sender, **kwargs):
	if kwargs['created']:
		f = kwargs['instance']
		
		context = {
			'ticket': f.ticket
			'queue': f.ticket.queue,
		}
		
		if f.submitter_email:
			send_templated_email('new_followup', context, recipients=t.submitter_email, sender=t.queue.email_address, fail_silently=True)