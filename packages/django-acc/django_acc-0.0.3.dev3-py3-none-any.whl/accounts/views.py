from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from .models import Profile

class RegisterView(View):
    def get(self, request):
        return render(request, 'accounts/register.html')
    def post(self, request):
        payload = request.POST
        try:
            new_user = User.objects.create_user(payload['username'], payload['email'], payload['password'])
            profile = Profile(fullname=payload['fullname'], user=new_user)
            profile.save()
        except ValueError as value_err:
            err = str(value_err)
            return render(request, 'accounts/register.html', {'err': err})
        return HttpResponse('hi')

class MyLoginView(LoginView):
    template_name = 'accounts/login.html'
    next = "google.com"
