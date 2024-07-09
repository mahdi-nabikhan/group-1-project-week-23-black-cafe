from django.urls import path, include
from django.views.generic import detail
from .views import *

app_name = 'accounts'
urlpatterns = [path('login/', CustomLoginView.as_view(), name='login'),
               path('logout/', logoutview, name='logout'),
               path('register/', RegistrationView.as_view(), name='register'), ]
