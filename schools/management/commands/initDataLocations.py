# 1st command
from django.core.management.base import BaseCommand
from django.conf import settings
from schools.models import Library, Location, Shelf, School

import json

import os


class Command(BaseCommand):
    """Closes the specified poll for voting"""

    def handle(self, *args, **options):
        """	Initialise the Database with Libraries names,
        shelfs and shelf steps"""

        # LibraryName -->nbr of shelf

        with open(os.path.join(settings.BASE_DIR,'initLocations.json')) as f:
            Data = json.load(f)

        for data in Data:
            
            school = School.objects.get_or_create(
                name=data['SchoolName'],
                city = data['Town'],
                country = data['Country']
            )[0]

            for l in data['Data']:  # Loop Libraries
                shelfs = []
                print(l)
                for i in range(1, data['Data'][l][0]+1):  # Loop Shelfs
                    steps = []
                    for c in range(1, data['Data'][l][1]+1):  # Loop shelf steps
                        a = Location(step=c)
                        a.save()
                        steps.append(a)
                    a = Shelf.objects.create(num=i)
                    a.location.set(steps)
                    a.save()
                    shelfs.append(a)
                lib = Library.objects.create(name=l)
                lib.shelf.set(shelfs)
                school.library.add(lib)
                lib.save()
            
            school.save()
