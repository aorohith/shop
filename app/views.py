
from django.http import JsonResponse
from django.shortcuts import render,redirect
from .models import *
from django.views import View
from .forms import CustRegForm,CustProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ProductView(View):
    def get(self,request):
        carttotal = 0
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        if request.user.is_authenticated:
            carttotal = len(Cart.objects.filter(user=request.user))
        content = {
            'mobiles':mobiles,
            'laptops':laptops,
            'topwears':topwears,
            'bottomwears':bottomwears,
            'carttotal':carttotal,
        }
        return render(request, 'app/home.html' ,content)


def search(request):
    product_objects = Product.objects.all()
    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        product_objects = product_objects.filter(title__icontains = item_name)
    return render(request,'app/search.html',{'product_objects':product_objects})

class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        item_already_in_cart = False
        carttotal = 0
        if request.user.is_authenticated:
            carttotal = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        content = {'product':product, 'item_already_in_cart':item_already_in_cart, 'carttotal':carttotal}
        print(item_already_in_cart)
        return render(request,'app/productdetail.html',content)

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

@login_required
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
            carttotal = 0
            if request.user.is_authenticated:
                carttotal = len(Cart.objects.filter(user=request.user))
            content = {'carts':cart,'amount':amount, 'totalamount':totalamount,'carttotal':carttotal}
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

@login_required
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

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user = request.user)
    carttotal = 0
    if request.user.is_authenticated:
        carttotal = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/orders.html',{'order_placed':op,'carttotal':carttotal})

@login_required
def buy_now(request):
    carttotal = 0
    if request.user.is_authenticated:
        carttotal = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/buynow.html',{'carttotal':carttotal})

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    carttotal = 0
    if request.user.is_authenticated:
        carttotal = len(Cart.objects.filter(user=request.user))
    content = {'add':add,
               'active':'btn-primary',
               'carttotal': carttotal,
    }
    return render(request, 'app/address.html',content)



def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'POCO' or data == 'Realme' or data == 'Apple':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    carttotal = 0
    if request.user.is_authenticated:
        carttotal = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/mobile.html', {'mobiles':mobiles,'carttotal':carttotal})

def laptop(request, data=None):
    if data == None:
        laptops = Product.objects.filter(category='L')
    elif data == 'HP' or data == 'Asuse' or data == 'Apple' or data =='Lenovo':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    carttotal = 0
    if request.user.is_authenticated:
        carttotal = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/laptop.html', {'laptops':laptops,'carttotal':carttotal})

def topwear(request, data=None):
    if data == None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'NIKE' or data == 'PUMA' or data == 'ADIDAS':
        topwears = Product.objects.filter(category='TW').filter(brand=data)
    carttotal = 0
    if request.user.is_authenticated:
        carttotal = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/topwear.html', {'topwears':topwears,'carttotal':carttotal})


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



@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustProfileForm()
        carttotal = 0
        if request.user.is_authenticated:
            carttotal = len(Cart.objects.filter(user=request.user))
        content = {'form':form,
                    'active':'btn-primary',
                    'carttotal':carttotal,
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


