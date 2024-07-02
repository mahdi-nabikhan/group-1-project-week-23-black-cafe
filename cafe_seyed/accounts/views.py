from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from cafe.urls import *





# Create your views here.




def login_view(request):
    form=AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            print(form)
            user=authenticate(request, username=email,password=password)
            if user is not None:
                login(request,user)
                return redirect ("cafe:landing_page")
         
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logoutview(request):
    logout(request)
    return redirect('cafe:landing_page')


# class RegisterView(View):
#     def post(self, request):
#         if request.POST['password'] != request.POST['confirm_password']:
#             return HttpResponse('Passwords do not match')

#         user = User(email=request.POST['email'], password=request.POST['password'])
#         user.set_password(request.POST['password'])
#         user.save()

#         return redirect('cafe:landing_page')

#     def get(self, request):
#         return render(request, 'accounts/registration.html')

def RegisterView(request):
    form=CustomUserCreationForm()
    if request.method=="POST":
        form=CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('cafe:landing_page'))
    context={"form":form}
    return render(request, 'accounts/registration.html',context)