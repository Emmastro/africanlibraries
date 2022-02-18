from django.urls import path
from . import views


urlpatterns = [
	#path('', views.home, name='home'),

	path('', views.Home.as_view(), name='home'),
		
	path('categories/<category>', views.Category.as_view(), name='category'),
	path('books/<pk>', views.BookDetail.as_view(), name='book_detail'),
	
	path('search', views.SearchView.as_view(), name='search'),
	
	path('authors/', views.Authors.as_view(), name='authors'),
	
	path('settings/', views.Settings.as_view(), name='settings'),
	path('help/', views.Help.as_view(), name='help'),
	
	path('authors/<pk>', views.Author.as_view(), name='author_detail'),

	path('readings', views.Readings.as_view(), name='readings'),
	
	path('addbook/', views.Addbook.as_view(), name='addbook'),
	
	path('comment/', views.comment, name='comment'), # Add a new comment on a book

	path('admin/', views.Admin.as_view(), name='admin_lib'),

]
