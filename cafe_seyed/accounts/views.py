from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from cafe.urls import *
from .decorators import unauthenticated_user, allowed_users
from .models import CustomUser


# Create your views here.

@unauthenticated_user
def login_view(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("cafe:landing_page")

    return render(request, 'accounts/login.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('cafe:landing_page')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(CustomLoginView, self).form_valid(form)


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
@unauthenticated_user
def RegisterView(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('cafe:landing_page'))
    context = {"form": form}
    return render(request, 'accounts/registration.html', context)


class RegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/registration.html'
    success_url = reverse_lazy('cafe:landing_page')


class EditProfileView(UpdateView):
    model = CustomUser

    success_url = reverse_lazy('cafe:profile')
    template_name = 'forms/edit_profile.html'
    fields = ['first_name', 'last_name', 'age', 'city']
    context_object_name = 'form'