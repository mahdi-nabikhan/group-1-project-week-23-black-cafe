from django import forms


class OrderForm(forms.Form):
    user_id = forms.IntegerField()
    quantity = forms.IntegerField()


class CartForm(forms.Form):
    user_id = forms.IntegerField()



