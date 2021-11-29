from sys import path
from pathlib import Path
path.append(str(Path(__file__).resolve().parent.parent))
from flask import Flask
from flask_restful import Api
from endpoints.ingAtmService import ListAllAtm, AddUpdateAtm, RemoveAtm, LoadAtmData
from flask_jwt import JWT
#from module.user import user, authenticate, identity
from werkzeug.security import safe_str_cmp

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

users = [
    User(1, 'user1', 'password1')
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

app = Flask(__name__)
api = Api(app)
app.secret_key = "password1"
jwt = JWT(app, authenticate, identity)

api.add_resource(RemoveAtm, '/deleteAtm/<int:atmId>')
api.add_resource(ListAllAtm, '/listAllAtm')
api.add_resource(AddUpdateAtm, '/addUpdateAtm')
api.add_resource(LoadAtmData, '/loadAtmData')

if __name__ == "__main__":
    app.run(port=5000, debug=True, host='0.0.0.0')

