from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm


class CityForm(forms.ModelForm):
    class Meta:
        model = models.City
        fields = ['name', 'country']
        widgets = {
            'name': forms.TextInput(),
            'country': forms.Select(),
        }


class ShopForm(forms.ModelForm):
    class Meta:
        model = models.Shop
        fields = ['name', 'city', 'adress']
        widgets = {
            'name': forms.TextInput(),
            'city': forms.Select(),
            'adress': forms.TextInput(),
        }


class GoodForm(forms.ModelForm):
    class Meta:
        model = models.Good
        fields = ['name', 'price', 'manufacturer', 'quantity', 'photo', 'status']
        widgets = {
            'name': forms.TextInput(),
            'price': forms.NumberInput(),
            'manufacturer': forms.Select(),
            'quantity': forms.NumberInput(),
            'photo': forms.FileInput(),
            'status': forms.Select()
        }


class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = models.Manufacturer
        fields = ['name']
        widgets = {
            'name': forms.TextInput(),
        }


class CreateUserForm(UserCreationForm):
    email = forms.CharField(
        label="E-mail",
        widget=forms.EmailInput(),
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.save()
        return user


class CakeForm(forms.ModelForm):
    class Meta:
        model = models.Cake
        fields = ['form', 'category', 'weight', 'photo', 'color', 'inscription']
        widgets = {
            'form': forms.Select(),
            'category': forms.Select(),
            'weight': forms.NumberInput(attrs={'step': 0.50, 'max': 4.00, "min": 1.00}),
            'photo': forms.FileInput(),
            'color': forms.Select(),
            'inscription': forms.TextInput(),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ['date_ready', 'shop']
        widgets = {
            'date_ready': forms.DateInput(),
            'shop': forms.Select(),
        }
