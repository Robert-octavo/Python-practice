from flask import Flask
from flask_restful import Api
# from flask_jwt import JWT

# from security import authenticate, identity
from users import UserList, User

app = Flask(__name__)
# app.secret_key = 'robert'
api = Api(app)

# jwt = JWT(app, authenticate, identity) 

# items = []

api.add_resource(UserList, '/users')
api.add_resource(User, '/user/<string:_id>')

if __name__ == '__main__':
    app.run(port=5000, debug=True)