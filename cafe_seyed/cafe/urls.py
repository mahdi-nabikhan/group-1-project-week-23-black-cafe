from django.urls import path, include
from django.views.generic import detail

from .views import *

app_name = 'cafe'
urlpatterns = [path('', CategoryListView.as_view(), name='landing_page'),
               path('item/<int:category_id>/', ProductListView.as_view(), name='items'),
               path('detail/<int:item_id>/', ItemDetail.as_view(), name='detail'),
               path('carts/', cart_detail, name='cart_detail'), ]
# path('order/',order_items,name='order'),]
