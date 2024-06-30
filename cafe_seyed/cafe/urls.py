from django.urls import path, include
from django.views.generic import detail

from .views import *

app_name = 'cafe'
urlpatterns = [path('', CategoryListView.as_view(), name='landing_page'),
               path('item/<int:category_id>/', ProductListView.as_view(), name='items'),
               path('detail/<int:item_id>/', ItemDetail.as_view(), name='detail'),
               path('carts/', cart_detail, name='cart_detail'),
               path('search/', search_products, name='search'),
               path('about_us/', about_us, name='about_us'),
               path('contact_us/', contact_us, name='contact_us'),
               path('detail/<int:item_id>/', ItemDetail.as_view(), name='detail'),
               path('showcart/', ShowCarts.as_view(), name='showcart'),
               path('tickets/', Ticket.as_view(), name='ticket'),

               path('showcart/', ShowCarts.as_view(), name='showcart'),
               path('tickets/', Ticket.as_view(), name='ticket'),
               path('add_category/', AddCategory.as_view(), name='add_category'),
               path('add_product/<int:category_id>', AddProduct.as_view(), name='add_product'),
               path('shows/', AddItem.as_view(), name='shows'),
               path('seecart/', AdminShowCarts.as_view(), name='seecart'),
               path('show/<cart_id>', Show.as_view(), name='show'),
               path('staff/', StaffPage.as_view(), name='staff'),
               path('adminsee/',AdminShowCart.as_view(), name='adminsee'),

               ]
