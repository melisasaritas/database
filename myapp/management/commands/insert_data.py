from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Insert dummy data into MySQL tables'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Insert dummy data into tables
            self.insert_admin_data(cursor)
            self.insert_computer_data(cursor)
            self.insert_customer_data(cursor)
            self.insert_records_data(cursor)
            self.insert_component_data(cursor)
            self.insert_storage_device_data(cursor)
            self.insert_processing_unit_data(cursor)
            self.insert_ram_data(cursor)
            self.insert_monitor_data(cursor)
            self.insert_keyboard_data(cursor)
            self.insert_pre_assembled_data(cursor)
            self.insert_recommendation_data(cursor)
            self.insert_pre_assembled_io_data(cursor)
            self.insert_buys_data(cursor)
            self.insert_use_components_data(cursor)
            # Insert data into other tables as needed

    def insert_admin_data(self, cursor):
        # Insert dummy data into the Administration table
        cursor.execute("""
            INSERT INTO Administration (BankAccount, AdminUsername, AdminPassword)
            VALUES ('1234567890', 'admin', 'admin123')
        """)

        # Insert dummy data into the Admin_Address table
        cursor.execute("""
            INSERT INTO Admin_Address (AdminId, Address)
            VALUES (1, '123 Main St')
        """)

        # Insert dummy data into the Admin_Phone table
        cursor.execute("""
            INSERT INTO Admin_Phone (AdminId, Phone)
            VALUES (1, '123-456-7890')
        """)

        # Insert data into other related tables as needed

    def insert_customer_data(self, cursor):
        # Insert dummy data into the Customer table
        cursor.execute("""
            INSERT INTO Customer (Username, Password)
            VALUES ('user1', 'user123'), ('user2', 'user123'), ('user3', 'user123')
        """)

        # Insert dummy data into the Cust_BankAcc table
        cursor.execute("""
            INSERT INTO Cust_BankAcc (CustomerID, BankAccount)
            VALUES (1, '9876543210'), (2, '9835543810'), (3, '1876743311')
        """)

        # Insert dummy data into the Cust_address table
        cursor.execute("""
            INSERT INTO Cust_address (CustomerID, Address)
            VALUES (1, '456 Elm St'), (2, '325 Ast St'), (3, '439 Lmn St')
        """)

        # Insert dummy data into the Cust_phone table
        cursor.execute("""
            INSERT INTO Cust_phone (CustomerID, Phone)
            VALUES (1, '987-654-3210'), (2, '937-664-3110'), (3, '483-154-6210')
        """)


    def insert_records_data(self, cursor):
    # Insert dummy data into the Records table (two entries)
        cursor.execute("""
            INSERT INTO Records (CustomerID, Feedback, Cancel_flag, Proceeding_flag, Received_flag, OrderDate)
            VALUES (1, 'Feedback 1', FALSE, TRUE, TRUE, '2024-05-16'), (2, 'Feedback 2', TRUE, FALSE, FALSE, '2024-05-15'), (3, 'Feedback 3', FALSE, TRUE, FALSE, '2024-05-11')
        """)

    def insert_computer_data(self, cursor):
        # Insert dummy data into the Computer table (two entries)
        cursor.execute("""
            INSERT INTO Computer (AdminID)
            VALUES (1), (1), (1), (1), (1), (1), (1), (1), (1), (1), (1), (1), (1), (1), (1), (1), (1), (1), (1), (1), (1), (1), (1), (1)
        """)

    def insert_buys_data(self, cursor):
        # Insert dummy data into the Buys table (two entries)
        cursor.execute("""
            INSERT INTO Buys (CustomerID, ComputerID)
            VALUES (1, 1), (2, 2), (3, 3)
        """)

    def insert_recommendation_data(self, cursor):
        # Insert dummy data into the Recommendation table (two entries)
        cursor.execute("""
            INSERT INTO Recommendation (ComputerID, ReceiverID)
            VALUES (1, 1), (2, 2), (3, 3)
        """)
        # Create Result_in table
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS Result_in (
                    RecomID INT,
                    ComputerID INT,
                    CustomerID INT,
                    FOREIGN KEY (RecomID) REFERENCES Recommendation(RecomID),
                    FOREIGN KEY (ComputerID) REFERENCES Recommendation(ComputerID),
                    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
                )
            """)

    def insert_ram_data(self, cursor):
    # Insert dummy data into the RAM table (two entries)
        cursor.execute("""
            INSERT INTO RAM (SerialNumber, Capacity)
            VALUES (7, 8), (8, 16), (9, 24)
            ON DUPLICATE KEY UPDATE Capacity = VALUES(Capacity);
        """)

    def insert_processing_unit_data(self, cursor):
        # Insert dummy data into the Processing_Unit table (two entries)
        cursor.execute("""
            INSERT INTO Processing_Unit (SerialNumber, ClockSpeed, Generation, CPU_flag, GPU_flag)
            VALUES (16, 3.2, 10, 0, 1), (17, 2.8, 9, 0, 1), (18, 2.3, 8, 0, 1), (19, 4.0, 11, 1, 0), (20, 3.8, 10, 1, 0), (21, 3.6, 9, 1, 0)
        """)

    def insert_storage_device_data(self, cursor):
        # Insert dummy data into the Storage_Device table (two entries)
        cursor.execute("""
            INSERT INTO Storage_Device (SerialNumber, WriteSpeed, Capacity, ReadSpeed, SSD_flag, HDD_flag)
            VALUES (10, 100, 512, 120, 1, 0), (11, 150, 1024, 80, 1, 0), (12, 50, 256, 160, 1, 0), (13, 50, 512, 40, 0, 1), (14, 60, 1024, 80, 0, 1), (15, 40, 256, 120, 0, 1)
        """)

    def insert_pre_assembled_data(self, cursor):
        # Insert dummy data into the Pre-assembled table (two entries)
        cursor.execute("""
            INSERT INTO Pre_assembled (ComputerID, RAM, Price, Processor, Name)
            VALUES (1, 123, 1200, 789, 'Lenovo'), (2, 456, 1500, 987, 'Hp'), (3, 461, 1600, 971, 'MSI')
        """)

    def insert_pre_assembled_io_data(self, cursor):
            # Insert dummy data into the Pre-assembled_IO table (two entries)
        cursor.execute("""
            INSERT INTO Pre_assembled_IO (ComputerID, IO)
            VALUES (1, 1), (2, 0), (3, 1)
        """)

    def insert_component_data(self, cursor):
        # Insert dummy data into the component table (two entries)
        cursor.execute("""
            INSERT INTO component (Price, Name)
            VALUES (100, 'Monitor 1'), (200, 'Monitor 2'), (300, 'Monitor 3'), (100, 'Keyboard 1'), (50, 'Keyboard 2'), (150, 'Keyboard 3'), (200, 'RAM 1'), (250, 'RAM 2'), (300, 'RAM 3'), (50, 'SSD 1'), (60, 'SSD 2'), (70, 'SSD 3'), (55, 'HDD 1'), (60, 'HDD 2'), (65, 'HDD 3'), (550, 'GPU 1'), (650, 'GPU 2'), (750, 'GPU 3'), (350, 'CPU 1'), (500, 'CPU 2'), (650, 'CPU 3')
        """)

    def insert_use_components_data(self, cursor):
        # Insert dummy data into the Use_components table (two entries)
        cursor.execute("""
            INSERT INTO Use_components (ComputerID, SerialNumber)
            VALUES (4, 1), (5, 2), (6, 3), (7, 4), (8, 5), (9, 6), (10, 7), (11, 8), (12, 9), (13, 10), (14, 11), (15, 12), (16, 13), (17, 14), (18, 15), (19, 16), (20, 17), (21, 18), (22, 19), (23, 20), (24, 21)
        """)

    def insert_monitor_data(self, cursor):
        # Insert dummy data into the Monitor table (two entries)
        cursor.execute("""
            INSERT INTO Monitor (SerialNumber)
            VALUES (1), (2), (3)
        """)

    def insert_keyboard_data(self, cursor):
        # Insert dummy data into the Keyboard table (two entries)
        cursor.execute("""
            INSERT INTO Keyboard (SerialNumber)
            VALUES (4), (5), (6)
        """)


        