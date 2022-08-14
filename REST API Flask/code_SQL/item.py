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
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row  = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
        return {'message': 'Item not found'}, 404

    def post(self, name):
        # For unique name item
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return ({'message': "An item with name '{}' already exists.".format(name)}, 400)

        # data = request.get_json()
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201 #This code is for CREATED

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items)) #create a new list with all the element except the one that match
        return {'message': 'Item deleted'}

    def put(self, name):
        
        data = Item.parser.parse_args()
        #data = request.get_json()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            # the item does not exist -- new
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            # update the item
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}