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
            # ADMIN LOGIN ADDING
            cursor.execute(
                "SELECT * FROM administration WHERE AdminUsername = %s AND AdminPassword = %s", [username, password])
            admin = cursor.fetchone()

            if admin:
                return redirect('/AdminPanel')

            cursor.execute(
                "SELECT * FROM customer WHERE Username = %s AND Password = %s", [username, password])
            row = cursor.fetchone()
            if row:
                # Extract CustomerID from the retrieved row
                customer_id = row[0]

                # Execute query to retrieve detailed customer information
                cursor.execute(
                    """
                    SELECT 
                        c.CustomerID,
                        c.Username,
                        cp.Phone,
                        cb.BankAccount,
                        ca.Address
                    FROM 
                        customer c
                    JOIN 
                        cust_phone cp ON c.CustomerID = cp.CustomerID
                    JOIN 
                        cust_bankacc cb ON c.CustomerID = cb.CustomerID
                    JOIN 
                        cust_address ca ON c.CustomerID = ca.CustomerID
                    WHERE 
                        c.CustomerID = %s;
                    """,
                    [customer_id]
                )

                # Fetch all details of the customer
                customer_info = cursor.fetchone()

                # Zip customer_info
                keys = ["CustomerID", "Username",
                        "Phone", "BankAccount", "Address"]
                customer_info_dict = dict(zip(keys, customer_info))

                # GET THE ORDER HISTORY
                cursor.execute(
                    """
                    SELECT 
                        RecordID, CustomerID, Feedback, Cancel_flag, Proceeding_flag, Received_flag, OrderDate
                    FROM records
                    WHERE
                        CustomerID = %s;
                    """,
                    [customer_id]
                )

                order_info = cursor.fetchall()  # Use fetchall() to get all records
                order_info_keys = ["RecordID", "CustomerID", "Feedback",
                                   "Cancel_flag", "Proceeding_flag", "Received_flag", "OrderDate"]
                order_info_list = [dict(zip(order_info_keys, order))
                                   for order in order_info]

                # Pass both customer_info and order_info to the template for rendering
                return render(request, 'useraccountnew.html', {'login_info': customer_info_dict, 'order_info': order_info_list})

            else:
                # Invalid credentials
                return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'login.html')


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
        return redirect('/UserAccount')

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

    return redirect(request.META.get('HTTP_REFERER', '/'))


def add_components_to_cart(request, product_id, name, price):
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
            INSERT INTO cart (ComputerID, Price, Name)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (product_id, price_f, name))

    return redirect(request.META.get('HTTP_REFERER', '/'))


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
        cursor.execute("SELECT * FROM Pre_assembled")
        products = cursor.fetchall()

        # Filter products by type
        laptops = [product for product in products if product[4] == 1]
        engineering_pcs = [product for product in products if product[4] == 2]
        gaming_pcs = [product for product in products if product[4] == 3]
        desktops = [product for product in products if product[4] == 4]

        image_filenames = ['thinkpad.jpg', 'dell.jpg', 'MSI.jpg', 'Acer-Aspire.jpg', 'Del-XPS.jpg',
                           'acernitro.jpg', 'hp.jpg', 'HP-Pav.jpg', 'lenovo.jpg']  # Add your image filenames here

        # Pair each product list with its respective image filenames
        products_with_images = zip(products, image_filenames)
        laptops_with_images = zip(laptops, image_filenames[:len(laptops)])
        engineering_with_images = zip(
            engineering_pcs, image_filenames[:len(engineering_pcs)])
        gaming_with_images = zip(gaming_pcs, image_filenames[:len(gaming_pcs)])
        desktops_with_images = zip(desktops, image_filenames[:len(desktops)])

        context = {
            'products_with_images': products_with_images,
            'laptops_with_images': laptops_with_images,
            'engineering_with_images': engineering_with_images,
            'gaming_with_images': gaming_with_images,
            'desktops_with_images': desktops_with_images
        }

        return render(request, 'computers.html', context)


def custom_components_view(request):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT component.*, monitor.* "
            "FROM component "
            "INNER JOIN monitor ON component.SerialNumber = monitor.SerialNumber"
        )
        monitors = cursor.fetchall()
        cursor.execute(
            """SELECT * FROM component INNER JOIN keyboard ON component.SerialNumber = keyboard.SerialNumber;""")
        keyboards = cursor.fetchall()
        cursor.execute(
            """SELECT * FROM component INNER JOIN ram ON component.SerialNumber = ram.SerialNumber;""")
        rams = cursor.fetchall()
        cursor.execute(
            """SELECT * FROM component INNER JOIN storage_device ON component.SerialNumber = storage_device.SerialNumber AND storage_device.SSD_flag = 1;""")
        SSDs = cursor.fetchall()
        cursor.execute(
            """SELECT * FROM component INNER JOIN storage_device ON component.SerialNumber = storage_device.SerialNumber AND storage_device.HDD_flag = 1;""")
        HDDs = cursor.fetchall()
        cursor.execute(
            """SELECT * FROM component INNER JOIN processing_unit ON component.SerialNumber = processing_unit.SerialNumber AND processing_unit.CPU_flag = 1;""")
        CPUs = cursor.fetchall()
        cursor.execute(
            """SELECT * FROM component INNER JOIN processing_unit ON component.SerialNumber = processing_unit.SerialNumber AND processing_unit.GPU_flag = 1;""")
        GPUs = cursor.fetchall()
        image_filenames = ['intel-corei5.jpg', 'gigabyte.jpeg',
                           'ryzen5.png', 'acernitro.jpg', 'kingstonssd.jpg',
                           'westernhdd.jpg', 'coffekeyboard.jpg']

        monitors_with_images = zip(monitors, image_filenames)
        keyboards_with_images = zip(keyboards, image_filenames)
        rams_with_images = zip(rams, image_filenames)
        SSDs_with_images = zip(SSDs, image_filenames)
        HDDs_with_images = zip(HDDs, image_filenames)
        CPUs_with_images = zip(CPUs, image_filenames)
        GPUs_with_images = zip(GPUs, image_filenames)

        return render(request, 'shop.html', {'MONITORS': monitors_with_images, 'KEYBOARDS': keyboards_with_images, 'RAMS': rams_with_images, 'SSDS': SSDs_with_images, 'HDDS': HDDs_with_images, 'CPUS': CPUs_with_images, 'GPUS': GPUs_with_images})


def show_monitors(request):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT component.*, monitor.* "
            "FROM component "
            "INNER JOIN monitor ON component.SerialNumber = monitor.SerialNumber"
        )
        monitors = cursor.fetchall()
        image_filenames = ['intel-corei5.jpg', 'gigabyte.jpeg',
                           'ryzen5.png', 'acernitro.jpg', 'kingstonssd.jpg',
                           'westernhdd.jpg', 'coffekeyboard.jpg']
        monitors_with_images = zip(monitors, image_filenames)
    return render(request, 'shop.html', {'MONITORS': monitors_with_images})


def show_keyboards(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT * FROM component INNER JOIN keyboard ON component.SerialNumber = keyboard.SerialNumber;""")
        keyboards = cursor.fetchall()
        image_filenames = ['coffekeyboard.jpg',
                           'intel-corei5.jpg', 'gigabyte.jpeg']
        keyboards_with_images = zip(keyboards, image_filenames)
    return render(request, 'shop.html', {'KEYBOARDS': keyboards_with_images})


def show_rams(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT * FROM component INNER JOIN ram ON component.SerialNumber = ram.SerialNumber;""")
        rams = cursor.fetchall()
        image_filenames = ['intel-corei5.jpg', 'gigabyte.jpeg',
                           'ryzen5.png', 'acernitro.jpg', 'kingstonssd.jpg',
                           'westernhdd.jpg', 'coffekeyboard.jpg']
        rams_with_images = zip(rams, image_filenames)
    return render(request, 'shop.html', {'RAMS': rams_with_images})


def show_ssds(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT * FROM component INNER JOIN storage_device ON component.SerialNumber = storage_device.SerialNumber AND storage_device.SSD_flag = 1;""")
        SSDs = cursor.fetchall()
        image_filenames = ['intel-corei5.jpg', 'gigabyte.jpeg',
                           'ryzen5.png', 'acernitro.jpg', 'kingstonssd.jpg',
                           'westernhdd.jpg', 'coffekeyboard.jpg']
        SSDs_with_images = zip(SSDs, image_filenames)
    return render(request, 'shop.html', {'SSDS': SSDs_with_images})


def show_hdds(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT * FROM component INNER JOIN storage_device ON component.SerialNumber = storage_device.SerialNumber AND storage_device.HDD_flag = 1;""")
        HDDs = cursor.fetchall()
        image_filenames = ['intel-corei5.jpg', 'gigabyte.jpeg',
                           'ryzen5.png', 'acernitro.jpg', 'kingstonssd.jpg',
                           'westernhdd.jpg', 'coffekeyboard.jpg']
        HDDs_with_images = zip(HDDs, image_filenames)
    return render(request, 'shop.html', {'HDDS': HDDs_with_images})


def show_cpus(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT * FROM component INNER JOIN processing_unit ON component.SerialNumber = processing_unit.SerialNumber AND processing_unit.CPU_flag = 1;""")
        CPUs = cursor.fetchall()
        image_filenames = ['intel-corei5.jpg', 'gigabyte.jpeg',
                           'ryzen5.png', 'acernitro.jpg', 'kingstonssd.jpg',
                           'westernhdd.jpg', 'coffekeyboard.jpg']
        CPUs_with_images = zip(CPUs, image_filenames)
    return render(request, 'shop.html', {'CPUS': CPUs_with_images})


def show_gpus(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT * FROM component INNER JOIN processing_unit ON component.SerialNumber = processing_unit.SerialNumber AND processing_unit.GPU_flag = 1;""")
        GPUs = cursor.fetchall()
        image_filenames = ['intel-corei5.jpg', 'gigabyte.jpeg',
                           'ryzen5.png', 'acernitro.jpg', 'kingstonssd.jpg',
                           'westernhdd.jpg', 'coffekeyboard.jpg']
        GPUs_with_images = zip(GPUs, image_filenames)
    return render(request, 'shop.html', {'GPUS': GPUs_with_images})


def custom_stock_data(request):
    with connection.cursor() as cursor:
        # Fetch components with monitors
        cursor.execute(
            '''
            SELECT component.SerialNumber, component.Price, component.Name 
            FROM component 
            INNER JOIN monitor ON component.SerialNumber = monitor.SerialNumber
            '''
        )
        monitors = cursor.fetchall()

        # Fetch components with keyboards
        cursor.execute(
            '''
            SELECT component.SerialNumber, component.Price, component.Name  
            FROM component 
            INNER JOIN keyboard ON component.SerialNumber = keyboard.SerialNumber;
            '''
        )
        keyboards = cursor.fetchall()

        # Fetch components with RAM
        cursor.execute(
            '''
            SELECT component.SerialNumber, component.Price, component.Name, ram.Capacity 
            FROM component 
            INNER JOIN ram ON component.SerialNumber = ram.SerialNumber;
            '''
        )
        rams = cursor.fetchall()

        # Fetch components with SSDs
        cursor.execute(
            '''
            SELECT component.SerialNumber, component.Price, component.Name, storage_device.WriteSpeed, storage_device.Capacity, storage_device.ReadSpeed 
            FROM component 
            INNER JOIN storage_device ON component.SerialNumber = storage_device.SerialNumber 
            AND storage_device.SSD_flag = 1;
            '''
        )
        SSDs = cursor.fetchall()

        # Fetch components with HDDs
        cursor.execute(
            '''
            SELECT component.SerialNumber, component.Price, component.Name, storage_device.WriteSpeed, storage_device.Capacity, storage_device.ReadSpeed 
            FROM component 
            INNER JOIN storage_device ON component.SerialNumber = storage_device.SerialNumber 
            AND storage_device.HDD_flag = 1;
            '''
        )
        HDDs = cursor.fetchall()

        # Fetch components with CPUs
        cursor.execute(
            '''
            SELECT component.SerialNumber, component.Price, component.Name, processing_unit.ClockSpeed, processing_unit.Generation 
            FROM component 
            INNER JOIN processing_unit ON component.SerialNumber = processing_unit.SerialNumber 
            AND processing_unit.CPU_flag = 1;
            '''
        )
        CPUs = cursor.fetchall()

        # Fetch components with GPUs
        cursor.execute(
            '''
            SELECT component.SerialNumber, component.Price, component.Name, processing_unit.ClockSpeed, processing_unit.Generation 
            FROM component 
            INNER JOIN processing_unit ON component.SerialNumber = processing_unit.SerialNumber 
            AND processing_unit.GPU_flag = 1;
            '''
        )
        GPUs = cursor.fetchall()

        cursor.execute(
            "SELECT * FROM Pre_assembled")
        pre_assembled = cursor.fetchall()

        return render(request, 'stock_data.html', {
            'monitors': monitors,
            'keyboards': keyboards,
            'rams': rams,
            'SSDs': SSDs,
            'HDDs': HDDs,
            'CPUs': CPUs,
            'GPUs': GPUs,
            'pre_assembled': pre_assembled
        })


@api_view(['GET', 'POST'])
def custom_insert_preassembled_view(request):
    if request.method == 'POST':
        computer_id = request.POST.get('ComputerID')
        ram = request.POST.get('RAM')
        price = request.POST.get('Price')
        processor = request.POST.get('Processor')
        Type = request.POST.get('Type')
        name = request.POST.get('Name')

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO pre_assembled (ComputerID, RAM, Price, Processor, Type, Name) VALUES (%s, %s, %s, %s, %s, %s)", [computer_id, ram, price, processor, Type, name])
        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return render(request, 'stock_data.html', {'error': 'Invalid credentials'})


def custom_remove_preassembled_view(request):
    computer_id = request.POST.get('ComputerID')

    with connection.cursor() as cursor:
        cursor.execute(
            "DELETE FROM pre_assembled WHERE ComputerID = %s;", [computer_id]
        )
        return redirect(request.META.get('HTTP_REFERER', '/'))


# from django.views.decorators.http import require_http_methods
# from rest_framework.decorators import api_view


# @api_view(['POST'])
# @require_http_methods(["POST"])
# def custom_insert_preassembled_view(request):
#     computer_id = request.POST.get('ComputerID')
#     ram = request.POST.get('RAM')
#     price = request.POST.get('Price')
#     processor = request.POST.get('Processor')
#     type = request.POST.get('Type')
#     name = request.POST.get('Name')

#     with connection.cursor() as cursor:
#         cursor.execute(
#             "INSERT INTO pre_assembled (ComputerID, RAM, Price, Processor, Type, Name) VALUES (%s, %s, %s, %s, %s, %s)",
#             [computer_id, ram, price, processor, type, name]
#         )

#     return redirect('stock_data_view')

# @api_view(['POST'])
# @require_http_methods(["POST"])
#
