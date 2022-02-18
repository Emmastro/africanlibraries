from django.db import models

from account.models import Reader, Author, Administrator

# Students can post their articles on the website
# Feed of books according to the student interest
# Multiple view of the feed
# Get the author image for a better general knowledge of the readers


class School(models.Model):
	
	name = models.CharField(max_length=100, null=True, blank=True, default=None)
	city = models.CharField(max_length=100, null=True, blank=True, default='Kinshasa')
	country = models.CharField(max_length=100, default='Democratic Republic of Congo')
	address = models.CharField(max_length=500, null=True, blank=True, default=None)
	postal_code = models.CharField(max_length=5, null=True, blank=True, default=None)

	# Books are linked to the school through the library, every schools have one library by default
	# *** the payment will be per library, and library size
	library = models.ManyToManyField('schools.Library', blank=True, default=None)
	url = models.CharField(max_length=100, null=True, blank=True, default='None')

	
	def __str__(self):
		return self.name


class Location(models.Model):
	"""
	Location id is the step of the shelf for the book
	"""
	step = models.IntegerField()

	def __str__(self):
		return 'Location {}'.format(hex(self.id))


class Publisher(models.Model):
	"""
	Description: Model Description
	"""
	name = models.CharField(max_length = 200,  null=True, blank=True, default=None)

	def __str__(self):
		return self.name

class Language(models.Model):
	""" Initialise with a list of languages """

	name = models.CharField(max_length = 200,  null=True, blank=True, default=None)

	def __str__(self):
		return self.name


class BookAbstract(models.Model):
	"""
	Description: For reading in the school library
	"""

	title = models.CharField(max_length = 100)
	subtitle = models.CharField(max_length = 200, null=True, blank=True)
	author = models.ManyToManyField('account.Author')
	
	published_date = models.DateField(null = True)
	# *** Optimisation by creating a separate table with one-on-one relation
	published_date_type = models.CharField(max_length=20 ,null=True, blank=True)
	publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True, blank=True)
	
	page_count=models.IntegerField( null=True, blank=True, default=None)
	
	imageCover = models.ImageField(upload_to="covers", 
		verbose_name="Book Cover", null=True, blank=True, default=None)
	previewLink=models.CharField(max_length = 200,  null=True, blank=True, default=None)
	# Book id from google book
	id_google_book = models.CharField(max_length=50,  null=True, blank=True, default=None)
	
	language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=True)
	
	ISBN_10 = models.CharField(max_length = 10,  null=True, blank=True, default=None)
	ISBN_13 = models.CharField(max_length = 13,  null=True, blank=True, default=None)

	category = models.ManyToManyField('schools.Category')
	description = models.TextField(null=True, blank=True, default=None)

	#eBooks attributes
	document = models.FileField(upload_to='eBooks',  null=True, blank=True, default=None)
	upload_time = models.DateTimeField(auto_now_add=True, null=True,blank=True)


	def __str__(self):

		return self.title

	def get_readings(self):
		""" Get the readings for all schools """
		return Reading.objects.filter(book__id = self.id)

	def likes(self):
		"""
			Return the likes of the book for the current school
		"""
		return Book.objects.filter(
			reading__book__id = self.id, reading__like=1, ).count()

	def nbr_read(self):
		"""
			Return the number of users that read the book
		"""
		
		return 5#Book.objects.filter(reading__book__id = self.id)

	def get_category(self):
		""" Return the all default book category """

		return self.category.all()

	def get_authors(self):
	
		return Author.objects.filter(bookabstract__id=self.id)

class Book(models.Model):
	"""
	A book attached to a specific school
		- Specify all attributes that depends to the school specifications
		- The attribute 'data' retain all fixed informations with for the book. 
		A base model of the book is stocked in AbstractBook and all dynamic data are in the 'Book' model. 
		The same book 'Item' have it fixed data in AbstractBook, and all the School related data linked 
		to it from the 'Book' model 
	"""

	data = models.ForeignKey(BookAbstract, on_delete=models.CASCADE, help_text='Book data')
	comments = models.ManyToManyField('schools.Comment', blank=True)

	number=models.IntegerField(default=1)

	# Differentiate books among schools
	location = models.ForeignKey(Location, on_delete=models.CASCADE, help_text='Book Location in the library')	

	approval = models.BooleanField(default=False, help_text='Approval to display the book')


	def __str__(self):

		return self.data.title

	def title_slug(self):

		return self.data.title.replace(' ', '-')
	def nbr_like(self):
		""" """
		return Book.objects.filter(reading__book__id = self.id, reading__like=1).count()

	def nbr_read(self):
		""" """
		return 0#Reading.objects.filter(book__id = self.id).count()

	def get_comments(self):
		""" """
		return self.comments.all()

	def my_reading(self):
		""" """
		if Reading.objects.filter(book__id=self.id, done=0):
			return True
		else:
			return False
	
	def image_url(self):
		""" """

		if self.data.imageCover and hasattr(self.data.imageCover, "url"):
			return self.data.imageCover.url

	
	def get_library(self):
		"""
			Books in the school library
			Return Id of the shelf, group and Library of the book
		"""
		return Library.objects.get(shelf__location__id= self.location.id).name

	def get_shelf(self):
		"""
			Books in the school library
		"""
		return Shelf.objects.filter(location = self.location)[0].num
		
	def get_step(self):
		"""
			Books in the school library
		"""
		return self.location

	def status(self, user):
		"""
			0 --> The book is free for reading : Read
			1 --> The book is read by the user : End reading
			2 --> The book is read by another user : Request reading
		"""
	
		reading = Reading.objects.filter(book__id=self.id, done=False)
		n=reading.count()
		if n==0: # No one is reading the book
			return 0
		
		else: # the book is read by someone

			if Reader.objects.filter(reading__id=reading[0].id,
				id=user.id).count()>0:
				# The user is actually reading the book
				
				return 1
			else: # The book is being read by someone else
				
				return 2	

class Comment(models.Model):
	"""
	- Reply for a comment of another person's reading comment 
	"""

	text = models.TextField(null=True, blank=True)

	writer = models.ForeignKey('account.Reader', on_delete = models.CASCADE)

	# Other readers can reply to the comment
	reply = models.ManyToManyField('self', blank=True) 

	date = models.DateField(auto_now=True)

	def __str__(self):
		
		return self.text[:10] + " ... {}".format(self.pk)
	#Add reactions about the comment
	#**Likes 

class Category(models.Model):
	""" Book category affected by the reader or the librarian 
	All public categories are suggested to be on the student profil
	Which will help to create a custumized suggestion

	The private categories will not be suggested to the overall 
	system, but capte to organise the persol student books
	"""

	name = models.CharField(max_length=100)	
	statut = models.CharField(max_length=50, default="Public") #  Private or public

	def __str__(self):
		if self.name:
			return self.name
		else:
			return 'Unknown'

class Reading(models.Model):
	"""
		A reader can read the same book many times
	"""
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	start_date = models.DateField(auto_now=True)
	end_date = models.DateField(null=True, blank=True)
	like = models.SmallIntegerField(null=True, blank=True)
	# Check if the reading is done
	done = models.BooleanField(default=False)

	
	def __str__(self):
		return self.book.data.title + ' ' + str(self.book.id)

	def get_reader(self):
		
		return Reader.objects.get(reading__id = self.id)

class Shelf(models.Model):
	""" """	
	location = models.ManyToManyField(Location)
	num = models.SmallIntegerField()

	def __str__(self):
		return "Shelf {}".format(self.id) 

class Library(models.Model):

	name = models.CharField(max_length=100)
	image = models.ImageField(upload_to="Library", verbose_name="Library Image")
	shelf = models.ManyToManyField(Shelf) # The shelf contains the steps

	def __str__(self):
		return self.name

	@property
	def image_url(self):
		
		if self.image and hasattr(self.image, "url"):
			return self.image.url