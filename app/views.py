
from django.shortcuts import render
from .models import *
from django.views import View
from .forms import CustRegForm,CustProfileForm
from django.contrib import messages


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
    return render(request, 'app/addtocart.html')

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
 return render(request, 'app/checkout.html')

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


