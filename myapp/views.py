from django.db import connection
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.urls import reverse
from django.http import HttpResponseRedirect


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
        image_filenames = ['thinkpad.jpg', 'dell.jpg',
                           'MSI.jpg']  # Add your image filenames here
        products_with_images = zip(products, image_filenames)
        return render(request, 'index.html', {'products_with_images': products_with_images})


def add_to_cart(request, product_id, ram, price, processor, name):
    with connection.cursor() as cursor:
        price_f = float(price)
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS cart (
                        CartID INT AUTO_INCREMENT PRIMARY KEY,
                        ComputerID INT,
                        RAM INT,
                        Price FLOAT,
                        Processor INT,
                        Name VARCHAR(100) NOT NULL,
                        FOREIGN KEY (ComputerID) REFERENCES Computer(ComputerID)
                    )
                """)
        insert_query = """
            INSERT INTO cart (ComputerID, RAM, Price, Processor, Name)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (product_id,
                       ram, price_f, processor, name))
    return redirect('/')


def view_cart(request):
    with connection.cursor() as cursor:
        cursor.execute("""SHOW TABLES LIKE 'cart';""")
        table_exists = cursor.fetchone()
        if table_exists:
            cursor.execute("SELECT * FROM server.cart")
            cart_items = cursor.fetchall()
        else:
            return render(request, 'cart.html', {'cart_items': []})

        # You can add additional logic here if needed (e.g., fetching from another table)

        return render(request, 'cart.html', {'cart_items': cart_items})


def checkout(request):
    with connection.cursor() as cursor:
        cursor.execute("""DROP TABLE cart;""")
    return redirect('/ShoppingCart')


def remove_item(request, product_id):
    with connection.cursor() as cursor:
        insert_query = """
            DELETE FROM cart
            WHERE CartID = %s
        """
        cursor.execute(insert_query, (product_id,))
    return redirect('/ShoppingCart')


def custom_computers_view(request):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM Pre_assembled")
        products = cursor.fetchall()
        image_filenames = ['thinkpad.jpg', 'dell.jpg',
                           'MSI.jpg', 'Acer-Aspire.jpg', 'Del-XPS.jpg',
                           'acernitro.jpg', 'hp.jpg', 'HP-Pav.jpg', 'lenovo.jpg']  # Add your image filenames here
        products_with_images = zip(products, image_filenames)
        return render(request, 'computers.html', {'products_with_images': products_with_images})
