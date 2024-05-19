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
