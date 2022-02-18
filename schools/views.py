from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic import ListView, DetailView
from django.views import View
from django.core.mail import send_mail
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.utils.decorators import method_decorator

from .models import*

from account.models import Reader

import datetime 


@method_decorator(login_required, name='dispatch')
class Home(ListView):

	model = Book
	template_name = "home.html"
	context_object_name = "books"
	paginate_by = 8

	def get_queryset(self):
		"""Filter to get for only the user's school"""
		schoolId = Reader.objects.get(pk=self.request.user.id).school.id
		return self.model.objects.filter(location__shelf__library__school__pk=schoolId)

	
	def get(self, request, *args, **kwargs):
		
		books = Book.objects.all()
		#** Give real data to fit the categories
		continue_reading = books[0:8]
		book_suggestions = books[8:16]
		book_popular = books[16:32]

		book_categories = [
			("Continue Reading", continue_reading),
			("Suggested for you", book_suggestions),
			("Most popular", book_popular)
		]
	
		return render(request, self.template_name, locals())

@method_decorator(login_required, name='dispatch')	
class Readings(ListView):
	template_name = "readings.html"
	model = Reading
	context_object_name = 'readings'
	paginate_by = 20
	
	def get_queryset(self):

		readings = Book.objects.filter(reading__reader__id=self.request.user.id)
		print(readings)
		return readings
	
class SearchView(ListView):

	template_name = 'search_result.html'
	context_object_name = 'books'
	paginate_by = 20



	def get_queryset(self):

		vector = SearchVector('data__title', 'data__subtitle', 'data__description','data__author__username')
		query = SearchQuery(self.request.GET['key'])

		books = Book.objects.annotate(
			rank=SearchRank(vector, query)).order_by('-rank')
		books = list(dict.fromkeys([r for r in books if r.rank > 0]))

		return books

	def get_context_data(self, **kwargs):
		
		context = super(SearchView, self).get_context_data(**kwargs)

		context['key'] = self.request.GET['key'] 

		return context
	

@method_decorator(login_required, name='dispatch')
class BookDetail(DetailView):
	"""docstring for Read_view"""
	
	model = Book
	template_name = "book_detail.html"
	context_object_name = "book"

	def get(self, request, *args, **kwargs):
		
		obj_key = self.kwargs.get('pk')
		book = self.model.objects.get(pk=obj_key)
		
		return render(request, self.template_name, locals())


	
	def post(self, request,  *args, **kwargs):
		
		print("post request")
		book = Book.objects.get(pk=request.POST['book'])
		status = book.status(request.user)
		print("Status: ", status)
		if status==0:

			reading = Reading.objects.create(
				start_date=datetime.date.today(), book=book, done=0)
			reading.save()
			a = Reader.objects.get(id=request.user.id)
			a.reading.add(reading)
			a.save()

			print("Reading start")


		elif status==1:

			#** Check if the book has been read: min 30min and other hacking scenario
			if True:
					
				reading = Reading.objects.get(book=book, reader__id=request.user.id, done=0)
				reading.done = 1
				reading.end_date = datetime.date.today()
				#reader = Reader.objects.get(id=request.user.id)
				reading.book.save()
				reading.save()
				print("Reading done")

		elif status==2:
			# Send an email notification

			send_mail("Request Reading",
			"""Dear {},
			You have requested reading the book {}.
			You will be soon notified when to get the book.

			Regards,
			Librarians Team""".format(request.user, book), settings.DEFAULT_FROM_EMAIL,
			recipient_list = [request.user.email])
					
		return render(request, self.template_name, locals())


class Settings(View):

	template_name = "settings.html"
	
	def get(self, request, *args, **kwargs):

		return render(request, self.template_name, locals())

class Help(View):

	template_name = "help.html"
	
	def get(self, request, *args, **kwargs):

		return render(request, self.template_name, locals())


@method_decorator(login_required, name='dispatch')
class Authors(ListView):

	model = Author

	template_name = "OurBooks.html"
	context_object_name = "authors"
	paginate_by = 50

	def get_queryset(self):
		"""Filter to get for only the user's school"""
		schoolId = Reader.objects.get(pk=self.request.user.id).school.id
		return self.model.objects.filter(location__shelf__library__school__pk=schoolId)

	def get_context_data(self, **kwargs):
		
		context = super(Home_view, self).get_context_data(**kwargs)

		reader = Reader.objects.get(id=self.request.user.id)
		context['suggested'] = Book.objects.filter(
			data__category__in = reader.category_preference.all()
			)
		#context['most_liked'] = Book.objects.order_by('')

		#context['most_read'] = Book.objects.filter(
		#	data__category__in = reader.category_preference.all()
		#	)

		return context

@method_decorator(login_required, name='dispatch')
class Author(DetailView):

	model = Author

	template_name = "OurBooks.html"
	context_object_name = "books"
	paginate_by = 50

	def get_queryset(self):
		"""Filter to get for only the user's school"""
		schoolId = Reader.objects.get(pk=self.request.user.id).school.id
		return self.model.objects.filter(location__shelf__library__school__pk=schoolId)

	def get_context_data(self, **kwargs):
		
		context = super(Home_view, self).get_context_data(**kwargs)
		
		context['research'] = True

		reader = Reader.objects.get(id=self.request.user.id)
		context['suggested'] = Book.objects.filter(
			data__category__in = reader.category_preference.all()
			)

		return context


@method_decorator(login_required, name='dispatch')
class Category(ListView):

	model = Category

	template_name = "OurBooks.html"
	context_object_name = "books"
	paginate_by = 50

	def get_queryset(self):
		"""Filter to get for only the user's school"""
		schoolId = Reader.objects.get(pk=self.request.user.id).school.id
		return self.model.objects.filter(location__shelf__library__school__pk=schoolId)

	def get_context_data(self, **kwargs):
		
		context = super(Books_view, self).get_context_data(**kwargs)
		context['page_title'] = "Our Books"
		context['research'] = True

		reader = Reader.objects.get(id=self.request.user.id)
		context['suggested'] = Book.objects.filter(
			data__category__in = reader.category_preference.all()
			)
		
		return context


@method_decorator(login_required, name='dispatch')
class Addbook(View):
	"""Add books for the librarians and students"""
	def __init__(self, *args, **kwargs):
		super(Addbook, self).__init__(*args, **kwargs)
		self.template_name = "Addbook.html"
		self.context_object_name = 'book'
		self.form_class = AddBookForm
		#self.model = Book

	def get_context_data(self, **kwargs):
		
		context = super().get_context_data(**kwargs)
		context['page_title'] = "Add a book"
		return context


	def get(self, request):
		form = self.form_class
		
		#form.fields = form.base_fields
		page_title = "Add a book"
		libs = Library.objects.all()

		return render(request, self.template_name, locals())

	def post(self, request):

		form = self.form_class(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			
		page_title = "Add a book"
		statut = "Book added"


		return render(request, self.template_name, locals())


def comment(request):
	""" Add a new comment on a book"""
	
	comment = request.POST['comment-text']
	book_id = request.POST['book-id']

	book = Book.objects.get(id = book_id)

	writer = Reader.objects.get(id = request.user.id)
	comment = Comment.objects.create(text = comment, writer = writer)
	
	try: # Try to save as a reply
		replyTo_id = request.POST['reply-to']
		replyTo = Comment.objects.get(id = replyTo_id)
		comment.reply.add(replyTo)
	except Exception as e:
		# Not a reply 
		pass

	comment.save()
	book.comments.add(comment)
	book.save()
	#return redirect('book_detail', book_id)


""" Admin views"""

# Admin views

@method_decorator(login_required, name='dispatch')
class Admin(View):
    """ Display Graphs and few features to start managing the library"""
    model = Book
    template_name = "admin_lib.html"

    def get(self, request):
    	
    	return render(request, self.template_name, locals())
