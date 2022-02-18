from django.shortcuts import render, redirect
from schools.Objects import Menus
from schools.models import School


def home(request):

	return render(request, "index.html", locals())

def get_school(request):

	try:
		school = School.objects.get(name=request.GET['school'])
		statut = school
		return redirect('home_school', school)
	except Exception as e:
		#raise e
		lst_menu = Menus(0, request, platform=True)
		statut = 'Not Found ! '
		#return redirect('home_school', )
		return render(request, "mainHome.html", locals())