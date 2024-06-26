from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from cafe.urls import *

# Create your views here.


def loginview(request):

    if request.method == 'POST':

        username=request.POST["username"]
        password=request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return render(request, 'landing_page/staff.html')
            login(request , user)
            return redirect('cafe:landing_page')
        else:
            return HttpResponse('Invalid Login')
        
    return render (request,'accounts/login.html')


def logoutview(request):
    logout(request)
    return redirect('cafe:landing_page')


class RegisterView(View):
    def post(self, request):
        if request.POST['password'] != request.POST['confirm_password']:
            return HttpResponse('Passwords do not match')

        user = User(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'])
        user.save()
        return redirect('cafe:landing_page')

    def get(self, request):
        return render(request, 'accounts/registeration.html')