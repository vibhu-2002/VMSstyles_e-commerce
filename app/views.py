from django.shortcuts import render, redirect
from django.views import View

from .models import Product, Cart, Customer, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm

from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



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
        item_already_in_cart = False
        if request.user.is_authenticated:

         item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product': product,'item_already_in_cart': item_already_in_cart})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product= Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        if not cart.exists():  
            return render(request, 'app/emptycart.html')

        amount = 0.0
        shipping_amount = 7.0
        totalamount = 0.0
        for p in cart:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
        totalamount = amount + shipping_amount
        return render(request, 'app/addtocart.html', {
            'carts': cart,
            'amount': amount,
            'totalamount': totalamount,
            'shipping_amount': shipping_amount
        })
    else:
        return redirect('login')  

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 7.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
        totalamount = amount + shipping_amount
        
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount,
            
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 7.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
        totalamount = amount + shipping_amount
        
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount,
            
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')

        # Delete all matching cart items for the product and user
        Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).delete()

        amount = 0.0
        shipping_amount = 7.0
        cart_products = Cart.objects.filter(user=request.user)

        for p in cart_products:
            amount += p.quantity * p.product.discounted_price

        totalamount = amount + shipping_amount

        return JsonResponse({
            'amount': amount,
            'totalamount': totalamount
        })




        
def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})

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

@login_required
def checkout(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)

    amount = 0.0
    shipping_amount = 7.0

    for item in cart_items:
        amount += item.quantity * item.product.discounted_price

    totalamount = amount + shipping_amount

    return render(request, 'app/checkout.html', {
        'add': add,
        'cart_items': cart_items,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'totalamount': totalamount
    })
@login_required
def payment_done(request):
    if request.method == "POST":
        user = request.user
        custid = request.POST.get('custid')
        customer = Customer.objects.get(id=custid)
        cart = Cart.objects.filter(user=user)

        for c in cart:
            OrderPlaced.objects.create(
                user=user,
                customer=customer,
                product=c.product,
                quantity=c.quantity
            )
            c.delete()
        return redirect("orders")
    return redirect("checkout")

@method_decorator(login_required, name='dispatch')
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