from django.shortcuts import render, redirect

from django.views.generic.edit import UpdateView
from django.views import View

from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView

from materialdesign.sidebar import *

from schools.models import School

from django.utils.decorators import method_decorator

from django.contrib.auth.decorators import login_required

from .forms import*
from .models import *


class Login(LoginView):

    template_name = "login.html"


class LostPassword(View):

    page_title = "New password"
    form_class = LoginForm
    template_name = "loginpage.html"


def logout_view(request):

    logout(request)

    return redirect('home')


class Registration(View):
    """Admin registration. The students registration will be done automaticaly by the admin"""
            
    template_name = "Registration.html"
    #form_class = RegistrationForm
    
    fields = [
    'password', 'email','first_name',
    'last_name', 'school_name', 'school_country',
    'school_city', 'school_town', 'school_address',
    'school_postal_code',
    ]
    #success_url = reverse_lazy('home')

    def get(self, request):
        
        return render(request, self.template_name, locals())

    def checkForm(self):
        
        for l in self.fields:
            if request.POST[l]!='':
                if request.POST[l]=='email':
                    # Check the email field
                    pass
                else:
                    return False
                # Check other fields
            else: 
                return False

        return True

    def post(self, request, *args, **kwargs):
        
        
        # Check if the form is valide


        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email'] 
        first_name = request.POST['first_name']  
        last_name = request.POST['last_name'] 

        school_name = request.POST['school_name']  
        school_country = request.POST['school_country'] 
        school_city = request.POST['school_city']
        school_address = request.POST['school_address'] 
        school_postal_code = request.POST['school_postal_code']


        #Create the admin
        admin = Administrator.objects.create(username = username,
            email=email,
            first_name=first_name, 
            last_name=last_name)

        school = School.objects.create(name=school_name, country = school_country,
            city = school_city, address = school_address, postal_code = school_postal_code)

        admin.set_password(password)
        admin.school = school

        school.save()
        admin.save()

        login(request, admin)

        return redirect('admin_lib')

  
def account_redirect(request):
    
    return redirect('accounts', request.user.id)

@method_decorator(login_required, name='dispatch')
class Account(UpdateView):
    """Update the user's details"""

    template_name = "account.html"
    model = Reader
    form_class = ReaderForm

    def __init__(self, *args, **kwargs):
        super(Account, self).__init__(*args, **kwargs)
        self.context_object_name = 'reader'


    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['lst_menu'] = Menus(2, self.request)
        
        return context
