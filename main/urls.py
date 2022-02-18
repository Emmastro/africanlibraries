from django.urls import path
from . import views


urlpatterns = [
	path('', views.home, name='home_portail'),
	path('get-school', views.get_school, name='find_school')
	
]
