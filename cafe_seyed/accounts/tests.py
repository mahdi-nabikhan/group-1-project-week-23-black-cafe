from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from django.core.exceptions import ValidationError


class CustomUserFormsTests(TestCase):

    def test_custom_user_creation_form_valid(self):
        """Test CustomUserCreationForm with valid data"""
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'age': 25,
            'city': 'Test City',
            'password1': 'Testpass123',
            'password2': 'Testpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_custom_user_creation_form_password_mismatch(self):
        """Test CustomUserCreationForm with password mismatch"""
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'age': 25,
            'city': 'Test City',
            'password1': 'Testpass123',
            'password2': 'Differentpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], ['Passwords must match'])


class CustomUserViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')
        self.login_url = reverse('accounts:login')
        self.landing_page_url = reverse('cafe:landing_page')
        self.user_model = get_user_model()
        self.user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'age': 25,
            'city': 'Test City',
            'password1': 'Testpass123',
            'password2': 'Testpass123'
        }
        self.user_model.objects.create_user(
            email='loginuser@example.com', password='Testpass123', age=25, city='Test City')

    def test_register_view_get(self):
        """Test GET request to register view"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/registration.html')

    def test_register_view_post_valid(self):
        """Test POST request to register view with valid data"""
        response = self.client.post(self.register_url, data=self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.landing_page_url)
        self.assertTrue(self.user_model.objects.filter(email='testuser@example.com').exists())

    def test_login_view_get(self):
        """Test GET request to login view"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_logout_view(self):
        """Test logout view"""
        self.client.login(email='loginuser@example.com', password='Testpass123')
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.landing_page_url)
        self.assertFalse('_auth_user_id' in self.client.session)


class CustomUserTests(TestCase):

    def setUp(self):
        self.user_model = get_user_model()

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'testuser@example.com'
        password = 'Testpass123'
        age = 25
        city = 'Test City'
        user = self.user_model.objects.create_user(
            email=email,
            password=password,
            age=age,
            city=city
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.age, age)
        self.assertEqual(user.city, city)

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'testuser@EXAMPLE.COM'
        user = self.user_model.objects.create_user(
            email=email,
            password='Testpass123',
            age=25,
            city='Test City'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            self.user_model.objects.create_user(
                email=None,
                password='Testpass123',
                age=25,
                city='Test City'
            )

    def test_create_superuser(self):
        """Test creating a new superuser"""
        email = 'superuser@example.com'
        password = 'Testpass123'
        age = 25
        city = 'Super City'
        user = self.user_model.objects.create_superuser(
            email=email,
            password=password,
            age=age,
            city=city
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_superuser_must_have_is_staff_true(self):
        """Test superuser must have is_staff=True"""
        with self.assertRaises(ValueError):
            self.user_model.objects.create_superuser(
                email='superuser@example.com',
                password='Testpass123',
                age=25,
                city='Super City',
                is_staff=False
            )

    def test_superuser_must_have_is_superuser_true(self):
        """Test superuser must have is_superuser=True"""
        with self.assertRaises(ValueError):
            self.user_model.objects.create_superuser(
                email='superuser@example.com',
                password='Testpass123',
                age=25,
                city='Super City',
                is_superuser=False
            )

    def test_age_is_positive(self):
        """Test that age must be a positive integer"""
        with self.assertRaises(ValidationError):
            user = self.user_model(
                email='user@example.com',
                age=-1,
                city='Test City'
            )
            user.full_clean()

    def test_email_field_is_unique(self):
        """Test that email field is unique"""
        email = 'uniqueuser@example.com'
        password = 'Testpass123'
        age = 25
        city = 'Unique City'
        self.user_model.objects.create_user(
            email=email,
            password=password,
            age=age,
            city=city
        )
        with self.assertRaises(ValidationError):
            user = self.user_model(
                email=email,
                age=30,
                city='Another City'
            )
            user.full_clean()
