from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error
import database as db

app = Flask(__name__)


def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='34.150.151.166',
            user='root',
            passwd='Database123!',
            database='4750_project'
        )
        return conn
    except Error as e:
        print("Error while connecting to MySQL:", e)
        return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user_accounts')
def list_user_accounts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User_Accounts")
    user_accounts = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('user_accounts.html', user_accounts=user_accounts)


@app.route('/add_user', methods=('GET', 'POST'))
def add_user():
    if request.method == 'POST':
        # Extract data from form
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Call the add_entry function to add the new user to the database
        db.clear_tables(conn, cursor)
        db.create_tables(conn, cursor)
        db.add_entry(conn, cursor, 'User_Accounts', {'Username': username, 'Password': password, 'User_Type': user_type})
        db.describe_and_count_all_tables(cursor)
        db.print_all_tables_data(cursor)
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_user.html')

# Route to view upcoming events
@app.route('/upcoming_events')
def view_upcoming_events():
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Event WHERE Date >= CURDATE()")
        events = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('upcoming_events.html', events=events)
    else:
        return "Failed to connect to the database"

# Route for food truck registration for an event
@app.route('/register_truck', methods=['GET', 'POST'])
def register_truck():
    if request.method == 'POST':
        truck_id = request.form['truck_id']
        event_id = request.form['event_id']


    # Load the registration form
    return render_template('register_truck.html')

# Route for attendee registration for an event
@app.route('/register_attendee', methods=['GET', 'POST'])
def register_attendee():
    if request.method == 'POST':
        attendee_id = request.form['attendee_id']
        event_id = request.form['event_id']


    # Load the registration form
    return render_template('register_attendee.html')


@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        location = request.form['location']
        contact_info = request.form['contact_info']
        date = request.form['date']
        name = request.form['name']

        conn = get_db_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Event (Location, Contact_Info, Date, Name) VALUES (%s, %s, %s, %s)",
                           (location, contact_info, date, name))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('view_upcoming_events'))  # Redirect to the events view
        else:
            return "Failed to connect to the database"

    return render_template('create_events.html')

@app.route('/submit_feedback', methods=['GET', 'POST'])
def submit_feedback():
    if request.method == 'POST':
        comments = request.form.get('comments')
        rating = request.form.get('rating')
        attendee_id = request.form.get('attendee_id')
        truck_id = request.form.get('truck_id')
        event_id = request.form.get('event_id')

        conn = get_db_connection()
        if conn is not None:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO Feedback_Ratings (Comments, Rating, Attendee_ID, Truck_ID, Event_ID) 
                    VALUES (%s, %s, %s, %s, %s)
                    """, (comments, rating, attendee_id, truck_id, event_id))
                conn.commit()
                message = "Feedback submitted successfully."
            except mysql.connector.Error as e:
                message = f"Error submitting feedback: {e}"
            finally:
                cursor.close()
                conn.close()
            return message  # Or redirect to a confirmation/thank you page
        else:
            return "Failed to connect to the database"

    return render_template('feedback.html')

@app.route('/add_menu', methods=['GET', 'POST'])
def add_menu_item():
    if request.method == 'POST':
        item_name = request.form['item_name']
        truck_id = request.form['truck_id']
        price = request.form['price']

        conn = get_db_connection()
        if conn is not None:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO Menu (Item_Name, Truck_ID, Price) 
                    VALUES (%s, %s, %s)
                    """, (item_name, truck_id, price))
                conn.commit()
                message = "Menu item added successfully."
            except mysql.connector.Error as e:
                message = f"Error adding menu item: {e}"
            finally:
                cursor.close()
                conn.close()
            return message
        else:
            return "Failed to connect to the database"

    return render_template('add_menu.html')

@app.route('/edit_menu_item', methods=['GET', 'POST'])
def edit_menu_item_details():
    if request.method == 'POST':
        item_id = request.form['item_id']
        description = request.form['description']
        dietary_info = request.form['dietary_info']

        conn = get_db_connection()
        if conn is not None:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    UPDATE Menu_Items
                    SET Description = %s, Dietary_Info = %s
                    WHERE Item_ID = %s
                    """, (description, dietary_info, item_id))
                conn.commit()
                message = "Menu item details updated successfully."
            except mysql.connector.Error as e:
                message = f"Error updating menu item details: {e}"
            finally:
                cursor.close()
                conn.close()
            return message
        else:
            return "Failed to connect to the database"

    return render_template('edit_menu_item.html')


@app.route('/food_truck_details', methods=['GET', 'POST'])
def food_truck_details():
    if request.method == 'POST':
        truck_id = request.form['truck_id']
        detail_id = request.form['detail_id']
        owner_details = request.form['owner_details']
        operational_hours = request.form['operational_hours']

        conn = get_db_connection()
        if conn is not None:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO Food_Truck_Details (Truck_ID, Detail_ID, Owner_Details, Operational_Hours) 
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    Owner_Details = VALUES(Owner_Details), 
                    Operational_Hours = VALUES(Operational_Hours)
                    """, (truck_id, detail_id, owner_details, operational_hours))
                conn.commit()
                message = "Food truck details added/updated successfully."
            except mysql.connector.Error as e:
                message = f"Error processing food truck details: {e}"
            finally:
                cursor.close()
                conn.close()
            return message
        else:
            return "Failed to connect to the database"

    return render_template('food_truck_details.html')



if __name__ == '__main__':
    app.run(debug=True)
