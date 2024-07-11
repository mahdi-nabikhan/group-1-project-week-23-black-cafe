from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from .models import Categories, Payment, Products, Cart, OrderItem, CheckOrder, Comment, Image, ProductImage, Ticket
from .forms import OrderForm, CartForm, TicketForm, AddCategoryForm, AddProductForm
from .models import Ticket, Categories, Products
from django.test import TestCase, Client
from django.urls import reverse
from cafe.models import Categories, Products, Cart, OrderItem, User
from cafe.forms import OrderForm, CartForm, TicketForm, AddCategoryForm, AddProductForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CategoriesModelTest(TestCase):
    def test_create_category(self):
        category = Categories.objects.create(name="Electronics", description="Electronics items")
        self.assertEqual(category.name, "Electronics")
        self.assertEqual(category.description, "Electronics items")


class PaymentModelTest(TestCase):
    def test_create_payment(self):
        payment = Payment.objects.create(payment_status=Payment.Status.PAY)
        self.assertEqual(payment.payment_status, Payment.Status.PAY)


class ProductsModelTest(TestCase):
    def setUp(self):
        self.category = Categories.objects.create(name="Electronics", description="Electronics items")

    def test_create_product(self):
        product = Products.objects.create(
            product_name="Laptop",
            quantity_in_stock=10,
            description="A powerful laptop",
            category=self.category,
            price=1000,
            discount=10
        )
        self.assertEqual(product.product_name, "Laptop")
        self.assertEqual(product.quantity_in_stock, 10)
        self.assertEqual(product.description, "A powerful laptop")
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.price, 1000)
        self.assertEqual(product.discount, 10)


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="password", age=25,
                                             city="Test City")

    def test_create_cart(self):
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(cart.user, self.user)
        self.assertFalse(cart.status)
        self.assertIsNotNone(cart.created_at)

    def test_cart_total_amount(self):
        category = Categories.objects.create(name="Electronics", description="Electronics items")
        product1 = Products.objects.create(
            product_name="Laptop",
            quantity_in_stock=10,
            description="A powerful laptop",
            category=category,
            price=1000
        )
        product2 = Products.objects.create(
            product_name="Mouse",
            quantity_in_stock=50,
            description="A wireless mouse",
            category=category,
            price=50
        )
        cart = Cart.objects.create(user=self.user)
        OrderItem.objects.create(product=product1, quantity=1, cart=cart)
        OrderItem.objects.create(product=product2, quantity=2, cart=cart)
        self.assertEqual(cart.get_total_amount(), 1100)


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.category = Categories.objects.create(name="Electronics", description="Electronics items")
        self.product = Products.objects.create(
            product_name="Laptop",
            quantity_in_stock=10,
            description="A powerful laptop",
            category=self.category,
            price=1000
        )
        self.user = User.objects.create_user(email="testuser@example.com", password="password", age=25,
                                             city="Test City")
        self.cart = Cart.objects.create(user=self.user)

    def test_create_order_item(self):
        order_item = OrderItem.objects.create(product=self.product, quantity=1, cart=self.cart)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.quantity, 1)
        self.assertEqual(order_item.cart, self.cart)
        self.assertEqual(order_item.total(), 1000)


class CheckOrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="staff@example.com", password="password", age=30, city="Staff City")
        self.cart = Cart.objects.create(user=self.user)

    def test_create_check_order(self):
        check_order = CheckOrder.objects.create(staff_id=self.user, cart_id=self.cart, status=CheckOrder.Status.PENDING)
        self.assertEqual(check_order.staff_id, self.user)
        self.assertEqual(check_order.cart_id, self.cart)
        self.assertEqual(check_order.status, CheckOrder.Status.PENDING)


class CommentModelTest(TestCase):
    def setUp(self):
        self.category = Categories.objects.create(name="Electronics", description="Electronics items")
        self.content_type = ContentType.objects.get_for_model(Categories)

    def test_create_comment(self):
        comment = Comment.objects.create(
            content_type=self.content_type,
            object_id=self.category.id,
            text="Great category!"
        )
        self.assertEqual(comment.content_type, self.content_type)
        self.assertEqual(comment.object_id, self.category.id)
        self.assertEqual(comment.text, "Great category!")


class ImageModelTest(TestCase):
    def setUp(self):
        self.category = Categories.objects.create(name="Electronics", description="Electronics items")

    def test_create_image(self):
        image = Image.objects.create(category=self.category, title="Laptop Image", description="An image of a laptop")
        self.assertEqual(image.category, self.category)
        self.assertEqual(image.title, "Laptop Image")
        self.assertEqual(image.description, "An image of a laptop")


class ProductImageModelTest(TestCase):
    def setUp(self):
        self.category = Categories.objects.create(name="Electronics", description="Electronics items")
        self.product = Products.objects.create(
            product_name="Laptop",
            quantity_in_stock=10,
            description="A powerful laptop",
            category=self.category,
            price=1000
        )

    def test_create_product_image(self):
        product_image = ProductImage.objects.create(product=self.product, title="Laptop Image",
                                                    description="An image of a laptop")
        self.assertEqual(product_image.product, self.product)
        self.assertEqual(product_image.title, "Laptop Image")
        self.assertEqual(product_image.description, "An image of a laptop")


class TicketModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="password", age=25,
                                             city="Test City")

    def test_create_ticket(self):
        ticket = Ticket.objects.create(user=self.user, title="Issue with order",
                                       description="The product arrived damaged", phone="1234567890")
        self.assertEqual(ticket.user, self.user)
        self.assertEqual(ticket.title, "Issue with order")
        self.assertEqual(ticket.description, "The product arrived damaged")
        self.assertEqual(ticket.phone, "1234567890")


class FormsTestCase(TestCase):

    def test_order_form_valid_data(self):
        form_data = {'quantity': 5}
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_order_form_invalid_data(self):
        form_data = {'quantity': 'invalid'}  # quantity should be an integer
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_cart_form_valid_data(self):
        form_data = {'user_id': 1}
        form = CartForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_cart_form_invalid_data(self):
        form_data = {'user_id': 'invalid'}  # user_id should be an integer
        form = CartForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_ticket_form_valid_data(self):
        form_data = {
            'title': 'Test Ticket',
            'description': 'Test Description',
            'phone': '1234567890'
        }
        form = TicketForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_ticket_form_invalid_data(self):
        form_data = {
            'title': '',
            'description': 'Test Description',
            'phone': '1234567890'
        }
        form = TicketForm(data=form_data)
        self.assertFalse(form.is_valid())  # title is required

    def test_add_category_form_valid_data(self):
        category_data = {
            'name': 'Test Category',
            'description': 'Test Description',
            'input_image': None  # ImageField can be optional in this test context
        }
        form = AddCategoryForm(data=category_data)
        self.assertFalse(form.is_valid())

    def test_add_category_form_invalid_data(self):
        category_data = {
            'name': '',
            'description': 'Test Description',
            'input_image': None
        }
        form = AddCategoryForm(data=category_data)
        self.assertFalse(form.is_valid())  # name is required

    def test_add_product_form_valid_data(self):
        product_data = {
            'product_name': 'Test Product',
            'quantity_in_stock': 10,
            'description': 'Test Description',
            'price': 100,
            'discount': 10,
            'input_image': None  # ImageField can be optional in this test context
        }
        form = AddProductForm(data=product_data)
        self.assertFalse(form.is_valid())

    def test_add_product_form_invalid_data(self):
        product_data = {
            'product_name': '',
            'quantity_in_stock': 10,
            'description': 'Test Description',
            'price': 100,
            'discount': 10,
            'input_image': None
        }
        form = AddProductForm(data=product_data)
        self.assertFalse(form.is_valid())  # product_name is required


class ViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='testuser@test.com', password='12345', age=21)
        self.category = Categories.objects.create(name='Test Category', description='Test Description')
        self.product = Products.objects.create(
            product_name='Test Product',
            quantity_in_stock=10,
            description='Test Description',
            price=100,
            discount=10,
            category=self.category
        )
        self.cart = Cart.objects.create(user=self.user, status=False)

    def test_category_list_view(self):
        response = self.client.get(reverse('cafe:landing_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'coffee_template/index.html')
        self.assertIn('category', response.context)

    def test_product_list_view(self):
        response = self.client.get(reverse('cafe:items', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'coffee_template/generic.html')
        self.assertIn('products', response.context)

    def test_item_detail_get(self):
        response = self.client.get(reverse('cafe:detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing_page/details.html')
        self.assertIn('product', response.context)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], OrderForm)

    def test_search_view(self):
        response = self.client.get(reverse('cafe:search') + '?q=Test')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'coffee_template/generic.html')
        self.assertIn('products', response.context)

    def test_about_us_view(self):
        response = self.client.get(reverse('cafe:about_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing_page/about_us.html')

    def test_ticket_view_get(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('cafe:ticket'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing_page/forms/ticket_cart.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], TicketForm)

    def test_add_category_view_get(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('cafe:add_category'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing_page/forms/add_category.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], AddCategoryForm)

    def test_add_product_view_get(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('cafe:add_product', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing_page/forms/add_product.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], AddProductForm)

    def test_admin_show_carts_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('cafe:seecart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing_page/show_all_cart.html')
        self.assertIn('carts', response.context)

    def test_export_to_excel_view(self):
        response = self.client.get(reverse('cafe:export_to_excel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/ms-excel')
        self.assertIn('attachment; filename="products.xlsx"', response['Content-Disposition'])

    def test_chart_view(self):
        response = self.client.get(reverse('cafe:cats'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/top_sales.html')

    def test_user_chart_view(self):
        response = self.client.get(reverse('cafe:user_chart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/city_chart.html')

    def test_user_age_view(self):
        response = self.client.get(reverse('cafe:user_age'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/age_chart.html')

    def test_cart_chart_view(self):
        response = self.client.get(reverse('cafe:cart_chart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing_page/cart_chart.html')

    def test_all_product_view(self):
        response = self.client.get(reverse('cafe:all_product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'coffee_template/all_product.html')
        self.assertIn('product', response.context)
