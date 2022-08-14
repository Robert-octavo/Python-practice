import sqlite3
from unittest import result
from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required

""" This class is a resource"""
class Item(Resource):
    parser = reqparse.RequestParser()
        # price argument cannot be blank
        # if there's more arguments we need to created
        # you put the parser here to be able to access later
    parser.add_argument('price',
        type=float,
        required=True,
        help = "This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        """TODO: find a item by its name (Unique) """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row  = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}


    def post(self, name):
        # For unique name item
        if self.find_by_name(name) is not None:
            return ({'message': "An item with name '{}' already exists.".format(name)}, 400)

        # data = request.get_json()
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        try:
            self.insert(item)
        except:
            return {"message": "An error occurred inserting the item"}, 500 #Internal server error

        return item, 201 #This code is for CREATED

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    def put(self, name):
        
        data = Item.parser.parse_args()
        #data = request.get_json()
        item = Item.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                Item.insert(updated_item)
            except:
                return {"message": "An error ocurred inserting the item"}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error ocurred Updating the item"}, 500
        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()
        return {'items': items}