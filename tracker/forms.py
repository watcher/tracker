from django import forms
from django.conf import settings
from tracker.models import Ticket, Queue, FollowUp, Attachment

class PublicTicketForm(forms.Form):
	queue = forms.ModelChoiceField(label='Queue', queryset=Queue.objects.filter(allow_public_submission=True).filter(active=True), empty_label=None)
	title = forms.CharField(label='Summary of your issue', required=True, max_length=100)
	submitter_email = forms.EmailField(label='Your e-mail address', required=True, help_text='This e-mail address will be used to inform you of all updates made to this ticket.')
	description = forms.CharField(label='Description of your issue', required=True, widget=forms.Textarea(), help_text='Please provide as much details as possible. This will help us solve your issue much faster.')
	priority = forms.ChoiceField(label='Priority', choices=Ticket.PRIORITY_CHOICES, initial=3, help_text='Please select the priority carefully. Priorities can and will be changed by members of the staff when reviewing your issue.')
	attachment = forms.FileField(label='Attach a file', required=False, help_text='You can attach a file (like a screenshot) to clarify your issue.')
	
	def save(self):
		t = Ticket(title=self.cleaned_data['title'], submitter_email=self.cleaned_data['submitter_email'], status=Ticket.NEW_STATUS, queue=self.cleaned_data['queue'], description=self.cleaned_data['description'], priority=self.cleaned_data['priority'])
		t.save()
		
		f = FollowUp(ticket=t, title='Ticket opened via web', public=True, comment='Ticket opened via the web.')
		f.save()
		
		# files = []
		if self.cleaned_data['attachment']:
			import mimetypes
			
			file = self.cleaned_data['attachment']
			filename = file.name.replace(' ', '_')
			
			a = Attachment(followup=f, filename=filename, mime_type=mimetypes.guess_type(filename)[0] or 'application/octet-stream', size=file.size)
			a.file.save(file.name, file)
			
			# if file.size < getattr(settings, 'MAX_EMAIL_ATTACHMENT_SIZE', 1024000):
			# 	files.append(a.file.path)
			
		return t