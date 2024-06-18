from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View

from .models import *
from .forms import *


# Create your views here.


# def landing_page(request):
#     category = Categories.objects.all()
#     context = {'category': category}
#     return render(request, 'landing_page/land.html', context)
#

class CategoryListView(ListView):
    model = Categories
    queryset = Categories.objects.all()
    context_object_name = 'category'
    template_name = 'landing_page/land.html'


# def items(request, category_id):
#     category = Categories.objects.get(id=category_id)
#     products = Products.objects.filter(category=category)
#     context = {'products': products, 'category': category}
#
#     return render(request, 'landing_page/category_items.html', context)


class ProductListView(View):

    def get(self, request, category_id):
        category = Categories.objects.get(id=category_id)
        products = Products.objects.filter(category=category)
        context = {'products': products, 'category': category}
        return render(request, 'landing_page/category_items.html', context)


def items_detail(request, item_id):
    c = Products.objects.filter(id=item_id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form1 = form.cleaned_data
            product = Products.objects.get(id=item_id)
            user = User.objects.get(id=form1['user_id'])
            total = form1['quantity'] * product.price
            OrderItem(product_id=product, user_id=user, quantity=form1['quantity'], price=product.price,
                      discount=0, total_price=total).save()
            Cart.objects.create(user_id=user, total_amount=total)
            return redirect('cafe:landing_page')

    else:
        form = OrderForm()
        return render(request, 'landing_page/details.html', {'product': c, 'form': form})


class ItemDetail(View):
    template_name = 'landing_page/details.html'

    def get(self, request, item_id):
        product = Products.objects.filter(id=item_id)
        form = OrderForm()
        return render(request, self.template_name, {'product': product, 'form': form})

    def post(self, request, item_id):
        # product = Products.objects.filter(id=item_id)
        product = Products.objects.get(id=item_id)
        form = OrderForm(request.POST)
        if form.is_valid():
            cart = Cart.objects.create(user=request.user)

            order = OrderItem(product=product, quantity=form.cleaned_data['quantity'], cart=cart)
            order.save()
            return render(request, self.template_name, {'product': product, 'form': form})


# def order_items(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form1 = form.cleaned_data
#             product = Products.objects.get(id=form1['product_id'])
#             user = User.objects.get(id=form1['user_id'])
#             total = form1['quantity'] * product.price
#             OrderItem(product_id=product, user_id=user, quantity=form1['quantity'], price=product.price,
#                       discount=0, total_price=total).save()
#             return redirect('cafe:landing_page')
#
#     else:
#         form = OrderForm()
#         return render(request, 'form_order.html', {'form': form})


def cart_detail(request):
    form = CartForm()
    cart = Cart()
    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            form1 = form.cleaned_data
            cart.objects.get(id=form1['user_id'])
            return redirect('cafe:landing_page')
    else:
        context = {'form': form, 'cart': cart}
        return render(request, 'landing_page/forms/cart_views.html', context)
