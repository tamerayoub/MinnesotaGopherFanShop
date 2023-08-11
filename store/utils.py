# Modified by Tamer Ayoub - 08/11/2023

# In Django, a "utils" file, short for utilities, is typically used to store various utility functions, classes,
# or constants that don't belong to a specific app or module but are used across different parts of your project.
# These utility functions are often used to perform common tasks, handle repetitive operations, or encapsulate complex logic.

import json
from .models import *


def cookieCart(request):

    # Create empty cart for now for non-logged in user
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        print('CART:', cart)

    items = []

    # Code below refers to the Model Order and its action functions get_cart_total, get_cart_items, and shipping
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    for i in cart:
        # We use try block to prevent items in cart that may have been removed from causing error
        try:
            if(cart[i]['quantity'] > 0):  # items with negative quantity = lot of freebies
                cartItems += cart[i]['quantity']

                product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

                item = {
                    'id': product.id,
                    'product': {'id': product.id, 'name': product.name, 'price': product.price,
                                'imageURL': product.imageURL}, 'quantity': cart[i]['quantity'],
                    'digital': product.digital, 'get_total': total,
                }
                items.append(item)

                if product.digital == False:
                    order['shipping'] = True
        except:
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems': cartItems, 'order': order, 'items': items}


# guestOrder function gets called during the processOrder View funcion logic when user isnt authenticated ->
# Create a guestOrder by returning a customer and their order to the back to the view


def guestOrder(request, data):

    # get the users form data
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    # get a customer if it exist, or create one if not, using email as a condition
    customer, created = Customer.objects.get_or_create(
        email=email,
    )

    # using the name submitted on the form by the guest, update the name of our new customer object
    customer.name = name
    customer.save()

    # create a order for our new customer
    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            # negative quantity = freebies
            quantity=(item['quantity'] if item['quantity']
                      > 0 else -1*item['quantity']),
        )
    return customer, order
