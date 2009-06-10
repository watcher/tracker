from django.db import models

class FollowUpManager(models.Manager):
	def private_followups(self):
		return self.filter(public=False)
		
	def public_followups(self):
		return self.filter(public=True)