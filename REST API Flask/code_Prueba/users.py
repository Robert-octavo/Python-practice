from cgitb import text
import sqlite3
from unittest import result
from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required

class User(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('name',
        type=str,
        required=True,
        help = "No puede ser en blanco"
    )
    parser.add_argument('apellido',
        type=str,
        required=True,
        help = "No puede ser en blanco"
    )

    parser.add_argument('cedula',
        type=str,
        required=True,
        help = "No puede ser en blanco"
    )

    parser.add_argument('fecha_nacimiento',
        type=str,
        required=True,
        help = "No puede ser en blanco"
    )
    def get(self, _id):
        item = self.find_by_id(_id)
        if item:
            return item
        return {'message': 'User not found'}, 404

    @classmethod
    def find_by_id(cls, _id):
        """TODO: find a user by its cedula (Unique) """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE _id=?"
        result = cursor.execute(query, (_id,))
        row  = result.fetchone()
        connection.close()

        if row:
            return {'user': {'_id': row[0],'name': row[1], 'apellido': row[2], 'cedula': row[3], 'fecha_nacimiento': row[4]}}

    def post(self, _id):
        # For unique name item
        if self.find_by_id(_id) is not None:
            return ({'message': "An user with name '{}' already exists.".format(_id)}, 400)

        # data = request.get_json()
        data = User.parser.parse_args()
        user = {'_id': _id, 'name': data['name'], 'apellido': data['apellido'], 'cedula': data['cedula'], 'fecha_nacimiento': data['fecha_nacimiento']}
        try:
            self.insert(user)
        except:
            return {"message": "An error occurred inserting the user"}, 500 #Internal server error

        return user, 201 #This code is for CREATED

    @classmethod
    def insert(cls, user):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, (user['_id'], user['name'], user['apellido'], user['cedula'], user['fecha_nacimiento']))

        connection.commit()
        connection.close()

    def delete(self, _id):

        if self.find_by_id(_id) is None:
            return ({'message': "An user with the '{}' doesn't exists.".format(_id)}, 400)
    
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM users WHERE _id=?"
        cursor.execute(query, (_id,))

        connection.commit()
        connection.close()

        return {'message': 'User deleted'}

    def put(self, _id):
        
        data = User.parser.parse_args()
        #data = request.get_json()
        user = User.find_by_id(_id)
        updated_user = {'_id': _id, 'name': data['name'], 'apellido': data['apellido'], 'cedula': data['cedula'], 'fecha_nacimiento': data['fecha_nacimiento']}

        if user is None:
            try:
                User.insert(updated_user)
            except:
                return {"message": "An error ocurred inserting the user"}, 500
        else:
            try:
                self.update(updated_user)
            except:
                return {"message": "An error ocurred Updating the user"}, 500
        return updated_user

    @classmethod
    def update(cls, user):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE users SET name=?, apellido=?, cedula=?, fecha_nacimiento=? WHERE _id=?"
        cursor.execute(query, (user['name'], user['apellido'], user['cedula'], user['fecha_nacimiento'],user['_id']))

        connection.commit()
        connection.close()

class UserList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users"
        result = cursor.execute(query)
        # row  = result.fetchone()
        users = []
        for row in result:
            users.append({'id': row[0],'name': row[1], 'apellido': row[2], 'cedula': row[3], 'fecha_nacimiento': row[4]})

        connection.close()
        return {'Users': users}