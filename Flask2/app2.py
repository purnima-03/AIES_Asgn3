from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
from flask_restful import Resource, Api

app = Flask(__name__) 
api = Api(app) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app) 
ma = Marshmallow(app)

class User(db.Model):
    studentid = db.Column(db.Integer, unique=True, primary_key=True)
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32))
    dob = db.Column(db.Integer)
    amountdue = db.Column(db.Integer)

    def __init__(self, studentid, firstname, lastname, dob, amountdue):
        self.studentid = studentid
        self.firstname = firstname
        self.lastname = lastname
        self.dob = dob
        self.amountdue = amountdue

class UserSchema(ma.Schema):
    class Meta:
        fields = ('studentid', 'firstname', 'lastname', 'dob', 'amountdue')

user_schema = UserSchema() 
users_schema = UserSchema(many=True)

class UserManager(Resource):
    @staticmethod
    def get():
        try: id = request.args['studentid']
        except Exception as _: id = None

        if not id:
            users = User.query.all()
            return jsonify(users_schema.dump(users))
        user = User.query.get(id)
        return jsonify(user_schema.dump(user))

    @staticmethod
    def post():
        studentid = request.json['studentid']
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        dob = request.json['dob']
        amountdue = request.json['amountdue']

        user = User(studentid, firstname, lastname, dob, amountdue)
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'Message': f'User {firstname} {lastname} inserted.'
        })

    @staticmethod
    def put():
        try: id = request.args['studentid']
        except Exception as _: id = None
        if not id:
            return jsonify({ 'Message': 'Must provide the Student ID' })
        
        user = User.query.get(id)
        studentid = request.json['studentid']
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        dob = request.json['dob']
        amountdue = request.json['amountdue']

        user.studentid = studentid
        user.firstname = firstname 
        user.lastname = lastname 
        user.dob = dob 
        user.age = amountdue 

        db.session.commit()
        return jsonify({
            'Message': f'User {firstname} {lastname} altered.'
        })

    @staticmethod
    def delete():
        try: id = request.args['studentid']
        except Exception as _: id = None
        if not id:
            return jsonify({ 'Message': 'Must provide the Student ID' })
        user = User.query.get(id)

        db.session.delete(user)
        db.session.commit()

        return jsonify({
            'Message': f'User {str(id)} deleted.'
        })


api.add_resource(UserManager, '/api/users')

if __name__ == '__main__':
    app.run(debug=True)
