from django.urls import path, include
from django.views.generic import detail

from .views import *

app_name = 'cafe'
urlpatterns = [path('', landing_page, name='landing_page'),
               path('item/<int:category_id>/', items, name='items'),
               path('detail/<int:item_id>/', items_detail, name='detail'),
               path('carts/', cart_detail, name='cart_detail'), ]
# path('order/',order_items,name='order'),]
