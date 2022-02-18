from django.shortcuts import render, redirect

from .forms import*

from django.views import View

import africanlibraries.settings as settings

from django.core.mail import send_mail

class SendMessage(View):


	def post(self, request):

		name = request.POST['name']
		email = request.POST['email']
		subject = request.POST['subject']
		message = request.POST['message']

		send_mail(
                subject,
                message + "\n From: {}".format(email),
                settings.DEFAULT_FROM_EMAIL,
                recipient_list = [settings.DEFAULT_FROM_EMAIL])

		return redirect('home')

	def get(self, request):

		return redirect('home')

class Subscribe(View):

	def post(self, request):

		name = request.POST['name']
		email = request.POST['email']
		
		# Subscribe here 

		return redirect('home')

	def get(self, request):

		return redirect('home')

class WeeklyReport(View):
	"""docstring for WeeklyReport"""
	def __init__(self, arg):
		super(WeeklyReport, self).__init__()
		self.arg = arg
		