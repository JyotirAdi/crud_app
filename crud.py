import json
from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("secret_key")
app.config['MONGO_URI'] = os.getenv("mongo_url")

mongo = PyMongo(app)

@app.route('/register', methods=['POST'])
def add_user():
    _json = request.json
    _name=_json['name']
    _email=_json['email']
    _pass=_json['pwd']

    if _name and _email and _pass and request.method =='POST':
        _hash_pass=generate_password_hash(_pass)

        id = mongo.db.user.insert_one({'name':_name,'email':_email,'pwd': _hash_pass})

        response_msg=jsonify("User added successfully")

        response_msg.status_code = 200
        return response_msg

    else:
        return not_found()
@app.route('/users')
def users():
    users = mongo.db.user.find()
    resp = dumps(users)
    return resp

@app.route('/users/<id>')
def user(id):
    try:
        user = mongo.db.user.find_one({'_id': ObjectId(id)})
        resp = dumps(user)
        return resp
    except:
        return {'status': 'false', "message": "User not found"}, 404

@app.route('/delete/<id>', methods = ['DELETE'])
def delete_user(id):
    try:
        mongo.db.user.delete_one({'_id':ObjectId(id)})
        resp = jsonify("user deleted successfully")  
        return resp, 200
    except:
        return {'status': 'false', "message": "User not found"}, 404

@app.route('/update/<id>', methods = ['PUT'])
def update_user(id):
    _id = id
    _json = request.json
    _name= _json['name']
    _email=_json['email']
    _password = _json['pwd']

    if _name and _email and _password and _id and request.method =='PUT':
        _hasshed_passpord=generate_password_hash(_password)
        mongo.db.user.update_one({ '_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set': {'name': _name,'email':_email , 'pwd':_hasshed_passpord}})
        resp = jsonify("User Updated Successfully ")
        return resp, 200
    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found ' + request.url
    }
    response=jsonify(message)
    response.status_code=404
    return response

if __name__=="__main__":
    app.run(debug=True) 

