from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
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

        # Hash the password
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Call the add_entry function to add the new user to the database
        db.clear_tables(conn, cursor)
        db.create_tables(conn, cursor)
        db.add_entry(conn, cursor, 'User_Accounts', {'Username': username, 'Password': hashed_password, 'User_Type': user_type})
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
        name = request.form['name']
        contact_info = request.form['contact_info']
        cuisine_type = request.form['cuisine_type']
        user_id = request.form['user_id']
        event_id = request.form.get('event_id') or None  # Optional field, set to None if not provided

        conn = get_db_connection()
        cursor = conn.cursor()

        # Call the add_entry function to add the new user to the database
        db.add_entry(conn, cursor, 'Food_Truck',
                     {'Name': name, 'Contact_Info': contact_info, 'Cuisine_Type': cuisine_type, 'User_ID':user_id, 'Event_ID':event_id})

        db.print_all_tables_data(cursor)
        cursor.close()
        conn.close()
        return redirect(url_for('index'))


    # Load the registration form
    return render_template('register_truck.html')

# Route for attendee registration for an event
@app.route('/register_attendee', methods=['GET', 'POST'])
def register_attendee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        user_id = request.form.get('user_id') or None  # Optional field
        event_id = request.form['event_id']

        conn = get_db_connection()
        cursor = conn.cursor()

        db.add_entry(conn, cursor, 'Attendee',
                     {'Name': name,
                    'Email': email,
                    'Phone_Number': phone_number,
                    'User_ID': user_id,  # Handle None for optional User_ID
                    'Event_ID': event_id})

        db.print_all_tables_data(cursor)
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

    # Load the registration form
    return render_template('register_attendee.html')


@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        location = request.form['location']
        contact_info = request.form['contact_info']
        event_date = request.form['date']
        name = request.form['name']

        conn = get_db_connection()
        cursor = conn.cursor()

        db.add_entry(conn, cursor, 'Event',
                     {'Location': location, 'Contact_Info': contact_info, 'Date': event_date, 'Name': name
                      })

        db.print_all_tables_data(cursor)
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

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
        cursor = conn.cursor()

        db.add_entry(conn, cursor, 'Feedback_Ratings',
                     {'Comments': comments, 'Rating': rating, 'Attendee_ID': attendee_id, 'Truck_ID': truck_id, 'Event_ID': event_id
                      })

        db.print_all_tables_data(cursor)
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('feedback.html')

@app.route('/add_menu', methods=['GET', 'POST'])
def add_menu():
    if request.method == 'POST':
        item_name = request.form['item_name']
        truck_id = request.form['truck_id']
        price = request.form['price']

        conn = get_db_connection()
        cursor = conn.cursor()

        db.add_entry(conn, cursor, 'Menu',
                     {'Item_Name': item_name, 'Truck_ID': truck_id, 'price': price
                      })

        db.print_all_tables_data(cursor)
        cursor.close()
        conn.close()
        return redirect(url_for('index'))


    return render_template('add_menu.html')

@app.route('/edit_menu_item', methods=['GET', 'POST'])
def edit_menu_item_details():
    if request.method == 'POST':
        menu_id = request.form['menu_id']
        description = request.form['description']
        dietary_info = request.form['dietary_info']

        conn = get_db_connection()
        cursor = conn.cursor()

        db.add_entry(conn, cursor, 'Menu_Items',
                     {'Menu_ID': menu_id, 'Description': description, 'dietary_info': dietary_info
                      })

        db.print_all_tables_data(cursor)
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('edit_menu_item.html')


@app.route('/food_truck_details', methods=['GET', 'POST'])
def food_truck_details():
    if request.method == 'POST':
        truck_id = request.form['truck_id']
        owner_details = request.form['owner_details']
        operational_hours = request.form['operational_hours']

        conn = get_db_connection()
        cursor = conn.cursor()

        db.add_entry(conn, cursor, 'Food_Truck_Details',
                     {'Truck_ID': truck_id, 'Owner_Details': owner_details, 'Operational_Hours': operational_hours
                      })

        db.print_all_tables_data(cursor)
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('food_truck_details.html')



if __name__ == '__main__':
    app.run(debug=True)