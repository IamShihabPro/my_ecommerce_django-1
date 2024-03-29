from django.shortcuts import render, get_object_or_404, redirect

# Authentication
from django.contrib.auth.decorators import login_required

# Model
from App_Order.models import Cart, Order
from App_Shop.models import Product

# Messages
from django.contrib import messages

# Create your views here.


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    print('item object line 19')
    print(item)

    order_item = Cart.objects.get_or_create(item=item, user=request.user, purchase=False)
    print('order item object line 23')
    print(order_item)
    print(order_item[0])

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    print('Order qs line 28')
    print(order_qs)

    if order_qs.exists():
        order = order_qs[0]
        print('Order exits line 33')
        print(order)

        if order.orderitems.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, "This item quantity was updated")
            return redirect('home')
        else:
            order.orderitems.add(order_item[0])
            messages.info(request, "This item was added to cart")
            return redirect('home')
    else:
        order = Order(user=request.user)
        order.save()
        order.orderitems.add(order_item[0])
        messages.info(request, "This item was added to cart")
        return redirect('home')


@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchase=False)
    orders = Order.objects.filter(user=request.user, ordered=False)

    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request, 'App_Order/cart.html', context={'carts':carts, 'order':order})
    else:
        messages.warning(request, "You don't have any item in cart!")
        return redirect('home')

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    print('item 68', item)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    print('order_qs 70', order_qs)

    if order_qs.exists():
        order = order_qs[0]
        print('order 74', order)
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchase=False)[0]
            print('order_item 77', order_item)
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.warning(request, "This item is remove in your cart")
            return redirect('cart')
        else:
           messages.info(request, "This item is not in your cart")
           return redirect('home')
    else:
        messages.info(request, "You don't have any active order")
        return redirect('home')
    

@login_required
def increase_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchase=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f"{item} quantity has been updated")
                return redirect('cart')
        else:
            messages.info(request, f"{item} is not in your cart")
            return redirect('home')
    else:
        messages.info(request, "You don't have any active order")
        return redirect('home')


@login_required
def decrease_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchase=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, f"{item} quantity has been updated")
                return redirect('cart')
                
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{item} quantity has been updated")
                return redirect('cart')



        else:
            messages.info(request, f"{item} is not in your cart")
            return redirect('home')
    else:
        messages.info(request, "You don't have any active order")
        return redirect('home')