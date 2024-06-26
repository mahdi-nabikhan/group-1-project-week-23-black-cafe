from django.shortcuts import render, redirect
from django.views.generic import ListView, View

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
    # {'context object name :queryset}
    context_object_name = 'category'
    template_name = 'coffee_template/index.html' ######


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
        return render(request, 'coffee_template/generic.html', context)


# def items_detail(request, item_id):
#     c = Products.objects.filter(id=item_id)
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form1 = form.cleaned_data
#             product = Products.objects.get(id=item_id)
#             user = User.objects.get(id=form1['user_id'])
#             total = form1['quantity'] * product.price
#             OrderItem(product_id=product, user_id=user, quantity=form1['quantity'], price=product.price,
#                       discount=0, total_price=total).save()
#             Cart.objects.create(user_id=user, total_amount=total)
#             return redirect('cafe:landing_page')

#     else:
#         form = OrderForm()
#         return render(request, 'landing_page/details.html', {'product': c, 'form': form})


class ItemDetail(View):
    template_name = 'landing_page/details.html'

    def get(self, request, item_id):
        product = Products.objects.filter(id=item_id)
        form = OrderForm()
        return render(request, 'landing_page/details.html', {'product': product, 'form': form})

    def post(self, request, item_id):
        product = Products.objects.filter(id=item_id)
        product1 = Products.objects.get(id=item_id)
        form = OrderForm(request.POST)
        if form.is_valid():
            cart = Cart.objects.create(user=request.user)

            order = OrderItem(product=product1, quantity=form.cleaned_data['quantity'], cart=cart)
            order.save()
            return render(request, 'landing_page/details.html', {'product': product, 'form': form})


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


def search_products(request):
    product_name = request.GET.get('q')
    products = Products.objects.filter(product_name__contains=product_name)

    context = {'products': products,
               'not_found': f'{product_name} does not exist.'
               }
    return render(request, 'coffee_template/generic.html', context)


def about_us(request):
    return render(request, 'landing_page/about_us.html')


def contact_us(request):
    pass


# def cart_detail(request):
#     form = CartForm()
#     cart = Cart()
#     if request.method == 'POST':
#         form = CartForm(request.POST)
#         if form.is_valid():
#             form1 = form.cleaned_data
#             cart.objects.get(id=form1['user_id'])
#             return redirect('cafe:landing_page')
#     else:
#         context = {'form': form, 'cart': cart}
#         return render(request, 'landing_page/forms/cart_views.html', context)


class ShowCarts(View):
    # template_name =

    def get(self, request):
        cart = Cart.objects.filter(user=request.user)
        return render(request, 'landing_page/all_carts.html', {'cart': cart})



class Ticket(View):
    def post(self, request):
        form = TicketForm(request.POST)
        if form.is_valid():

            m = form.save(commit=False)
            m.user = request.user

            m.save()

            form.save(commit=False)
            form.user = request.user
            form.save()

            return redirect('cafe:landing_page')

    def get(self, request):
        form = TicketForm()
        return render(request, 'landing_page/forms/ticket_cart.html', {'form': form})


class AddCategory(View):
    def get(self, request):
        form = AddCategoryForm()
        return render(request, 'landing_page/forms/add_category.html', {'form': form})

    def post(self, request):
        form = AddCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category_item = form.cleaned_data
            category = form.save()
            Image.objects.create(image=category_item['input_image'], category=category)
            return redirect('cafe:landing_page')
