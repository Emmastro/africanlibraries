from schools.models import*
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Closes the specified poll for voting"""
    
    def handle(self, *args, **options):
        """
        Import the books database from an Excel file and a cover folder
        """
        books = Book.objects.all()
        for b in books:
            print('Deleting {}'.format(b.title))
            b.delete()