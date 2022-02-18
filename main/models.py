from django.db import models

from account.models import Reader


class SchoolAdmin(Reader):
	"""
	Description: Model Description
	"""
    
	payement = models.ManyToManyField('main.Payment')

class Payment(models.Model):
    """
    Description: Model Description
    """
    date = models.DateField(auto_now=True)
    amount = models.SmallIntegerField(null=True)

