from django.urls import path, include
from django.views.generic import detail
from .views import *

app_name = 'accounts'
urlpatterns = [path('login/', login_view, name='login'),
               path('logout/', logoutview, name='logout'),
               path('register/', RegisterView, name='register'), ]
