import os
 
import pandas as pd

from schools.models import*

from django.core.management.base import BaseCommand

from django.core.files.base import ContentFile
from PIL import Image

from io import BytesIO

class Command(BaseCommand):
    """Closes the specified poll for voting"""
    def add_arguments(self, parser):
        parser.add_argument('excelDB', type=str)
        parser.add_argument('coversDB', type=str)
        parser.add_argument('index_start', type=int)
        parser.add_argument('index_end', type=int)

    def handle(self, *args, **options):
        """
        Import the books data from an Excel file and a cover folder
        The index is the nomber of books to import
        """
        index_start = options['index_start'] 
        index_end = options['index_end']

        data = pd.read_excel(options['excelDB'])

        data.fillna(value='', inplace=True)
        
        #Get the precised number of books to import
        covers = os.listdir(options['coversDB'])[index_start:index_end]
        
        covers_name = []
        covers_ext = []

        for l in covers:
            n=l.split('.')
            covers_name.append(n[0])
            covers_ext.append(n[1])

        #Import Authors
        for i,l in enumerate(data['Author'][index_start:index_end]):
            
            if l!='Unknown':
                for n in l.split(','):
                    try:
                        Author.objects.get(name=n)
                    except:
                        Author.objects.create(name=n).save()
        #Import Books

        Author(name = "Unknown").save() # ***Put in Default
        for i in range(index_start,index_end):
            print(data['Title'][i])
            location = Location.objects.get(
                step=data['Shelf_step'][i],
                shelf__num=data['Shelf'][i],
                shelf__library__name=data['Library'][i])

            book = Book.objects.create(
                title=data['Title'][i],
                subtitle=data['Subtitle'][i],
                description =data['Description'][i],
                number=int(data['Number'][i]),
                loc=location,
                )
            authors = data['Author'][i].split(',')
            for a in authors:
                try:
                    author = Author.objects.get(name=a)
                    book.author.add(author)
                except:
                    pass
            try:
                fileName = str(i+1) + '.' + covers_ext[i]
                cover = Image.open(
                    options['coversDB']+'/'+fileName)
                cover.resize((200,200))
                img = BytesIO()
                cover.save(img, cover.format)
                book.imageCover.save(
                    fileName, 
                    ContentFile(img.getvalue()), save=False)
            except Exception as e:
                raise Exception(e)
                pass #No cover to display     
            
            book.save()