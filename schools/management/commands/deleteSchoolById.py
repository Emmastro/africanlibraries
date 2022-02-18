from schools.models import School

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Closes the specified poll for voting"""
    def add_arguments(self, parser):

        parser.add_argument('pk', type=int)

    def handle(self, *args, **options):
        """
        Import the books database from an Excel file and a cover folder
        """
        pk = options['pk'] 
        school = School.objects.get(id=pk)
        school.delete()