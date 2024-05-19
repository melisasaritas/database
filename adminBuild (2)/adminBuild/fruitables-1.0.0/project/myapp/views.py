from django.db import connection
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def custom_view(request):
    # Your custom logic here
    data = {"message": "Hello from a model-less view!"}
    return Response(data)


def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Execute raw SQL query to authenticate user
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM customer WHERE Username = %s AND Password = %s", [username, password])
            row = cursor.fetchone()
            if row:
                return redirect('/')
            else:
                # Invalid credentials
                return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'login.html')

# Define your custom view function for signup


@api_view(['GET', 'POST'])
def custom_register_view(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Execute raw SQL query to add user to the customer table
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO customer (Username, Password) VALUES (%s, %s)", [username, password])

        # Redirect to a success page or any other desired view
        return redirect('/login')
    else:
        # Render the signup form template
        return render(request, 'signup.html')

@api_view(['GET', 'POST'])
def custom_home_view(request):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM Pre_assembled")
        products = cursor.fetchall()
        image_filenames = ['thinkpad.jpg', 'dell.jpg', 'MSI.jpg']  # Add your image filenames here
        products_with_images = zip(products, image_filenames)
        return render(request, 'index.html', {'products_with_images': products_with_images})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])
    if product_id not in cart:
        cart.append(product_id)
    request.session['cart'] = cart
    return redirect('/')

def view_cart(request):
    cart = request.session.get('cart', [])
    if (cart == []):
        return render(request, 'cart.html', {'cart_items': []})
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM Pre_assembled WHERE ComputerID IN (%s)" % ','.join(['%s'] * len(cart)), cart)
        cart_items = cursor.fetchall()
        if not cart_items:
            cursor.execute(
                "SELECT * FROM custom_made WHERE ComputerID IN (%s)" % ','.join(['%s'] * len(cart)), cart)
            cart_items = cursor.fetchall()
        return render(request, 'cart.html', {'cart_items': cart_items})

def checkout(request):
    request.session['cart'] = []
    return redirect('/ShoppingCart')
