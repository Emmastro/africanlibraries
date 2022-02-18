from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
import django.contrib

#print(django.contrib.auth.urls.)

urlpatterns = [
	path('', views.account_redirect, name='accounts'), #Reply to a comment
	path('login/', views.Login.as_view(), name='login'),
	path('registration/', views.Registration.as_view(), name='registration'),
	path('logout/', views.logout_view, name='logout'),
	path('password_change', views.LostPassword.as_view(), name='password_change'),
	path('<pk>/', views.Account.as_view(), name='accounts'), #Reply to a comment	

]
