from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Insert dummy data into MySQL tables'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Insert dummy data into tables
            self.insert_admin_data(cursor)
            self.insert_customer_data(cursor)
            self.insert_records_data(cursor)
            self.insert_ram_data(cursor)
            self.insert_processing_unit_data(cursor)
            self.insert_storage_device_data(cursor)
            self.insert_component_data(cursor)
            self.insert_monitor_data(cursor)
            self.insert_computer_data(cursor)
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
            VALUES (1, '9876543210')
        """)

        # Insert dummy data into the Cust_address table
        cursor.execute("""
            INSERT INTO Cust_address (CustomerID, Address)
            VALUES (1, '456 Elm St')
        """)

        # Insert dummy data into the Cust_phone table
        cursor.execute("""
            INSERT INTO Cust_phone (CustomerID, Phone)
            VALUES (1, '987-654-3210')
        """)


    def insert_records_data(self, cursor):
    # Insert dummy data into the Records table (two entries)
        cursor.execute("""
            INSERT INTO Records (CustomerID, Feedback, Cancel_flag, Proceeding_flag, Received_flag, OrderDate)
            VALUES (1, 'Feedback 1', FALSE, TRUE, TRUE, '2024-05-16')
        """)

        cursor.execute("""
            INSERT INTO Records (CustomerID, Feedback, Cancel_flag, Proceeding_flag, Received_flag, OrderDate)
            VALUES (2, 'Feedback 2', TRUE, FALSE, FALSE, '2024-05-15')
        """)

    def insert_computer_data(self, cursor):
        # Insert dummy data into the Computer table (two entries)
        cursor.execute("""
            INSERT INTO Computer (AdminID)
            VALUES (1), (1), (1)
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
            VALUES (123, 8), (456, 16)
            ON DUPLICATE KEY UPDATE Capacity = VALUES(Capacity);
        """)

    def insert_processing_unit_data(self, cursor):
        # Insert dummy data into the Processing_Unit table (two entries)
        cursor.execute("""
            INSERT INTO Processing_Unit (SerialNumber, ClockSpeed, Generation, CPU_flag, GPU_flag)
            VALUES (789, 3.2, 10, 1, 0), (987, 2.8, 9, 1, 1)
            ON DUPLICATE KEY UPDATE ClockSpeed = VALUES(ClockSpeed), Generation = VALUES(Generation), CPU_flag = VALUES(CPU_flag), GPU_flag = VALUES(GPU_flag)
        """)

    def insert_storage_device_data(self, cursor):
        # Insert dummy data into the Storage_Device table (two entries)
        cursor.execute("""
            INSERT INTO Storage_Device (SerialNumber, WriteSpeed, Capacity, ReadSpeed, SSD_flag, HDD_flag)
            VALUES (654, 100, 512, 120, 1, 0), (321, 50, 1024, 80, 0, 1)
            ON DUPLICATE KEY UPDATE WriteSpeed = VALUES(WriteSpeed), Capacity = VALUES(Capacity), ReadSpeed = VALUES(ReadSpeed), SSD_flag = VALUES(SSD_flag), HDD_flag = VALUES(HDD_flag)
        """)

    def insert_pre_assembled_data(self, cursor):
        # Insert dummy data into the Pre-assembled table (two entries)
        cursor.execute("""
            INSERT INTO Pre_assembled (ComputerID, RAM, Price, Processor, Storage, Name)
            VALUES (1, 123, 1200, 789, 654, 'Lenovo'), (2, 456, 1500, 987, 321, 'Hp'), (3, 461, 1600, 971, 521, 'MSI')
            ON DUPLICATE KEY UPDATE RAM = VALUES(RAM), Price = VALUES(Price), Processor = VALUES(Processor), Storage = VALUES(Storage), Name = VALUES(Name)
        """)

    def insert_pre_assembled_io_data(self, cursor):
            # Insert dummy data into the Pre-assembled_IO table (two entries)
        cursor.execute("""
            INSERT INTO Pre_assembled_IO (ComputerID, IO)
            VALUES (1, 1), (2, 0)
            ON DUPLICATE KEY UPDATE IO = VALUES(IO)
        """)

    def insert_component_data(self, cursor):
        # Insert dummy data into the component table (two entries)
        cursor.execute("""
            INSERT INTO component (Price, Name)
            VALUES (100, 'Component 1'), (200, 'Component 2'), (300, 'Component 3')
        """)

    def insert_use_components_data(self, cursor):
        # Insert dummy data into the Use_components table (two entries)
        cursor.execute("""
            INSERT INTO Use_components (ComputerID, SerialNumber)
            VALUES (1, 1), (2, 2), (3, 3), (4, 4)
        """)

    def insert_monitor_data(self, cursor):
        # Insert dummy data into the Monitor table (two entries)
        cursor.execute("""
            INSERT INTO Monitor (SerialNumber)
            VALUES (1), (2)
            ON DUPLICATE KEY UPDATE SerialNumber = VALUES(SerialNumber)
        """)

    def insert_keyboard_data(self, cursor):
        # Insert dummy data into the Keyboard table (two entries)
        cursor.execute("""
            INSERT INTO Keyboard (SerialNumber)
            VALUES (3), (4)
            ON DUPLICATE KEY UPDATE SerialNumber = VALUES(SerialNumber)
        """)


        