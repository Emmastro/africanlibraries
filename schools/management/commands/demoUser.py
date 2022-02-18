from django.core.management.base import BaseCommand
from account.models import Reader
from schools.models import School


class Command(BaseCommand):
    """Closes the specified poll for voting"""

    def handle(self, *args, **options):
        """"""
        for l in range(2):

            for i in range(10):
                
                reader = Reader(username='Demo{}{}'.format(i,l), school=School.objects.get(pk=l+1))
                
                reader.set_password("Demo")

                reader.save()