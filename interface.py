from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import database as db

app = Flask(__name__)
app.secret_key = 'Database_Project_2024'  # Needed for session management



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
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT Event_ID, Name, Location, Date, Contact_Info FROM Event')
    raw_events = cursor.fetchall()
    events = [
        (event[0], event[1], event[2], event[3].strftime('%Y-%m-%d'), event[4]) if isinstance(event[3], datetime) else event
        for event in raw_events
    ]
    cursor.close()
    conn.close()
    return render_template('home.html', events=events)


@app.route('/list_attendees')
def list_attendees():
    if 'role' not in session or session['role'] != 'Event Manager':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('dashboard'))

    conn = get_db_connection()
    if conn is None:
        flash('Failed to connect to the database', 'error')
        return redirect(url_for('dashboard'))

    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.Attendee_ID, a.Name, a.Email, a.Phone_Number, e.Name AS Event_Name
        FROM Attendee AS a
        JOIN Event AS e ON a.Event_ID = e.Event_ID
        ORDER BY e.Date DESC, a.Name
    """)
    attendees = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('list_attendees.html', attendees=attendees)

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
        #db.clear_tables(conn, cursor)
        #db.create_tables(conn, cursor)
        db.add_entry(conn, cursor, 'User_Accounts', {'Username': username, 'Password': hashed_password, 'User_Type': user_type})
        db.describe_and_count_all_tables(cursor)
        db.print_all_tables_data(cursor)
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_user.html')


@app.route('/index')
def index():
    return render_template('index.html')

def check_user_credentials(username, password):
    conn = get_db_connection()
    if conn is None:
        return None
    cursor = conn.cursor()

    try:
        # SQL query to find the user with the given username
        query = "SELECT User_ID, Username, Password, User_Type FROM User_Accounts WHERE Username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            return {
                'User_ID': user[0],
                'Username': user[1],
                'User_Type': user[3]
            }
        return None
    finally:
        cursor.close()
        conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = check_user_credentials(username, password)
        if user:
            session['username'] = user['Username']
            session['user_id'] = user['User_ID']
            session['role'] = user['User_Type']
            flash('Login successful!', category='success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', category='error')

    return render_template('login.html')


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

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

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

@app.route('/event_details')
def event_details():
    event_id = request.args.get('event_id')
    if not event_id:
        flash('No event specified.', 'error')
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch event details
    cursor.execute('SELECT Name, Location, Date, Contact_Info FROM Event WHERE Event_ID = %s', (event_id,))
    event = cursor.fetchone()

    # Fetch food trucks attending this event
    cursor.execute('SELECT Truck_ID, Name, Cuisine_Type FROM Food_Truck WHERE Event_ID = %s', (event_id,))
    food_trucks = cursor.fetchall()

    # Fetch menus and reviews for each food truck
    menus = {}
    reviews = {}
    for truck in food_trucks:
        cursor.execute('SELECT Menu_ID, Item_Name, Price FROM Menu WHERE Truck_ID = %s', (truck[0],))
        menus[truck[1]] = cursor.fetchall()  # Using truck name as key

        # Fetch reviews for each truck
        cursor.execute('SELECT Comments, Rating FROM Feedback_Ratings WHERE Truck_ID = %s', (truck[0],))
        reviews[truck[1]] = cursor.fetchall()

    cursor.close()
    conn.close()

    # Make sure to pass event_id to the template
    return render_template('event_details.html', event=event, food_trucks=food_trucks, menus=menus, reviews=reviews, event_id=event_id)


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
    if 'role' not in session or session['role'] != 'Attendee':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Extract feedback data from form
        comments = request.form.get('comments')
        rating = request.form.get('rating')
        attendee_id = request.form.get('attendee_id')
        truck_id = request.form.get('truck_id')
        event_id = request.form.get('event_id')

        conn = get_db_connection()
        cursor = conn.cursor()

        # Add the feedback to the database
        db.add_entry(conn, cursor, 'Feedback_Ratings',
                     {'Comments': comments, 'Rating': rating, 'Attendee_ID': attendee_id, 'Truck_ID': truck_id,
                      'Event_ID': event_id})

        cursor.close()
        conn.close()
        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for('dashboard'))

    # Load the feedback form
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

@app.route('/submit_truck_review/<int:truck_id>/<int:event_id>', methods=['GET', 'POST'])
def submit_truck_review(truck_id, event_id):
    if 'role' not in session or session['role'] != 'Attendee':
        flash('You must be logged in as an attendee to review trucks.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        comments = request.form['comments']
        rating = request.form['rating']
        attendee_id = request.form['attendee_id']  # This should match session['user_id'], could double-check for security
        truck_id = request.form['truck_id']        # Passed via hidden form field
        event_id = request.form['event_id']        # Passed via hidden form field

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO Feedback_Ratings (Comments, Rating, Attendee_ID, Truck_ID, Event_ID) VALUES (%s, %s, %s, %s, %s)',
            (comments, rating, attendee_id, truck_id, event_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Your review has been submitted.', 'success')
        return redirect(url_for('event_details', event_id=event_id))

    return render_template('submit_truck_review.html', truck_id=truck_id, event_id=event_id)

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