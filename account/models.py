from django.db import models

from django.urls import reverse

from django.contrib.auth.models import User


class Reader(User):
	"""
	A reader is any school member that can have access to the library for
	reading purpose
	"""
	# Reader's school
	school = models.ForeignKey('schools.School',
	 on_delete=models.CASCADE)
	
	#Get the reader image for a better interaction with other readers
	image = models.ImageField(upload_to="Reader_Profile",
		verbose_name="Profil Image", null=True, blank=True)

	#Save all the reader's reading for creating an history and customize the book suggestions
	reading = models.ManyToManyField('schools.Reading',
		blank=True)
	
	book_registered = models.ManyToManyField('schools.Book', blank=True)

	# Save the reader preference of a customized reading suggestions

	category_preference = models.ManyToManyField('schools.Category', blank=True)
	author_preference = models.ManyToManyField('account.Author', blank=True)

	def image_url(self):
		"""
		"""
		if self.image and hasattr(self.image, "url"):
			return self.image.url

	def get_absolute_url(self):

		return reverse('accounts', kwargs={'pk': self.pk})

	class Meta(object):
		"""docstring for Meta"""
		verbose_name = 'Reader'
        #verbose_name_plural = _('Reader')

		
class Author(User):
	"""
	Author for an eBook on the website (for online reading/download or sale)
	"""

	#Get the reader image for a better interaction with other readers
	image = models.ImageField(upload_to="Reader_Profile",
		verbose_name="Profil Image", null=True, blank=True)

	bio = models.TextField(null=True)
	

	def image_url(self):
		
		if self.image and hasattr(self.image, "url"):
			return self.image.url

	class Meta(object):
		"""docstring for Meta"""
		verbose_name = 'Author'



class Administrator(User):
	""" Admin Account for the school library.
	Affectations: - Register the school
				  - Can Register all students 
				  - Access to the full school dashboard 
				  - Pay for the service
	"""


	school = models.ForeignKey('schools.School',
	 on_delete=models.CASCADE,  null=True, blank=True)
	
	#Get the reader image for a better interaction with other readers
	image = models.ImageField(upload_to="Reader_Profile",
		verbose_name="Profil Image", null=True, blank=True)
	
	# Payment methodes
	creditCardNumber = models.IntegerField( null=True, blank=True)
	
	def image_url(self):
		"""
		"""
		if self.image and hasattr(self.image, "url"):
			return self.image.url

	def get_absolute_url(self):

		return reverse('accounts', kwargs={'pk': self.pk})

	class Meta(object):
		"""docstring for Meta"""
		verbose_name = 'Administrator'
		#verbose_name_plural = _('Reader')

