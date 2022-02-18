from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
	path('', views.profiles, name='profiles'),
	path('<username>', views.profile, name="profileDetail") # Rename the url
]

