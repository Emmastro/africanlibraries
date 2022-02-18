from django.db import models

# Create your models here.

class WeeklyMail(models.Model):

	date = models.DateField()

	def __str__(self):
		return self.date

