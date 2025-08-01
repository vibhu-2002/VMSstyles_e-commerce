from django.shortcuts import render
from django.views import View

from .models import Product, Cart, Customer, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm

from django.contrib import messages



class ProductView(View):  # ✅ fixed casing
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        return render(request, 'app/home.html', {
            'topwears': topwears,
            'bottomwears': bottomwears,
            'mobiles': mobiles
        })

class ProductDetailView(View):  # ✅ fixed casing 
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', {'product': product})


def add_to_cart(request):
 return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

def address(request):
 return render(request, 'app/address.html')

def orders(request):
 return render(request, 'app/orders.html')

def mobile(request, data=None):
    if data is None:
        mobiles = Product.objects.filter(category='M')
    elif data.lower() in ['redmi', 'samsung']:
        mobiles = Product.objects.filter(category='M', brand__iexact=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M', discounted_price__lt=200)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M', discounted_price__gt=200)
    else:
        mobiles = Product.objects.filter(category='M')  # fallback for unknown data

    return render(request, 'app/mobile.html', {'mobiles': mobiles})



class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful!")
            form = CustomerRegistrationForm()  # Clear form after save
        else:
            messages.error(request, "Please correct the errors below.")
        return render(request, 'app/customerregistration.html', {'form': form})    


def checkout(request):
 return render(request, 'app/checkout.html')


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
           usr= request.user
           name = form.cleaned_data['name']
           locality = form.cleaned_data['locality']
           city = form.cleaned_data['city']
           state = form.cleaned_data['state']
           zipcode = form.cleaned_data['zipcode']
           reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
           reg.save()
           messages.success(request, "Profile updated successfully!")
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})