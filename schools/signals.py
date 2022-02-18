from account.models import Reader
from django.core.signals import request_started 
from django.dispatch import receiver


@receiver(request_started, sender=Reader)
def count_connection(sender, environ, **kwargs):
	pass

    