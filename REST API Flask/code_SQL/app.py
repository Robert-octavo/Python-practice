from email import message
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity) #creates a new endpoint cal /auth

items = []
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
        """for item in items:
            if item['name'] == name:
                return item"""
        # return the first that return the filter function
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item is not None else 404 #this is because you need to return a dictionary
        #200 if item else 404

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

api.add_resource(Item, '/item/<string:name>') 
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


app.run(port=5000, debug=True)