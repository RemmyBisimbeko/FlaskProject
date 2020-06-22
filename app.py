from flask import Flask, render_template
from data import Restructures

# Init App
app = Flask(__name__)

# Create Variable equal to Function imported 
Restructures = Restructures()

# Create Variable equal to Function imported 
Applications = Applications()

# Home Route
@app.route('/')
def home():
    return render_template('home.html')

# About Route
@app.route('/about')
def about():
    return render_template('about.html')

# Restrucres Route
@app.route('/restructures')
def restructures():
    return render_template('restructures.html', restructures = Restructures)

# Single Restrucre Route
@app.route('/restructure/<string:id>')
def restructure(id):
    return render_template('restructure.html', id=id)

# Applications Route
@app.route('/applications')
def restructures():
    return render_template('applications.html', applications = Applications)

# Single Restrucre Route
@app.route('/application/<string:id>')
def restructure(id):
    return render_template('application.html', id=id)



# Run Server
if __name__ == '__main__':
    app.run(debug=True)