from django import forms

from cafe.models import Ticket, Categories, Products


class OrderForm(forms.Form):
    quantity = forms.IntegerField()


class CartForm(forms.Form):
    user_id = forms.IntegerField()


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'phone']


class AddCategoryForm(forms.ModelForm):
    input_image = forms.ImageField(label='Image')

    class Meta:
        model = Categories
        fields = ['name', 'description']


class AddProductForm(forms.ModelForm):
    input_image = forms.ImageField(label='Image')

    class Meta:
        model = Products
        fields = ['product_name', 'quantity_in_stock', 'description', 'price', 'discount']
