from django.db.models import Sum, F, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import *
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.descriptors import Max
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

User = get_user_model()
from .models import *
from .forms import *
from .decorators import *
from django.utils.decorators import method_decorator


# Create your views here.


class CategoryListView(ListView):
    model = Categories
    context_object_name = 'category'
    template_name = 'coffee_template/index.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        category = [self.get_queryset()[i:i + 4] for i in range(0, len(self.get_queryset()), 4)]
        context["category"] = category
        return context


# def items(request, category_id):
#     category = Categories.objects.get(id=category_id)
#     products = Products.objects.filter(category=category)
#     context = {'products': products, 'category': category}
#
#     return render(request, 'landing_page/category_items.html', context)


# class ProductListView(View):

#     def get(self, request, category_id):
#         category = Categories.objects.get(id=category_id)
#         products = Products.objects.filter(category=category)
#         context = {'products': products, 'category': category}
#         return render(request, 'coffee_template/generic.html', context)

class ProductListView(DetailView):
    model = Categories
    template_name = 'coffee_template/generic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object  # id ro mide (override shode az hamin method)
        item = Products.objects.filter(category=category)
        context.update({
            'products': item,
        })
        return context


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
            order = OrderItem(product=product1, quantity=form.cleaned_data['quantity'])
            test = Cart.objects.filter(user=request.user, status=False).first()
            if test:
                order.cart = test
                order.save()
            else:
                order.cart = Cart.objects.create(user=request.user)
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


# def search_products(request):
#     product_name = request.GET.get('q')
#     products = Products.objects.filter(product_name__contains=product_name)

#     context = {'products': products,
#                'not_found': f'{product_name} does not exist.'
#                }
#     return render(request, 'coffee_template/generic.html', context)

class Search(ListView):
    model = Products
    template_name = 'coffee_template/generic.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        product_name = self.request.GET.get('q')
        all_products = self.get_queryset().filter(product_name__icontains=product_name)
        context["products"] = all_products
        context["not_found"] = f'{product_name} does not exist.'
        return context


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


# class ShowCarts(View):
#     def get(self, request):
#         cart = Cart.objects.filter(user=request.user)
#
#         cart = cart.annotate(result=F('order_items__product__price') * F('order_items__quantity'))
#
#         total_price = cart.aggregate(total_price=Sum('result'))['total_price']
#
#         return render(request, 'landing_page/all_carts.html', {'cart': cart, 'total_price': total_price})


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


# class AddCategory(View):
#     def get(self, request):
#         form = AddCategoryForm()
#         return render(request, 'landing_page/forms/add_category.html', {'form': form})
#
#     def post(self, request):
#         form = AddCategoryForm(request.POST, request.FILES)
#         if form.is_valid():
#             category_item = form.cleaned_data
#             category = form.save()
#             Image.objects.create(image=category_item['input_image'], category=category)
#             return redirect('cafe:landing_page')
@method_decorator(allowed_users(allowed_roles=['manager', 'staff']), name='dispatch')
class AddCategory(FormView):
    form_class = AddCategoryForm
    template_name = 'landing_page/forms/add_category.html'
    success_url = reverse_lazy('cafe:landing_page')

    def form_valid(self, form):
        form_data = form.cleaned_data
        category = Categories.objects.create(name=form_data['name'], description=form_data['description'])
        Image.objects.create(category=category, image=form_data['input_image'])
        return super().form_valid(form)


@method_decorator(allowed_users(allowed_roles=['manager', 'staff']), name='dispatch')
class AddProduct(View):
    def get(self, request, category_id):
        form = AddProductForm()
        context = {'form': form}
        return render(request, 'landing_page/forms/add_product.html', context)

    def post(self, request, category_id):
        category = Categories.objects.get(id=category_id)
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.category = category
            product.save()
            ProductImage.objects.create(image=form.cleaned_data['input_image'], product=product)
            return redirect('cafe:landing_page')


class AddItem(ListView):
    model = Categories
    queryset = Categories.objects.all()
    context_object_name = 'category'
    template_name = 'landing_page/admin_panel.html'


class AdminShowCarts(ListView):
    model = Cart
    queryset = Cart.objects.filter(status=True)
    context_object_name = 'carts'
    template_name = 'landing_page/show_all_cart.html'


# class Show(View):
#     def get(self, request, cart_id):
#         cart = Cart.objects.get(id=cart_id)
#         item = OrderItem.objects.filter(cart=cart)
#         cart2 = item.annotate(result=F('product__price') * F('quantity'))

#         total_price = cart2.aggregate(total_price=Sum('result'))['total_price']

#         context = {'item': item, 'total_price': total_price,'cart2':cart2}
#         return render(request, 'coffee_template/my_cart.html', context)

class Show(DetailView):
    model = User
    template_name = 'coffee_template/my_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object  # id ro mide (override shode az hamin method)
        item = OrderItem.objects.filter(cart__user=user, cart__status=False)
        cart2 = item.annotate(result=F('product__price') * F('quantity'))
        total_price = cart2.aggregate(total_price=Sum('result'))['total_price']
        context.update({
            'item': item,
            'total_price': total_price,
            'cart2': cart2
        })
        return context


class PayCart(View):
    template_name = 'coffee_template/my_cart.html'

    def post(self, request):
        user = request.user.id
        cart = Cart.objects.get(user=user,status=False)
        cart.status = True
        cart.save()
        return redirect('cafe:landing_page')


class DeleteItem(DeleteView):
    model = OrderItem
    success_url = reverse_lazy('cafe:landing_page')
    template_name = 'coffee_template/delete_order_item.html'



# class ShowCarts(View):
#     def get(self, request):
#         cart = Cart.objects.filter(user=request.user, status=False)
#         return render(request, 'landing_page/all_carts.html', {'cart': cart})

@method_decorator(allowed_users(allowed_roles=['manager', 'staff']), name='dispatch')
class ShowCarts(ListView):
    model = Cart
    template_name = 'landing_page/all_carts.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cart'] = Cart.objects.filter(user=self.request.user, status=False)
        return data


@method_decorator(allowed_users(allowed_roles=['manager', 'staff']), name='dispatch')
class StaffPage(View):
    def get(self, request):
        # return render(request, template_name='landing_page/staff.html')
        return render(request, template_name='admin/dashboard.html')


# class AdminShowCart(View):
#     template_name = 'landing_page/adminshowcart.html'

#     def get(self, request):
#         cart = Cart.objects.all()
#         context = {'cart': cart}
#         return render(request, template_name=self.template_name, context=context)

class AdminShowCart(ListView):
    model = Cart
    template_name = 'landing_page/adminshowcart.html'
    context_object_name = 'cart'


def chart(request):
    result = (OrderItem.objects.all()
              .values('product__product_name')
              .annotate(dcount=Sum('quantity'))
              .order_by()
              )
    product_name = []
    quantity = []
    for i in result:
        for j in i.values():
            if type(j) == int:
                quantity.append(j)
            else:
                product_name.append(j)

    context = {'test': result, 'quantity': quantity, 'label': product_name}
    # return render(request, 'landing_page/cats.html', context)
    return render(request, 'admin/top_sales.html', context)


def export_to_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="products.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Products"

    # Add headers
    headers = ["Name", "Price", "Quantity"]
    ws.append(headers)

    # Add data from the model
    result = OrderItem.objects.filter(cart__status=True)
    for products in result:
        ws.append([products.product.product_name, products.product.price, products.quantity])

    # Save the workbook to the HttpResponse
    wb.save(response)
    return response


# chage of userchart
def user_chart(request):
    result = (User.objects.all()
              .values('city')
              .annotate(dcount=Count('id'))
              .order_by()
              )

    city = []
    quantity = []

    for dicts in result:
        for j in dicts.values():
            if type(j) == int:
                quantity.append(j)
            else:
                city.append(j)

    context = {'quantity': quantity, 'city': city}
    return render(request, 'admin/city_chart.html', context)


def user_age(request):
    user_age = (User.objects.all()
                .values('age')
                .annotate(dcount=Count('id'))
                .order_by()
                )
    age = []
    count_age = []
    d = []
    for dict in user_age:
        age.append(dict['age'])
        count_age.append(dict['dcount'])
        d.append(dict)

    context = {'age': age, 'count_age': count_age, 'd': d}
    return render(request, 'admin/age_chart.html', context)


from django.db.models.functions import ExtractHour


def cart_chart(request):
    result = (Cart.objects.all()
              .annotate(hour=ExtractHour('created_at'))
              .values('hour')
              .annotate(dcount=Count('hour'))
              .order_by('hour')
              )

    time = []
    for i in result:
        time.append(i['hour'])

    quantity = []
    for i in result:
        quantity.append(i['dcount'])
    context = {'result': result, 'time': time, 'quantity': quantity}
    return render(request, 'landing_page/cart_chart.html', context)


class AllProduct(ListView):
    model = Products
    context_object_name = 'product'
    template_name = 'coffee_template/all_product.html'


class Profile(View):
    template_name = 'coffee_template/profile.html'

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        not_pay_cart = Cart.objects.filter(user=user, status=False)
        pay_cart = Cart.objects.filter(user=user, status=True)
        orders = OrderItem.objects.filter(cart__status=True, quantity__gt=5)
        context = {'user': user, 'not_pay_cart': not_pay_cart, 'pay_cart': pay_cart, 'orders': orders}
        return render(request, template_name=self.template_name, context=context)


class PaidCart(ListView):
    queryset = Cart.objects.filter(status=True)
    template_name = "admin/pay_cart.html"
    context_object_name = 'pay_cart'


class NotPaidCart(ListView):
    queryset = Cart.objects.filter(status=False)
    template_name = "admin/not_pay_cart.html"
    context_object_name = 'not_pay_cart'


class AdminShowDetail(DetailView):
    model = Cart
    template_name = 'admin/admin_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.object
        context['orders'] = OrderItem.objects.filter(cart=cart)
        return context

