import sqlite3
import tkinter as tk
import csv
import os
import numpy as np
import pandas as pd


dbFileName = "Coursework.db"

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File {file_path} deleted successfully.")
    else:
        print(f"File {file_path} does not exist.")

delete_file(dbFileName)

def createDB():
    connection = sqlite3.connect(dbFileName)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Restaurant(
            RestaurantID INTEGER PRIMARY KEY,
            RestaurantName TEXT,
            LocationID INT,
            ManagerID INT,
            CuisineID INT,
            CategoryID INT,
            ZoneID INT,
            FOREIGN KEY (LocationID) References Location (LocationID),
            FOREIGN KEY (ManagerID) References Manager (ManagerID),
            FOREIGN KEY (CuisineID) References Cuisine (CuisineID),
            FOREIGN KEY (CategoryID) References Category (CategoryID),
            FOREIGN KEY (ZoneID) References Zone (ZoneID)
        )
    ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Manager (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Email TEXT,
                ManagerName TEXT,
                YearsAsManager INT
            )
    ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Cuisine (
                    CuisineID INTEGER PRIMARY KEY,
                    CuisineName TEXT UNIQUE
        )
    ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Category (
        CategoryID INTEGER PRIMARY KEY,
        CategoryName TEXT UNIQUE
    )
    ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Zone (
        ZoneID INTEGER PRIMARY KEY,
        ZoneName TEXT UNIQUE
    )
    ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Location (
        LocationID INTEGER PRIMARY KEY,
        Street TEXT,
        City TEXT,
        State TEXT,
        PostCode TEXT
    )
    ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Orders(
        OrderID TEXT PRIMARY KEY,
        OrderDate DATE,
        OrderAmount DECIMAL(10, 2),
        QuantityOfItems INT,
        DeliveryTimeTaken INT,
        CustomerRatingFood INT,
        CustomerID INTEGER REFERENCES Customer(CustomerID),
        RestaurantID INTEGER REFERENCES Restaurant(RestaurantID),
        CustomerRatingDelivery INT,
        PaymentMode TEXT,
        CardNumber TEXT
        )
    ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Customer(
        CustomerID INTEGER PRIMARY KEY,
        FirstName TEXT,
        LastName TEXT
    )
    ''')

    connection.commit()
    connection.close()

createDB()
    
def populateRestaurantDatabase():
    with open('restaurant_info.csv', newline='', encoding='utf-8') as csvFile:
        restaurantInfo = csv.DictReader(csvFile)
        restaurantInfo = list(restaurantInfo)

        for row in restaurantInfo:
            RestaurantID = row["RestaurantID"]
            RestaurantName = row["RestaurantName"]
            Cuisine = row["Cuisine"]
            Zone = row["Zone"]
            Category = row["Category"]
            Store = row["Store"]
            Manager = row["Manager"]
            Years_as_manager = row["Years_as_manager"]
            Email = row["Email"]
            Address = row["Address"].split(";")

            # Update Manager Information
            managerId = insertIntoTable('Manager', ['Email','ManagerName', 'YearsAsManager'], [Email, Manager, Years_as_manager])
            
            # Update Cuisine Information
            cuisineID = insertIntoTable('Cuisine', ['CuisineName'], [Cuisine])
            
            # Update Zone Information
            zoneid = insertIntoTable('Zone', ['ZoneName'], [Zone])
            
            # Update Manager Information
            categoryid = insertIntoTable('Category', ['CategoryName'], [Category])
            
            locationID = ""
            # Update Address Information
            if(len(Address) == 4):
                locationID = insertIntoTable('Location', ['Street', 'City', 'State', 'PostCode'], Address)
            elif (len(Address) == 3):

                street, city, state = Address
                postalCode = None

                locationID = insertIntoTable('Location', ['Street', 'City', 'State', 'PostCode'], [street,city,state,postalCode])
            else:
                print("Address length incorrect")

            # Update Manager Information
            restauntid = insertIntoTable('Restaurant', 
                                         ['RestaurantID', 'RestaurantName', 'ManagerID', 'CuisineID', "CategoryID", 'ZoneID', 'LocationID'], 
                                         [RestaurantID,RestaurantName,managerId,cuisineID,categoryid,zoneid,locationID]
            )

            # print(restauntid)

def populateOrdersDatabase():
    with open('Orders.csv', newline='', encoding='utf-8') as csvFile:
        orders = csv.DictReader(csvFile)
        orders = list(orders)

        for row in orders:
            orderId = row["Order ID"]
            firstName = row["First_Customer_Name"]
            lastName = row["Last_Customer_Name"]
            restauntId = row["Restaurant ID"]
            orderDate = row["Order Date"]
            quantity = row["Quantity of Items"]
            orderAmount = row["Order Amount"]
            paymentMode = row["Payment Mode"]
            deliveryTimeTaken = int(row["Delivery Time Taken (mins)"])
            foodRating = row["Customer Rating-Food"]
            deliveryRating = row["Customer Rating-Delivery"]
            creditCardNumber = row["Credit Card"]
            debitCardNumber= row["Debit Card"]
           
            df = pd.read_csv('Orders.csv')
   
            if (deliveryTimeTaken <= 0):
                deliveryTimeTaken = df['Delivery Time Taken (mins)'].mean(axis=0)

            cardNumber = None

            if(debitCardNumber):
                cardNumber = debitCardNumber
            else:
                cardNumber = creditCardNumber

            # Update Customer Information
            customerID = insertIntoTable('Customer', ['FirstName', 'LastName'], [firstName, lastName])

            # Update Order Information
            savetoOrderDB = insertIntoTable('Orders', 
                ['OrderID', 'OrderDate', 'OrderAmount', 'QuantityOfItems', 'DeliveryTimeTaken', 'CustomerRatingFood', 'CustomerID', 'RestaurantID', 'CustomerRatingDelivery', 'PaymentMode', 'CardNumber'], 
                [orderId, orderDate, orderAmount, quantity, deliveryTimeTaken, foodRating, customerID, restauntId, deliveryRating, paymentMode, cardNumber])

def find_id(table_name, column_names, values):
    connection = sqlite3.connect('Coursework.db')
    cursor = connection.cursor()

    # Construct the SELECT query dynamically
    select_query = f'SELECT * FROM {table_name} WHERE '
    conditions = ' AND '.join(f'{column} = ?' for column in column_names)
    select_query += conditions

    # print(select_query)
    # Execute the query with the provided values
    result = cursor.execute(select_query, values).fetchone()

    connection.close()

    return result[0] if result else None

def insertIntoTable(table_name, columns, values):

    existingID = find_id(table_name,columns,values)

    # Establish a connection to the SQLite database
    connection = sqlite3.connect(dbFileName)
    cursor = connection.cursor()

    if(existingID):
        return existingID
    else:
        # Prepare the query for inserting data
        if(values[0] != ""):
            columns_str = ', '.join(columns)
            placeholders = ', '.join(['?' for _ in values])
            query = f'INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})'

            # Execute the insert query
            cursor.execute(query, values)
            
            # Get the last inserted row's primary key
            
            new_id = cursor.lastrowid
            
            # Commit the changes and close the connection
            connection.commit()
            connection.close()
            
            return new_id
        
populateRestaurantDatabase()
populateOrdersDatabase()