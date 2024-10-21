from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group

from django.http import HttpResponse
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from . import models
from . import forms


def admin_edit(request):
    return render(request, 'admin_edit.html')


def main(request):
    return render(request, 'main.html')


class CityListView(ListView):
    model = models.City
    template_name = 'cities.html'
    context_object_name = 'cities'


class CityCreateView(CreateView):
    model = models.City
    form_class = forms.CityForm
    template_name = 'city_create.html'
    success_url = reverse_lazy('city_list')


class ShopListView(ListView):
    model = models.Shop
    template_name = 'shops.html'
    context_object_name = 'shops'


class ShopCreateView(CreateView):
    model = models.Shop
    form_class = forms.ShopForm
    template_name = 'shop_create.html'
    success_url = reverse_lazy('shop_list')


class ShopUpdateView(UpdateView):
    model = models.Shop
    form_class = forms.ShopForm
    template_name = 'shop_update.html'
    success_url = reverse_lazy('shop_list')


class ShopDeleteView(DeleteView):
    model = models.Shop
    success_url = reverse_lazy('shop_list')
    template_name = 'shop_delete.html'


def conf_del_shop(request, pk):
    shop = get_object_or_404(models.Shop, pk=pk)
    return render(request, 'conf_del_shop.html', {'shop': shop})


class GoodListView(ListView):
    model = models.Good
    template_name = 'goods.html'
    context_object_name = 'goods'


class GoodCreateView(CreateView):
    model = models.Good
    form_class = forms.GoodForm
    template_name = 'good_create.html'
    success_url = reverse_lazy('good_list')


class GoodUpdateView(UpdateView):
    model = models.Good
    form_class = forms.GoodForm
    template_name = 'good_update.html'
    success_url = reverse_lazy('good_list')


class GoodDeleteView(DeleteView):
    model = models.Good
    success_url = reverse_lazy('good_list')
    template_name = 'good_delete.html'


def conf_del_good(request, pk):
    good = get_object_or_404(models.Good, pk=pk)
    return render(request, 'conf_del_good.html', {'good': good})


class ManufacturerListView(ListView):
    model = models.Manufacturer
    template_name = 'manufacturers.html'
    context_object_name = 'manufacturers'


class ManufacturerCreateView(CreateView):
    model = models.Manufacturer
    form_class = forms.ManufacturerForm
    template_name = 'manufacturer_create.html'
    success_url = reverse_lazy('manufacturer_list')


def sign_out(request):
    logout(request)
    return redirect('main')


def sign_up(request):
    if request.method == 'POST':
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.groups.add(Group.objects.get(name='client'))
            login(request, new_user)
            return redirect('client_main')
        else:
            return render(request, 'sign_up.html', {'form': form})
    else:
        form = forms.CreateUserForm()
        return render(request, 'sign_up.html', {'form': form})


def sign_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            if is_manager(user):
                return redirect('admin_edit')
            else:
                return redirect('client_main')
        else:
            return render(request, 'sign_in.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'sign_in.html', {'form': form})


def is_manager(user):
    return user.groups.filter(name='manager').exists()


def client_main(request):
    return render(request, 'client_main.html')


def cake_create(request):
    if request.method == 'POST':
        form = forms.CakeForm(request.POST)
        if form.is_valid():
            cake = form.save(commit=False)
            cake.price = cake.weight * 1000
            cake.prepayment = cake.price / 2
            cake.save()
            return render(request, 'order_create.html', {'cake': cake})
        else:
            return redirect('cake_create')
    else:
        form = forms.CakeForm()
    return render(request, 'cake_create.html', {'form': form})


def order_create(request):
    if request.method == 'POST':
        form = forms.OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_main')
        else:
            return redirect('order_create')
    else:
        form = forms.OrderForm()
    return render(request, 'order_create.html', {'form': form})
