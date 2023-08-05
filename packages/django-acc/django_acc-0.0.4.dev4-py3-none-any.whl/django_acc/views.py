from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from .models import Profile, Organization

class RegisterView(View):
    def get(self, request):
        return render(request, 'django_acc/register.html')
    def post(self, request):
        payload = request.POST
        try:
            new_user = User.objects.create_user(payload['username'], payload['email'], payload['password'])
            profile = Profile(fullname=payload['fullname'], user=new_user)
            profile.save()
            
            default_organization = Organization(name=new_user.username, owner=new_user)
            default_organization.save()
            
        except ValueError as value_err:
            err = str(value_err)
            return render(request, 'django_acc/register.html', {'err': err})
        return HttpResponse('hi')

class MyLoginView(LoginView):
    template_name = 'django_acc/login.html'
    next = "google.com"
