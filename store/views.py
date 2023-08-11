# Modified by Tamer Ayoub - 08/11/2023

# This file contains our different views such as store, cart, checkout, updateItem and processOrder

from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
# cookieCart, cartData and guestOrder are logic functions stored in the utils.py file to run some of  our logic processes
from .utils import cookieCart, cartData, guestOrder


def store(request):

    # CartData is a function in utils.py that returns a dictionary of items that include the total number of
    # cart items, the order and items
    data = cartData(request)

    # Retrieves the different cart itemes
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    # Fetches a list of all available products.
    products = Product.objects.all()

    # This dictionary named context is created to hold the data that will be passed to the template for rendering
    # It includes the 'products' and 'cartItems' data retrieved earlier.
    context = {'products': products, 'cartItems': cartItems}

    # Render the 'store.html' template with the provided context data
    return render(request, 'store/store.html', context)


def cart(request):

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

# This updateItem view can get called from the store and the cart template. This view correlates to cart.js.
# Elements with the class 'update-cart', when clicked, will activate this view.


def updateItem(request):
    # the data dictionary receives the proudctId and action from the cart.js file
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    # retrieves current logged in user
    customer = request.user.customer

    # retrives the current product we are updating using the productId
    product = Product.objects.get(id=productId)

    # this line either creates a new order or fetches an existing order in the Order model for the customerm, using customer as a condition
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    # this line either creates a new orderItem or fetches an existing orderItem in the OrderItem model, using order and product as a condition
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    # add or remove quanity, based on the action
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    # This line is saves the changes made to the orderItem object to the database
    orderItem.save()

    # if the orderItem falls below 0, delete the item
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


# This view 'processOrder' gets called from the checkout.html template. When user submits userFormData and shippingInfo into form, process the order here


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    # if a user has a order, get it, or create it, using customer as a condition ; else use guestOrder, which is a function in the utils.py file file
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
    else:
        # The guestOrder function will retur our 'guest' a customer account aswell as an order
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)
