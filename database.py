import mysql.connector
from mysql.connector import Error


def clear_tables(cursor):
    tables_to_drop = [
        "Transactions", "Feedback_Ratings", "RSVP", "Menu_Items", "Menu",
        "Food_Truck_Details", "Food_Truck", "Event_Details", "Attendee",
        "Event", "User_Accounts"
    ]

    for table in tables_to_drop:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
    print("All tables dropped successfully")


def create_tables(cursor):
    # SQL commands to execute
    create_table_commands = """

    -- User Accounts Table
    CREATE TABLE User_Accounts (
        User_ID INT PRIMARY KEY,
        Username VARCHAR(255) NOT NULL,
        Password VARCHAR(255) NOT NULL,
        User_Type VARCHAR(255)
    );

    -- Event Table
    CREATE TABLE Event (
        Event_ID INT PRIMARY KEY,
        Location VARCHAR(255),
        Contact_Info VARCHAR(255),
        Date DATE,
        Name VARCHAR(255)
    );

    -- Food Truck Table
    CREATE TABLE Food_Truck (
        Truck_ID INT PRIMARY KEY,
        Name VARCHAR(255),
        Contact_Info VARCHAR(255),
        Cuisine_Type VARCHAR(255),
        User_ID INT,
        Event_ID INT,
        FOREIGN KEY (User_ID) REFERENCES User_Accounts(User_ID),
        FOREIGN KEY (Event_ID) REFERENCES Event(Event_ID)
    );

    -- Attendee Table
    CREATE TABLE Attendee (
        Attendee_ID INT PRIMARY KEY,
        Name VARCHAR(255),
        Email VARCHAR(255),
        Phone_Number VARCHAR(255),
        User_ID INT,
        Event_ID INT,
        FOREIGN KEY (User_ID) REFERENCES User_Accounts(User_ID),
        FOREIGN KEY (Event_ID) REFERENCES Event(Event_ID)
    );

    -- Event Details Table
    CREATE TABLE Event_Details (
        Event_ID INT,
        Detail_ID INT PRIMARY KEY,
        Specific_Instructions TEXT,
        Event_Rules TEXT,
        FOREIGN KEY (Event_ID) REFERENCES Event(Event_ID)
    );

    -- Feedback & Ratings Table
    CREATE TABLE Feedback_Ratings (
        Feedback_ID INT PRIMARY KEY,
        Comments TEXT,
        Rating INT,
        Attendee_ID INT,
        Truck_ID INT,
        Event_ID INT,
        FOREIGN KEY (Attendee_ID) REFERENCES Attendee(Attendee_ID),
        FOREIGN KEY (Truck_ID) REFERENCES Food_Truck(Truck_ID),
        FOREIGN KEY (Event_ID) REFERENCES Event(Event_ID)
    );

    -- RSVP Table
    CREATE TABLE RSVP (
        RSVP_ID INT PRIMARY KEY,
        Attendee_ID INT,
        Event_ID INT,
        User_ID INT,
        FOREIGN KEY (Attendee_ID) REFERENCES Attendee(Attendee_ID),
        FOREIGN KEY (Event_ID) REFERENCES Event(Event_ID),
        FOREIGN KEY (User_ID) REFERENCES User_Accounts(User_ID)
    );

    -- Menu Table: has the check constraint for the price
    CREATE TABLE Menu (
        Menu_ID INT PRIMARY KEY,
        Item_Name VARCHAR(255),
        Truck_ID INT,
        Price DECIMAL(10, 2),
        CONSTRAINT Price_Above_Zero CHECK (Price >= 0),
        FOREIGN KEY (Truck_ID) REFERENCES Food_Truck(Truck_ID)
    );

    -- Menu Items Table
    CREATE TABLE Menu_Items (
        Menu_ID INT,
        Item_ID INT PRIMARY KEY,
        Description TEXT,
        Dietary_Info VARCHAR(255),
        FOREIGN KEY (Menu_ID) REFERENCES Menu(Menu_ID)
    );

    -- Food Truck Details Table
    CREATE TABLE Food_Truck_Details (
        Truck_ID INT,
        Detail_ID INT PRIMARY KEY,
        Owner_Details TEXT,
        Operational_Hours TEXT,
        FOREIGN KEY (Truck_ID) REFERENCES Food_Truck(Truck_ID)
    );

    -- Transactions Table
    CREATE TABLE Transactions (
        Transaction_ID INT PRIMARY KEY,
        Attendee_ID INT,
        Event_ID INT,
        Amount DECIMAL(10, 2),
        Transaction_Date DATE,
        FOREIGN KEY (Attendee_ID) REFERENCES Attendee(Attendee_ID),
        FOREIGN KEY (Event_ID) REFERENCES Event(Event_ID)
    );

    """

    for result in cursor.execute(create_table_commands, multi=True):
        pass
        # This is needed to ensure that all results are consumed

    # Commit changes
    conn.commit()


def get_all_tables(cursor):
    cursor.execute("SHOW TABLES")

    # Fetch and print all the results
    tables = cursor.fetchall()
    print("Tables in the database:")
    for table in tables:
        print(table[0])


def populate_tables(cursor):
    # User_Accounts
    cursor.execute("""
        INSERT INTO User_Accounts (User_ID, Username, Password, User_Type) VALUES
        (1, 'user1', 'pass1', 'Type1'),
        (2, 'user2', 'pass2', 'Type2'),
        (3, 'user3', 'pass3', 'Type3'),
        (4, 'user4', 'pass4', 'Type4'),
        (5, 'user5', 'pass5', 'Type5');
    """)

    # Event
    cursor.execute("""
        INSERT INTO Event (Event_ID, Location, Contact_Info, Date, Name) VALUES
        (1, 'Location1', 'Contact1', '2023-01-01', 'Event1'),
        (2, 'Location2', 'Contact2', '2023-01-02', 'Event2'),
        (3, 'Location3', 'Contact3', '2023-01-03', 'Event3'),
        (4, 'Location4', 'Contact4', '2023-01-04', 'Event4'),
        (5, 'Location5', 'Contact5', '2023-01-05', 'Event5');
    """)

    # Attendee
    cursor.execute("""
           INSERT INTO Attendee (Attendee_ID, Name, Email, Phone_Number, User_ID, Event_ID) VALUES
           (1, 'John Doe', 'john@example.com', '1234567890', 1, 1),
           (2, 'Jane Smith', 'jane@example.com', '0987654321', 2, 2),
           (3, 'Alice Brown', 'alice@example.com', '1122334455', 3, 3),
           (4, 'Bob Johnson', 'bob@example.com', '2233445566', 4, 4),
           (5, 'Charlie Davis', 'charlie@example.com', '3344556677', 5, 5);
       """)

    # Event_Details
    cursor.execute("""
        INSERT INTO Event_Details (Event_ID, Detail_ID, Specific_Instructions, Event_Rules) VALUES
        (1, 1, 'Instructions 1', 'Rules 1'),
        (2, 2, 'Instructions 2', 'Rules 2'),
        (3, 3, 'Instructions 3', 'Rules 3'),
        (4, 4, 'Instructions 4', 'Rules 4'),
        (5, 5, 'Instructions 5', 'Rules 5');
    """)

    # Food_Truck
    cursor.execute("""
            INSERT INTO Food_Truck (Truck_ID, Name, Contact_Info, Cuisine_Type, User_ID, Event_ID) VALUES
            (1, 'Truck A', '123-456-7890', 'American', 1, 1),
            (2, 'Truck B', '234-567-8901', 'Italian', 2, 2),
            (3, 'Truck C', '345-678-9012', 'Mexican', 3, 3),
            (4, 'Truck D', '456-789-0123', 'Japanese', 4, 4),
            (5, 'Truck E', '567-890-1234', 'French', 5, 5);
        """)

    # Feedback_Ratings
    cursor.execute("""
        INSERT INTO Feedback_Ratings (Feedback_ID, Comments, Rating, Attendee_ID, Truck_ID, Event_ID) VALUES
        (1, 'Good', 4, 1, 1, 1),
        (2, 'Excellent', 5, 2, 2, 2),
        (3, 'Average', 3, 3, 3, 3),
        (4, 'Poor', 2, 4, 4, 4),
        (5, 'Fair', 3, 5, 5, 5);
    """)

    # RSVP
    cursor.execute("""
        INSERT INTO RSVP (RSVP_ID, Attendee_ID, Event_ID, User_ID) VALUES
        (1, 1, 1, 1),
        (2, 2, 2, 2),
        (3, 3, 3, 3),
        (4, 4, 4, 4),
        (5, 5, 5, 5);
    """)

    # Menu
    cursor.execute("""
        INSERT INTO Menu (Menu_ID, Item_Name, Truck_ID, Price) VALUES
        (1, 'Burger', 1, 5.99),
        (2, 'Pizza', 2, 7.99),
        (3, 'Taco', 3, 3.99),
        (4, 'Sushi', 4, 9.99),
        (5, 'Pasta', 5, 8.99);
    """)
    # Menu_Items
    cursor.execute("""
        INSERT INTO Menu_Items (Menu_ID, Item_ID, Description, Dietary_Info) VALUES
        (1, 1, 'Delicious beef burger', 'Contains meat'),
        (2, 2, 'Cheese pizza with toppings', 'Vegetarian'),
        (3, 3, 'Spicy taco', 'Gluten-free'),
        (4, 4, 'Assorted sushi platter', 'Contains fish'),
        (5, 5, 'Italian pasta with sauce', 'Vegetarian');
    """)

    # Food_Truck_Details
    cursor.execute("""
            INSERT INTO Food_Truck_Details (Truck_ID, Detail_ID, Owner_Details, Operational_Hours) VALUES
            (1, 1, 'Owner 1 Details', '9am-5pm'),
            (2, 2, 'Owner 2 Details', '10am-6pm'),
            (3, 3, 'Owner 3 Details', '11am-7pm'),
            (4, 4, 'Owner 4 Details', '12pm-8pm'),
            (5, 5, 'Owner 5 Details', '8am-4pm');
        """)

    # Transactions
    cursor.execute("""
            INSERT INTO Transactions (Transaction_ID, Attendee_ID, Event_ID, Amount, Transaction_Date) VALUES
            (1, 1, 1, 100.00, '2023-01-01'),
            (2, 2, 2, 150.00, '2023-01-02'),
            (3, 3, 3, 200.00, '2023-01-03'),
            (4, 4, 4, 250.00, '2023-01-04'),
            (5, 5, 5, 300.00, '2023-01-05');
        """)

    conn.commit()
    print("Data inserted successfully into all tables")


tables = {
    'User_Accounts': 4,  # User_ID, Username, Password, User_Type
    'Event': 5,  # Event_ID, Location, Contact_Info, Date, Name
    'Food_Truck': 6,  # Truck_ID, Name, Contact_Info, Cuisine_Type, User_ID, Event_ID
    'Attendee': 6,  # Attendee_ID, Name, Email, Phone_Number, User_ID, Event_ID
    'Event_Details': 4,  # Event_ID, Detail_ID, Specific_Instructions, Event_Rules
    'Feedback_Ratings': 6,  # Feedback_ID, Comments, Rating, Attendee_ID, Truck_ID, Event_ID
    'RSVP': 4,  # RSVP_ID, Attendee_ID, Event_ID, User_ID
    'Menu': 4,  # Menu_ID, Item_Name, Truck_ID, Price
    'Menu_Items': 4,  # Menu_ID, Item_ID, Description, Dietary_Info
    'Food_Truck_Details': 4,  # Truck_ID, Detail_ID, Owner_Details, Operational_Hours
    'Transactions': 5  # Transaction_ID, Attendee_ID, Event_ID, Amount, Transaction_Date
}

table_pk = {
    'User_Accounts': 'User_ID',
    'Event': 'Event_ID',
    'Food_Truck': 'Truck_ID',
    'Attendee': 'Attendee_ID',
    'Event_Details': 'Detail_ID',
    'Feedback_Ratings': 'Feedback_ID',
    'RSVP': 'RSVP_ID',
    'Menu': 'Menu_ID',
    'Menu_Items': 'Item_ID',
    'Food_Truck_Details': 'Detail_ID',
    'Transactions': 'Transaction_ID'
}


def add_entry(curser, table_name, args=[]):
    if table_name in tables and tables[table_name] == len(args):
        # Create placeholders for the values
        placeholders = ', '.join(['%s'] * len(args))

        # Create the INSERT INTO statement
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"

        # Execute the query
        cursor.execute(insert_query, tuple(args))
    else:
        print(f"Error: The number of arguments does not match the number of columns in '{table_name}'.")


def delete_entry(cursor, table_name, primary_key_value):
    if table_name in tables:
        # Assuming the primary key is the first column
        primary_key_column = table_pk[table_name]  # This is the actual primary key column name
        delete_query = f"DELETE FROM {table_name} WHERE {primary_key_column} = %s"
        cursor.execute(delete_query, (primary_key_value,))
    else:
        print(f"Error: Table '{table_name}' not found.")


def get_entry(cursor, table_name, primary_key_value):
    if table_name in tables:
        # Assuming the primary key is the first column
        primary_key_column = table_pk[table_name]  # This is the actual primary key column name
        get_query = f"SELECT * FROM {table_name} WHERE {primary_key_column} = %s"
        cursor.execute(get_query, (primary_key_value,))
    else:
        print(f"Error: Table '{table_name}' not found.")


def update_entry(cursor, table_name, primary_key_value, update_values=[]):
    if table_name in tables and len(update_values) == tables[table_name] - 1:
        # Construct the SET part of the SQL query
        set_values = ', '.join([f"{column} = %s" for column in update_values.keys()])

        # Assuming the primary key is the first column
        primary_key_column = table_pk[table_name]  # This is the actual primary key column name
        update_query = f"UPDATE {table_name} SET {set_values} WHERE {primary_key_column} = %s"
        print("test")

        # Prepare the values for the SQL query
        update_values_list = list(update_values.values()) + [primary_key_value]

        # Execute the update query with parameters
        cursor.execute(update_query, update_values_list)
        conn.commit()  # Commit the transaction
        print("Entry updated successfully.")
    else:
        print(f"Error: Table '{table_name}' not found or incorrect number of update values.")

def get_truck_revenue(cursor, truck_id, event_id):
    try:
        # Drop the stored procedure if it already exists
        cursor.execute("DROP PROCEDURE IF EXISTS CalculateTotalRevenue")

        # Define the SQL code to create the stored procedure
        create_stored_procedure_query = """
        CREATE PROCEDURE CalculateTotalRevenue (IN truck_id INT, IN event_id INT, OUT total DECIMAL(10, 2))
        BEGIN
            SELECT SUM(Amount) INTO total
            FROM Transactions
            WHERE Truck_ID = truck_id AND Event_ID = event_id;
        END
        """

        # Execute the SQL code to create the stored procedure
        cursor.execute(create_stored_procedure_query)
        print("Stored procedure CalculateTotalRevenue created successfully")

        # Execute the stored procedure to retrieve truck revenue
        cursor.callproc("CalculateTotalRevenue", [truck_id, event_id, 0])

        # Fetch the result of the stored procedure
        cursor.execute("SELECT @total")
        total_revenue = cursor.fetchone()[0]

        return total_revenue

    except Error as e:
        print("Error while retrieving truck revenue:", e)

def describe_and_count_all_tables(cursor):
    for table_name in tables.keys():
        try:
            # Describe the table schema
            cursor.execute(f"DESC {table_name}")
            rows = cursor.fetchall()
            print(f"\nSchema for table '{table_name}':")
            for row in rows:
                print(row)

            # Count the total number of rows in the table
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"Total number of rows in '{table_name}': {count}")

        except Exception as e:
            print(f"Error while processing table '{table_name}':", e)
try:
    # Establish the database connection
    conn = mysql.connector.connect(
        host='34.150.151.166',
        user='root',
        passwd='Database123!',
        database='4750_project'
    )

    # Check if the connection was successful
    if conn.is_connected():
        print("Successfully connected to the database")

        # Create a cursor object
        cursor = conn.cursor()
        clear_tables(cursor)
        get_all_tables(cursor)
        create_tables(cursor)
        get_all_tables(cursor)
        populate_tables(cursor)

        describe_and_count_all_tables(cursor)

        # Testing add_entry function
        add_entry(cursor, 'User_Accounts', [6, 'user6', 'pass6', 'Type6'])

        # Testing get_entry function
        get_entry(cursor, 'User_Accounts', 6)
        print(cursor.fetchall())  # This should print the entry with User_ID = 6

        # Testing update_entry function
        update_entry(cursor, 'User_Accounts', 6, {'username': 'user7', 'password': 'pass7', 'user_type': 'Type7'})
        # get_entry(cursor, 'User_Accounts', 6)
        # print(cursor.fetchall())  # This should print the entry with User_ID = 6 updated

        # Testing delete_entry function
        delete_entry(cursor, 'User_Accounts', 6)

        # Verification: Check if the entry has been deleted
        get_entry(cursor, 'User_Accounts', 6)
        result = cursor.fetchall()
        if not result:
            print("Entry with User_ID = 6 has been successfully deleted.")
        else:
            print("Error: Entry with User_ID = 6 still exists after deletion.")

        # Need to insert values into truck table and event table
        # Testing get_truck_revenue function
        truck_id = 1
        event_id = 1
        revenue = get_truck_revenue(cursor, truck_id, event_id)
        print(f"Total revenue for truck {truck_id} at event {event_id}: ${revenue}")

except Error as e:
    print("Error while connecting to MySQL:", e)

"""
finally:
    cursor.close()
    conn.close()
"""