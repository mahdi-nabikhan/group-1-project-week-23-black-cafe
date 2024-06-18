from django.contrib.contenttypes.models import ContentType

from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.


from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.TextField()


class Products(models.Model):
    product_name = models.CharField(max_length=200, null=False)
    quantity_in_stock = models.IntegerField(null=False)
    description = models.TextField()
    category = models.ForeignKey(Categories, on_delete=models.DO_NOTHING)
    price = models.IntegerField(null=False)
    discount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.product_name, self.price}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_amount(self):
        pass

    def sum(self):
        pass


class OrderItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(null=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="order_items")

    # TODO: Merge the two methods. Don't be clown
    # def all_price(self):
    #     if self.discount > 0:
    #         self.total_price = self.price * self.quantity * (100 - self.discount // 100)
    #         return self.total_price
    #     self.total_price = self.price * self.quantity
    #     return self.total_price

    def prices(self):
        pass

    def total(self):
        pass


class Payment(models.Model):
    class Status(models.TextChoices):
        PAY = 'PD', 'Paid'
        NOT_PAY = 'NP', 'Not Paid'

    # ... other fields ...

    payment_status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.NOT_PAY
    )


# class Staff(models.Model):
#     firstname = models.CharField(max_length=300)
#     lastname = models.CharField(max_length=300)
#     phone = models.CharField(max_length=13)


class CheckOrder(models.Model):
    class Status(models.TextChoices):
        PENDING = ('Pending', 'Pending')
        DELIVERED = ('Delivered', 'Delivered')
        CANCELED = ('Canceled', 'Canceled')

    staff_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    cart_id = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.CharField(max_length=200)
    content_object = GenericForeignKey('content_type', 'object_id')
    text = models.TextField()


class Image(models.Model):
    category = models.ForeignKey(Categories, related_name='image', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', verbose_name='image')


class ProductImage(models.Model):
    product = models.ForeignKey(Products, related_name='image', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product_image/', verbose_name='image')
