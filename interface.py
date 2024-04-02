from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

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
        cursor.execute("INSERT INTO User_Accounts (Username, Password, User_Type) VALUES (%s, %s, %s)",
                       (username, password, user_type))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('list_user_accounts'))

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


if __name__ == '__main__':
    app.run(debug=True)
