"""
2nd Command
Import Book Version 2 for all book details
Import books from the excel database, filling missing information 
with the Google Book service using the API

"""
import os

import pandas as pd

from schools.models import*
from account.models import Author

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from django.core.files.base import ContentFile
from PIL import Image

from io import BytesIO

import datetime
class Command(BaseCommand):
    """Closes the specified poll for voting"""
    def add_arguments(self, parser):
        parser.add_argument('excelDB', type=str)
        parser.add_argument('coversDB', type=str)
        parser.add_argument('index_start', type=int)
        parser.add_argument('index_end', type=int)
        parser.add_argument('SchoolIndex', type=int)

    def handle(self, *args, **options):
        """
        Import the books data from an Excel file and a cover folder
        The index is the nomber of books to import
        """
        index_start = options['index_start'] 
        index_end = options['index_end']
        schoolIndex = options['SchoolIndex']
        data = pd.read_excel(options['excelDB'])

        data.loc[:, ['Category', 'Publisher', 'Authors', 'Description', 'Subtitle']] = data.loc[:, ['Category', 'Publisher', 'Authors', 'Description', 'Subtitle']].fillna('')
        data.loc[:, ['PublishedDate', 'PageCount']] = data.loc[:, ['PublishedDate', 'PageCount']].fillna(0)   
        data.loc[:, 'Number'] = data.loc[:, 'Number'].fillna(value=1)
        
        covers = os.listdir(options['coversDB'])[index_start:index_end]
        
        
        covers_name = []
        covers_ext = []

        # *************************************************************
        # Replace by cover downloads
        for l in covers:
            n=l.split('.')
            covers_name.append(n[0])
            covers_ext.append(n[1])
        # *************************************************************

        # Try creating unknown author if it's the first import
        Author.objects.get_or_create(username='Unknown')

        # Import Publishers
        for i,publisher in enumerate(data['Publisher'][index_start:index_end]):
            
            if publisher!='Unknown':
                Publisher.objects.get_or_create(name=n)

        # Try creating unknown publisher if it's the first import
        Publisher.objects.get_or_create(name = "Unknown")


        print("Go over books in the Excel sheet and save all entries")
        for i in range(index_start,index_end):

            # Locations are already created from the commange 'initlocation'
            location = Location.objects.get(
                step=data['Shelf_step'][i],
                shelf__num=data['Shelf'][i],
                shelf__library__name=data['Library'][i],
                shelf__library__school = School.objects.get(pk = schoolIndex)
                )
            
            # If the publication date is only a year, an year attribute is added
            published_date = data['PublishedDate'][i]
            
            if published_date==0: # No Data 
                published_date = None

            elif type(published_date)==type(0):
                y,m,d = published_date,6,12
                published_date = datetime.date(int(y),int(m),int(d))
            
            elif len(published_date.strip())==7:
                y,m = published_date.strip().split('-')
                published_date = datetime.date(int(y),int(m), 12)
            
            elif len(published_date.strip())==10:
                y,m,d = published_date.strip().split('-')
                published_date = datetime.date(int(y),int(m),int(d))


            bookData = BookAbstract.objects.get_or_create(
                title = data['Title'][i],
                subtitle = data['Subtitle'][i],
                description = data['Description'][i],
                page_count= int(data['PageCount'][i]),
                )

            if bookData[1]:
                
                categories = data['Category'][i].split(',')
    
                for category in categories:
                    category_obj = Category.objects.get_or_create(name=category, statut='public')
                    bookData[0].category.add(category_obj[0])

                authors = data['Authors'][i].split(',')
                
                for auth in authors:

                    author = Author.objects.get_or_create(username=auth)

                    bookData[0].author.add(author[0]) # 1st value from get_or_create is the object, the 2nd value is a bollean

                # ---Process publisher creation or affectation--- 

                publisher_data = data['Publisher'][i].strip()            
                
                if publisher_data!='Unknown':
                    
                    publisher = Publisher.objects.get_or_create(name=publisher_data)
                    bookData[0].publisher = publisher[0]
                else:
                    # Affect an Unknown author
                    bookData[0].publisher = Publisher.objects.get(name='Unknown')

                # Affect cover images
                try:
                    fileName = str(i+1) + '.' + covers_ext[i]
                    cover = Image.open(
                        options['coversDB']+'/'+fileName)
                    cover.resize((200,200))
                    img = BytesIO()
                    cover.save(img, cover.format)
                    bookData[0].imageCover.save(
                        fileName, 
                        ContentFile(img.getvalue()), save=True)

                except Exception as e:
                    pass #No cover to display       
            
            book = Book.objects.create(
                number=int(data['Number'][i]),
                data = bookData[0],
                location=location,
                )

            book.save()