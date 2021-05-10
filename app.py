import os
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
# from RestructuresData import Restructures
# from ApplicationsData import Applications
# from EnrollmentsData import Enrollments
# from CrosssellsData import Crosssells

from flask_mysqldb import MySQL
# Import wtforms and  Each Type of Field to be used
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
# Import passlib hash
from passlib.hash import sha256_crypt
# Bring wraps in
from functools import wraps

# Init App
app = Flask(__name__)
app.secret_key = 'secret123'
app.config['SESSION_TYPE'] = 'filesystem'

# Config MySQL
app.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST")
app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.environ.get("MYSQL_DB")
app.config['MYSQL_CURSORCLASS'] = os.environ.get("MYSQL_CURSORCLASS")
# Init MySQL
mysql = MySQL(app)


# Create Variable equal to Function imported 
# Restructures = Restructures()
# Applications = Applications()
# Enrollments = Enrollments()
# Crosssells = Crosssells()

# Home Route
@app.route('/')
def home():
    return render_template('home.html')

# Cross Sells Route
@app.route('/crosssells')
def crosssells():
    # Create  Cursor
    cur = mysql.connection.cursor()

    # Get Cross Sells
    result = cur.execute("SELECT * FROM crosssells")

    # Set Cross Sell Variable and set it to all in Dictionary form
    crosssells = cur.fetchall()

    if result > 0:
        return render_template('crosssells.html', crosssells=crosssells)
    else:
        msg = 'No Cross Sells Yet'
        return render_template('crosssells.html', msg=msg)

    # Close Connection
    cur.close()

# Single Cross Sell Route
@app.route('/crosssell/<string:id>')
def crosssell(id):
    # Create  Cursor
    cur = mysql.connection.cursor()

    # Get Cross Sell
    result = cur.execute("SELECT * FROM crosssells WHERE id=%s", [id ])

    # Set Cross Sell Variable and set it to all in Dictionary form
    crosssell = cur.fetchone()

    return render_template('crosssell.html', crosssell=crosssell)

# Single HR Issue Route
@app.route('/hrissue/<string:id>')
def hrissue(id):
    # Create  Cursor
    cur = mysql.connection.cursor()

    # Get HR Issue
    result = cur.execute("SELECT * FROM hrissues WHERE id=%s", [id ])

    # Set HR Issues Variable and set it to all in Dictionary form
    hrissue = cur.fetchone()

    return render_template('hrissue.html', hrissue=hrissue)

# HR Issues Route
@app.route('/hrissues')
def hrissues():
     # Create  Cursor
    cur = mysql.connection.cursor()

    # Get HR Issues
    result = cur.execute("SELECT * FROM hrissues")

    # Set HR Issue Variable and set it to all in Dictionary form
    hrissues = cur.fetchall()

    if result > 0:
        return render_template('hrissues.html', hrissues=hrissues)
    else:
        msg = 'No HR Issues Yet'
        return render_template('hrissues.html', msg=msg)

    # Close Connection
    cur.close()

# About Route
@app.route('/about')
def about():
    return render_template('about.html')

# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

# User Register
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
                # Passes password check
                # app.logger.info('PASSWORD MATCHED')
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return  redirect(url_for('dashboard'))
            else:
                error='Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            # app.logger.info('NO USER FOUND')
            error='Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # Check Logic
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You are not Authorised, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout Route
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Cross Sell Dashboard Route
@app.route('/dashboard_crosssells')
@is_logged_in
def dashboard_crosssells():
    # Create  Cursor
    cur = mysql.connection.cursor()

    # Get Cross Sells 
    result = cur.execute("SELECT * FROM crosssells")

    # Set Cross Sell Variable and set it to all in Dictionary form
    crosssells = cur.fetchall()

    if result > 0:
        return render_template('dashboard_crosssells.html', crosssells=crosssells)
    else:
        msg = 'No Cross Sells Yet'
        return render_template('dashboard_crosssells.html', msg=msg)

    # Close Connection
    cur.close()

# HR Issues Dashboard Route
@app.route('/dashboard_hrissues')
@is_logged_in
def dashboard_hrissues():
    # Create  Cursor
    cur = mysql.connection.cursor()

    # Get Cross Sells 
    result = cur.execute("SELECT * FROM hrissues")

    # Set Cross Sell Variable and set it to all in Dictionary form
    hrissues = cur.fetchall()

    if result > 0:
        return render_template('dashboard_hrissues.html', hrissues=hrissues)
    else:
        msg = 'No HR Issues Yet'
        return render_template('dashboard_hrissues.html', msg=msg)

    # Close Connection
    cur.close()

# Dashboard Route
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')

# Add Cross Sell Form Class
class CrosssellForm(Form):
    pf_number = StringField('pf_number', [validators.Length(min=1, max=6)])
    branch = StringField('branch', [validators.Length(min=1, max=50)])
    customer_account = StringField('customer_account', [validators.Length(min=1, max=20)])
    product = StringField('product', [validators.Length(min=1, max=20)])
    crosssell_type = StringField('crosssell_type', [validators.Length(min=1, max=20)])
    naration = TextAreaField('naration', [validators.Length(min=10)])
    # submission_date = StringField('submission_date', [validators.Length(min=1, max=20)])

    # username = StringField('Username', [validators.Length(min=4, max=25)])
    # username = StringField('Username', [validators.Length(min=4, max=25)])
    # email = StringField('Email', [validators.Length(min=6, max=50)])
    # password = PasswordField('Password', [
    #     validators.DataRequired(),
    #     validators.EqualTo('confirm', message='Passwords do not match')
    # ])
    # confirm = PasswordField('Confirm Password')

# Add Crosssell Route  
@app.route('/add_crosssell', methods=['GET', 'POST'])
@is_logged_in
def add_crosssell():
    form = CrosssellForm(request.form)
    if request.method == 'POST' and form.validate():
        pf_number = form.pf_number.data
        branch = form.branch.data
        customer_account = form.customer_account.data
        product = form.product.data
        crosssell_type = form.crosssell_type.data
        naration = form.naration.data
        # submission_date = form.submission_date.data

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute 
        cur.execute("INSERT INTO crosssells(pf_number, branch, customer_account, product, crosssell_type, naration, name) VALUES(%s, %s, %s, %s, %s, %s, %s)", (pf_number, branch, customer_account, product, crosssell_type, naration, session['username']))

        # Commit to DB
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash('Your cross sell was made successfully', 'success')

        return redirect(url_for('dashboard_crosssells'))

    return render_template('add_crosssell.html', form=form)

# Edit Crosssell Route  
@app.route('/edit_crosssell/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_crosssell(id):

    # Create Cursor
    cur = mysql.connection.cursor()

    # Get Cross sell by id
    result = cur.execute("SELECT * FROM crosssells WHERE id = %s", [id])

    crosssell = cur.fetchone()

    # Get Form
    form = CrosssellForm(request.form)

    # Populate Cross sell form fields
    form.pf_number.data = crosssell['pf_number']
    form.branch.data = crosssell['branch']
    form.customer_account.data = crosssell['customer_account']
    form.product.data = crosssell['product']
    form.crosssell_type.data = crosssell['crosssell_type']
    form.naration.data = crosssell['naration']

    if request.method == 'POST' and form.validate():
        pf_number = request.form['pf_number']
        branch = request.form['branch']
        customer_account = request.form['customer_account']
        product = request.form['product']
        crosssell_type = request.form['crosssell_type']
        naration = request.form['naration']
        # submission_date = '2020-08-31 23:38:49'
        # name = session['username']

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute 
        cur.execute("UPDATE crosssells SET pf_number=%s, branch=%s, customer_account=%s, product=%s, crosssell_type=%s, naration=%s WHERE id=%s", (pf_number, branch, customer_account, product, crosssell_type, naration, id))

        # Commit to DB
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash('Your cross sell was updated successfully', 'success')

        return redirect(url_for('dashboard_crosssells'))

    return render_template('edit_crosssell.html', form=form)


# Add HR Issue Form Class
class HrissueForm(Form):
    pf_number = StringField('pf_number', [validators.Length(min=1, max=6)])
    branch = StringField('branch', [validators.Length(min=1, max=50)])
    topic = StringField('topic', [validators.Length(min=1, max=20)])
    issue_type = StringField('issue_type', [validators.Length(min=1, max=20)])
    hrissue = TextAreaField('hrissue', [validators.Length(min=10)])

# Add HR Issue Route  
@app.route('/add_hrissue', methods=['GET', 'POST'])
@is_logged_in
def add_hrissue():
    form = HrissueForm(request.form)
    if request.method == 'POST' and form.validate():
        pf_number = form.pf_number.data
        branch = form.branch.data
        topic = form.topic.data
        issue_type = form.issue_type.data
        hrissue = form.hrissue.data
        # submission_date = form.submission_date.data

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute 
        cur.execute("INSERT INTO hrissues(pf_number, branch, topic, issue_type, hrissue, name)VALUES(%s, %s, %s, %s, %s, %s)", (pf_number, branch, topic, issue_type, hrissue, session['username']))

        # Commit to DB
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash('Your HR issue was made successfully', 'success')

        return redirect(url_for('dashboard_hrissues'))

    return render_template('add_hrissue.html', form=form)

# Edit HRissue Route  
@app.route('/edit_hrissue/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_hrissue(id):

    # Create Cursor
    cur = mysql.connection.cursor()

    # Get Cross sell by id
    result = cur.execute("SELECT * FROM hrissues WHERE id = %s", [id])

    hrissue = cur.fetchone()

    # Get Form
    form = HrissueForm(request.form)

    # Populate HR Issue form fields
    form.pf_number.data = hrissue['pf_number']
    form.branch.data = hrissue['branch']
    form.topic.data = hrissue['topic']
    form.issue_type.data = hrissue['issue_type']
    form.hrissue.data = hrissue['hrissue']

    if request.method == 'POST' and form.validate():
        pf_number = request.form['pf_number']
        branch = request.form['branch']
        topic = request.form['topic']
        issue_type = request.form['issue_type']
        hrissue = request.form['hrissue']
        # submission_date = '2020-08-31 23:38:49'
        # name = session['username']

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute 
        cur.execute("UPDATE hrissues SET pf_number=%s, branch=%s, topic=%s, issue_type=%s, hrissue=%s WHERE id=%s", (pf_number, branch, topic, issue_type, hrissue, id))

        # Commit to DB
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash('Your HR issue was updated successfully', 'success')

        return redirect(url_for('dashboard_hrissues'))

    return render_template('edit_hrissue.html', form=form)


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
    
    app.run(debug=True)