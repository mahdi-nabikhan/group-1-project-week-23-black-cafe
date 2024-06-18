from django import forms


class OrderForm(forms.Form):

    quantity = forms.IntegerField()


class CartForm(forms.Form):
    user_id = forms.IntegerField()



