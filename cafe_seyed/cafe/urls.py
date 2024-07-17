from django.urls import path, include
from django.views.generic import detail

from .views import *

app_name = 'cafe'
urlpatterns = [path('', CategoryListView.as_view(), name='landing_page'),
               path('item/<int:pk>/', ProductListView.as_view(), name='items'),
               path('detail/<int:item_id>/', ItemDetail.as_view(), name='detail'),
               path('carts/', cart_detail, name='cart_detail'),
               path('search/', Search.as_view(), name='search'),
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
               path('show/<int:pk>', Show.as_view(), name='show'),
               path('staff/', StaffPage.as_view(), name='staff'),
               path('adminsee/', AdminShowCart.as_view(), name='adminsee'),
               path('cats/', chart, name='cats'),
               path('export/', export_to_excel, name='export_to_excel'),
               path('userchart/', user_chart, name='user_chart'),
               path('user_age/', user_age, name='user_age'),
               path('cart_chart/', cart_chart, name='cart_chart'),
               path('all_products/', AllProduct.as_view(), name='all_product'),
               path('profile/', Profile.as_view(), name='profile'),
               path('not_pay_cart/',NotPaidCart.as_view(),name='not_paid_cart'),
               path('paid_cart/',PaidCart.as_view(),name='paid_cart'),
               path('adminshow/<pk>/',AdminShowDetail.as_view(),name='adminshow'),
               path('pay/',PayCart.as_view(),name='pay'),
               path('delete_item/<int:pk>/',DeleteItem.as_view(),name='delete_item'),

               ]
