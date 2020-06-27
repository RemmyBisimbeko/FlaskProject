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

@app.route('/register')
def register():
    form = RegisterForm(request.form)
    # Check if GET or POST request, and make sure everything is validated
    # if request.method == 'POST' and form.validate():
        # return render_template('register.html')
    return render_template('register.html', form=form)

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