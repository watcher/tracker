from django import forms
from models import Ticket, Queue, FollowUp, Attachment
from django.conf import settings

class PublicTicketForm(forms.Form):
	queue = forms.ChoiceField(label='Queue', required=True, choices=())
	title = forms.CharField(label='Summary of your issue', required=True, max_length=100, widget=forms.TextInput())
	submitter_email = forms.EmailField(required=True, label='Your e-mail address', help_text='We will use this e-mail to keep you informed of all updates to this ticket.')
	body = forms.CharField(label='Description of your issue', widget=forms.Textarea(), required=True, help_text='Please provide as much details as possible to help us solve your issue.')
	priority = forms.ChoiceField(label='Priority', choices=Ticket.PRIORITY_CHOICES, initial=3, help_text='Please select a priority carefully, this will be changed by a member of staff if too high or low.')
	attachment = forms.FileField(required=False, label='Attach file', help_text='You can attach a file such as a document or screenshot to this ticket.')
	
	def save(self):
		q = Queue.objects.get(id=int(self.cleaned_data['queue']))
		
		t = Ticket(title=self.cleaned_data['title'], submitter_email=self.cleaned_data['submitter_email'], status=Ticket.NEW_STATUS, queue=q, description=self.cleaned_data['body'], priority=self.cleaned_data['priority'])
		t.save()
		
		f = FollowUp(ticket=t, title='Ticket opened via web', public=True, comment=self.cleaned_data['body'])
		f.save()
		
		files = []
		if self.cleaned_data['attachment']:
			import mimetypes
			
			file = self.cleaned_data['attachment']
			filename = file.name.replace(' ', '_')
			a = Attachment(followup=f, filename=filename, mime_type=mimetypes.guess_type(filename)[0] or 'application/octet-stream', size=file.size)
			a.file.save(file.name, file, save=False)
			a.save()
			
			if file.size < getattr(settings, 'MAX_EMAIL_ATTACHMENT_SIZE', 512000):
				# Only files smaller thant 512 kb, or smaller than the MAX_EMAIL_ATTACHMENT_SIZE, are sent via email.
				files.append(a.file.path)
		
		if q.new_ticket_cc:
			# here should be some code to fire of an e-mail to the new_ticket_cc address informing them of the new ticket.
			pass
			
		return t