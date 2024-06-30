from django.urls import path, include
from django.views.generic import detail
from .views import *

app_name = 'accounts'
urlpatterns = [path('login/', loginview, name='login'),
               path('logout/', logoutview, name='logout'),
               path('rigerster/', RegisterView.as_view(), name='register'), ]
