from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
import django.contrib

#print(django.contrib.auth.urls.)

urlpatterns = [

	#path('startReading/', views.validate_username, name='validate_username'),
	path('validate_username/', views.validate_username, name='validate_username'),

]
