from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_claims, 
    jwt_optional, 
    get_jwt_identity,
    fresh_jwt_required)
from models.item import itemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type = float,
            required = True,
            help = "This field can't be left blank"
        )
    parser.add_argument('store_id',
            type = int,
            required = True,
            help = "Every item needs a store id"
        )
 
    @jwt_required
    def get(self, name):
        item = itemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found'}, 404

    
    @fresh_jwt_required
    def post(self, name):
        if itemModel.find_by_name(name):
            return {"message": f"an item with name {name} already exists."}, 400

        data = Item.parser.parse_args()
        item = itemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message':'An error occured inserting the item'},500

        return item.json(), 201
    
    @jwt_required
    def delete(self,name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        item = itemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message":"Item deleted"}

    def put(self,name):
        data = Item.parser.parse_args()

        item = itemModel.find_by_name(name)

        if item is None:
            item = itemModel(name, **data)
        else:
            item.price = data['price']
        
        item.save_to_db()

        return item.json()
    

class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in itemModel.find_all()]
        if user_id:
            return {'items':items}, 200
        return {
            'items':[item['name'] for item in items],
            'message': 'Access More data by logging in.'
            },200
        # list(map(lambda x: x.json(),itemModel.query.all()))