from multiprocessing import connection
import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        """TODO: Find a user in the database"""
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM  users WHERE username=?"
        result = cursor.execute(query, (username,)) #TODO: it has to be in a tuple (username,)
        row = result.fetchone() #get the first row from result
        if row: # if row is not none
            # user = cls(row[0], row[1], row[2])
            user = cls(*row) #same from the above
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        """TODO: Find a user in the database by id"""
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM  users WHERE id=?"
        result = cursor.execute(query, (_id,)) #TODO: it has to be in a tuple (username,)
        row = result.fetchone() #get the first row from result
        if row: # if row is not none
            # user = cls(row[0], row[1], row[2])
            user = cls(*row) #same from the above
        else:
            user = None
        connection.close()
        return user

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        
        if User.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User created successfully"}, 201