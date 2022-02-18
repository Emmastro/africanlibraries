from django.db import models
from account.models import Reader


class Librarian(Reader):
    """
    """
    profil = models.TextField(null=True)
    role =  models.CharField(max_length = 200)

    class Meta:
        pass