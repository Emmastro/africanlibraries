from django.shortcuts import render,  redirect
from schools.Objects import *
from .models import Librarian

def profiles(request):
	return redirect('home')

def profile(request, username):
	page_title = "Our librarians | Details"
	lst_menu = Menus(0,request)
	page_title = "Team Profile"
	librarian = Librarian.objects.get(username=username)
	return render (request, "Team_detail.html", locals())