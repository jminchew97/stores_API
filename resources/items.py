import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores, items

from schemas import ItemSchema, ItemUpdateSchema

bp = Blueprint("items",__name__, description="Operation on items")


@bp.route("/item")
class Item(MethodView):

    @bp.arguments(ItemSchema)
    @bp.response(201, ItemSchema)
    def post(self, item_data):
        """create new item within store."""

        # checks if item exists in DB
        for item in items.values():
            if (item_data["name"] == item["name"] and 
            item_data["store_id"]== item["store_id"]):
                abort(404,message="item already exists")

        # check if store entered is valid
        if item_data['store_id'] not in stores:
            abort(404,message="Store not found")
        
        # Store ID check passed 
        # create item UUID
        item_id =uuid.uuid4().hex
        item = {**item_data,"item_id":item_id,"store_name":stores[item_data["store_id"]]}
        items[item_id] = item

        return items, 201

    @bp.response(200, ItemSchema(many=True)) # applies schema to multiple item objects
    def get(self):
        """Get all items"""
        return items.values()

@bp.route("/item/<string:item_id>")
class SpecificItem(MethodView):

    @bp.response(200, ItemSchema)
    def get(self, item_id):
        """Get specific item using UUID"""
        try:
            return items[item_id]
        except KeyError:
            abort(404,message="Item not found")

    @bp.arguments(ItemUpdateSchema) # Schema used to validate data sent to endpoint
    @bp.response(200, ItemUpdateSchema) # Schema used to validate data sent from endpint
    def put(self, item_data, item_id):
        """Update an item"""
        try:
            items[item_id].update(item_data)
        except KeyError:
            abort(404,message="Item not found.")
        return items[item_id]
    def delete(self, item_id):
        """Delete specific item using UUID"""
        try:
            del items[item_id]
            return {"message":"item deleted"}
        except KeyError:
            abort(404,message="Item not found")

