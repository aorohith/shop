
from django.http import JsonResponse
from django.shortcuts import render,redirect
from .models import *
from django.views import View
from .forms import CustRegForm,CustProfileForm
from django.contrib import messages
from django.db.models import Q


class ProductView(View):
    def get(self,request):
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        content = {
            'mobiles':mobiles,
            'laptops':laptops,
            'topwears':topwears,
            'bottomwears':bottomwears,
        }
        return render(request, 'app/home.html' ,content)


class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        return render(request,'app/productdetail.html',{'product':product})

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user ]
        # cart product total amount
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            content = {'carts':cart,'amount':amount, 'totalamount':totalamount}
            return render(request, 'app/addtocart.html',content)
        else:
            return render(request, 'app/emptycart.html')
            

# cart count plus button function

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user ]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


# cart count minus button function

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user ]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user ]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def buy_now(request):
 return render(request, 'app/buynow.html')

def address(request):
    add = Customer.objects.filter(user=request.user)
    content = {'add':add,
               'active':'btn-primary'
    }
    return render(request, 'app/address.html',content)

def orders(request):
 return render(request, 'app/orders.html')

def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'POCO' or data == 'Realme' or data == 'Apple':
        mobiles = Product.objects.filter(category='M').filter(brand=data)

    return render(request, 'app/mobile.html', {'mobiles':mobiles})


class CustRegView(View):
    def get(self,request):
        form = CustRegForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    def post(self,request):
        form = CustRegForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations Registered successfully')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})


def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user ]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    content = {'add':add, 'totalamount':totalamount,'cart_items':cart_items}
    return render(request, 'app/checkout.html', content)

class ProfileView(View):
    def get(self,request):
        form = CustProfileForm()
        content = {'form':form,
                    'active':'btn-primary'
        }
        return render(request,'app/profile.html', content )
    
    def post(self,request):
        form = CustProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request,'Congratulations!! Profile updated successfully')
        content = {'form':form,
                    'active':'btn-primary'
        }
        return render(request, 'app/profile.html',content)


