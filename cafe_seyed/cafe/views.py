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


def items(request, category_id):
    category = Categories.objects.get(id=category_id)
    products = Products.objects.filter(category=category)
    context = {'products': products, 'category': category}

    return render(request, 'landing_page/category_items.html', context)


class ProductListView(View):
    template_name = 'landing_page/category_items.html'

    def get(self, request, category_id):
        category = Categories.objects.get(id=category_id)
        products = Products.objects.filter(category=category)
        context = {'products': products, 'category': category}
        return render(request, self.template_name, context)


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
            # add foregin key model
            Cart.objects.create(user_id=user, total_amount=total)
            return redirect('cafe:landing_page')

    else:
        form = OrderForm()
        return render(request, 'landing_page/details.html', {'product': c, 'form': form})





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
