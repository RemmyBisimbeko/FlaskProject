from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os 

# Init App
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite ')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db (SqlAlchemy)
db = SQLAlchemy(app)
# Init Marshmallow
ma = Marshmallow(app)

# Loan Class/Model
class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    account = db.Column(db.String(20), unique=True)
    branch = db.Column(db.String(20))
    telephone = db.Column(db.String(20), unique=True)
    officer = db.Column(db.String(30))
    email = db.Column(db.String(30), unique=True)
    reason = db.Column(db.String(500))
    
    def __init__(self, name, account, branch, telephone, officer, email, reason):
        self.name = name
        self.account = account
        self.branch = branch
        self.telephone = telephone
        self.officer = officer
        self.email = email
        self.reason = reason

# Loan Schema
class LoanSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'account', 'branch', 'telephone', 'officer', 'email', 'reason')

# Init Schema
loan_schema = LoanSchema()
loans_schema = LoanSchema(many=True)

# Create a Loan
@app.route('/loan', methods=['POST'])
def add_loan():
    name = request.json['name']
    account = request.json['account']
    branch = request.json['branch']
    telephone = request.json['telephone']
    officer = request.json['officer']
    email = request.json['email']
    reason = request.json['reason']

    new_loan = Loan(name, account, branch, telephone, officer, email, reason)

    db.session.add(new_loan)
    db.session.commit()

    return loan.jsonify(new_loan)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)