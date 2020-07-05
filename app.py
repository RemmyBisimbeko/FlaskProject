from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from RestructuresData import Restructures
from ApplicationsData import Applications
from EnrollmentsData import Enrollments

from flask_mysqldb import MySQL
# Import wtforms and  Each Type of Field to be used
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
# Import passlib hash
from passlib.hash import sha256_crypt

# Init App
app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345etc'
app.config['MYSQL_DB'] = 'flaskproject'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# Init MySQL
mysql = MySQL(app)


# Create Variable equal to Function imported 
Restructures = Restructures()
Applications = Applications()
Enrollments = Enrollments()

# Home Route
@app.route('/')
def home():
    return render_template('home.html')

# About Route
@app.route('/about')
def about():
    return render_template('about.html')

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    # Check if GET or POST request, and make sure everything is validated
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        # Encryt password before sending it, submiting it
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create Cursor, used to execute commands(mysql)
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close the Connection
        cur.close()

        # Set flash message once user is registered  - 'message', 'category'
        flash('You have been registered Successfully, please log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check method
    if request.method == 'POST':
        # If form is submited, GET username and password from the form
        # GET form fields, no need for using wtf forms
        username = request.form['username']
        # Candidate-user input, bse we want to compare with password which is in the db
        passsword_candidate = request.form['password']

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute Query, GET user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        # Check result, >0 - any rows found
        if result > 0:
            # Get Stored hash
            data = cur.fetchone()
            # Get password from that fetch
            password = data['password']

            # Compare the passwords
            if sha256_crypt.verify(passsword_candidate, password):
                app.logger.info('PASSWORD MATCHED')
        else:
            app.logger.info('NO USER FOUND')

    return render_template('login.html')

# Restructures Route
@app.route('/restructures')
def restructures():
    return render_template('restructures.html', restructures = Restructures)

# Single Restructure Route
@app.route('/restructure/<string:id>')
def restructure(id):
    return render_template('restructure.html', id=id)

# Applications Route
@app.route('/applications')
def applications():
    return render_template('applications.html', applications = Applications)

# Single Application Route
@app.route('/application/<string:id>')
def application(id):
    return render_template('application.html', id=id)

# Enrollments Route
@app.route('/enrollments')
def enrollments():
    return render_template('enrollments.html', enrollments = Enrollments)

# Single Enrollment Route
@app.route('/enrollment/<string:id>')
def enrollment(id):
    return render_template('enrollment.html', id=id)

# Run Server
if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)