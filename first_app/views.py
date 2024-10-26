from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm

from .models import *
from .utils import cookieCart, cartData, guestOrder

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    return LoginView.as_view()(request)

def store(request):

     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data['items']
          

     products = Product.objects.all()
     context = {'products':products, 'cartItems':cartItems}
     return render(request, 'first_app/store.html', context)

def cart(request):

     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data['items']


     context = {'items':items, 'order':order, 'cartItems':cartItems}
     return render(request, 'first_app/cart.html', context)
#from django.views.decorators.csrf import csrf_exempt

#@csrf_exempt
def checkout(request):
     #Create empty cart for now for non-logged in user
     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data['items']

     context = {'items':items, 'order':order, 'cartItems':cartItems}
     return render(request, 'first_app/checkout.html', context)

def updateItem(request):
     data = json.loads(request.body)
     productId = data['productId']
     action = data['action']

     print('Action:', action)
     print('Product:', productId)

     customer = request.user.customer
     product = Product.objects.get(id=productId)
     order, created =Order.objects.get_or_create(customer=customer, complete=False)

     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

     if action == 'add':
          orderItem.quantity = (orderItem.quantity + 1)
     elif action == 'remove':
          orderItem.quantity = (orderItem.quantity - 1)

     orderItem.save()

     if orderItem.quantity <= 0:
          orderItem.delete()

     return JsonResponse('Item was added', safe=False)


#@csrf_exempt
def processOrder(request):
     transaction_id = datetime.datetime.now().timestamp()
     data = json.loads(request.body)

     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
     else:
          customer, order = guestOrder(request, data)

     total = float(data['form']['total'])
     order.transaction_id = transaction_id

     if total == order.get_cart_total:
          order.complete = True
     order.save()

     if order.shipping == True:
               ShippingAddress.objects.create(
                    customer = customer,
                    order = order,
                    address = data['shipping']['address'],
                    city = data['shipping']['city'],
                    state = data['shipping']['state'],
                    zipcode = data['shipping']['zipcode'],
                    )

     return JsonResponse('Payment completed!', safe=False)