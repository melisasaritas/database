from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Create tables in the MySQL database'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Create Administration table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Administration (
                    AdminId INT AUTO_INCREMENT PRIMARY KEY,
                    BankAccount VARCHAR(100) NOT NULL,
                    AdminUsername VARCHAR(100) NOT NULL,
                    AdminPassword VARCHAR(100) NOT NULL
                )
            """)

            # Create Admin_Address table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Admin_Address (
                    AdminId INT,
                    Address VARCHAR(100) NOT NULL,
                    PRIMARY KEY (AdminID, Address),
                    FOREIGN KEY (AdminId) REFERENCES Administration(AdminId)
                )
            """)

            # Create Admin_Phone table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Admin_Phone (
                    AdminId INT,
                    Phone VARCHAR(100) NOT NULL,
                    PRIMARY KEY (AdminID, Phone),
                    FOREIGN KEY (AdminId) REFERENCES Administration(AdminId)
                )
            """)

            # Create Customer table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Customer (
                    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
                    Username VARCHAR(100) NOT NULL,
                    Password VARCHAR(100) NOT NULL
                )
            """)

            # Create Cust_BankAcc table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Cust_BankAcc (
                    CustomerID INT,
                    BankAccount VARCHAR(100) NOT NULL,
                    PRIMARY KEY (CustomerID, BankAccount),
                    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
                )
            """)

            # Create Cust_address table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Cust_address (
                    CustomerID INT,
                    Address VARCHAR(100) NOT NULL,
                    PRIMARY KEY (CustomerID, Address), 
                    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
                )
            """)

            # Create Cust_phone table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Cust_phone (
                    CustomerID INT,
                    Phone VARCHAR(100) NOT NULL,
                    PRIMARY KEY (CustomerID, Phone),
                    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
                )
            """)

            # Create Records table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Records (
                    RecordID INT AUTO_INCREMENT PRIMARY KEY,
                    CustomerID INT,
                    Feedback TEXT,
                    Cancel_flag BOOLEAN,
                    Proceeding_flag BOOLEAN,
                    Received_flag BOOLEAN,
                    OrderDate DATE, 
                    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Computer (
                    ComputerID INT AUTO_INCREMENT PRIMARY KEY,
                    AdminID INT,
                    FOREIGN KEY (AdminID) REFERENCES Administration(AdminId)
                )
            """)

            # Create Buys table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Buys (
                    CustomerID INT,
                    ComputerID INT,
                    PRIMARY KEY (CustomerID, ComputerID), 
                    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
                    FOREIGN KEY (ComputerID) REFERENCES Computer(ComputerID)
                )
            """)

            # Create Recommendation table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Recommendation (
                    RecomID INT AUTO_INCREMENT PRIMARY KEY,
                    ComputerID INT,
                    ReceiverID INT, 
                    FOREIGN KEY (ComputerID) REFERENCES Computer(ComputerID)
                )
            """)

            # Create component table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS component (
                    SerialNumber INT AUTO_INCREMENT PRIMARY KEY,
                    Price FLOAT,
                    Name VARCHAR(100) NOT NULL
                )
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

            # Create RAM table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS RAM (
                    SerialNumber INT PRIMARY KEY,
                    Capacity INT,
                    FOREIGN KEY (SerialNumber) REFERENCES component(SerialNumber)
                )
            """)

            # Create Computer table

            # Create Processing_Unit table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Processing_Unit (
                    SerialNumber INT PRIMARY KEY,
                    ClockSpeed FLOAT,
                    Generation INT,
                    CPU_flag BOOLEAN,
                    GPU_flag BOOLEAN,
                    FOREIGN KEY (SerialNumber) REFERENCES component(SerialNumber)
                )
            """)

            # Create Storage_Device table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Storage_Device (
                    SerialNumber INT PRIMARY KEY,
                    WriteSpeed FLOAT,
                    Capacity INT,
                    ReadSpeed FLOAT,
                    SSD_flag BOOLEAN,
                    HDD_flag BOOLEAN,
                    FOREIGN KEY (SerialNumber) REFERENCES component(SerialNumber)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Pre_assembled (
                    ComputerID INT PRIMARY KEY,
                    RAM INT,
                    Price FLOAT,
                    Processor INT,
                    Type INT,
                    Name VARCHAR(100) NOT NULL,
                    FOREIGN KEY (ComputerID) REFERENCES Computer(ComputerID)
                )
            """)

            # Create Pre-assembled_IO table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Pre_assembled_IO (
                    ComputerID INT,
                    IO INT,
                    PRIMARY KEY (ComputerID, IO),
                    FOREIGN KEY (ComputerID) REFERENCES Computer(ComputerID)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS custom_made (
                   ComputerID INT,
                   PRIMARY KEY (ComputerID),
                   FOREIGN KEY (ComputerID) REFERENCES Computer(ComputerID)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pre_assembled_storage (
                    ComputerID INT,
                    Storage VARCHAR(100) NOT NULL,
                    PRIMARY KEY (ComputerID, Storage),
                    FOREIGN KEY (ComputerID) REFERENCES Computer(ComputerID)
                )
            """)

            # Create Use_components table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Use_components (
                    ComputerID INT,
                    SerialNumber INT,
                    PRIMARY KEY (ComputerID, SerialNumber),
                    FOREIGN KEY (ComputerID) REFERENCES Computer(ComputerID),
                    FOREIGN KEY (SerialNumber) REFERENCES Component(SerialNumber)
                )
            """)

            # Create Monitor table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Monitor (
                    SerialNumber INT PRIMARY KEY,
                    FOREIGN KEY (SerialNumber) REFERENCES component(SerialNumber)
                )
            """)

            # Create Keyboard table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Keyboard (
                    SerialNumber INT PRIMARY KEY,
                    FOREIGN KEY (SerialNumber) REFERENCES component(SerialNumber)
                )
            """)
