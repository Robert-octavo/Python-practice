from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity) #creates a new endpoint cal /auth

items = []
""" This class is a resource"""
class Item(Resource):
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

        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201 #This code is for CREATED

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>') 
api.add_resource(ItemList, '/items')


app.run(port=5000, debug=True)