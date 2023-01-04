import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores, items

bp = Blueprint("items",__name__, description="Operation on items")


@bp.route("/item")
class Item(MethodView):
    def post(self):
        """create new item within store."""
        item_data = request.get_json()

        if ("price" not in item_data 
        or "name" not in item_data 
        or "store_id" not in item_data):
            #abort(404, message="Bas request. Make sure 'price', 'name', and 'store_id' are in JSON payload")
            return {"message":"JSON does not have store id/name/price of item."}
        # check if item already exists
        for item in items.values():
            if (item_data["name"] == item["name"] and 
            item_data["store_id"]== item["store_id"]):
                abort(404,message="item already exists")

        if item_data['store_id'] not in stores:
            abort(404,message="Store not found")
        
        # store ID is valid
        # create item UUID
        item_id =uuid.uuid4().hex
        item = {**item_data,"item_id":item_id,"store_name":stores[item_data["store_id"]]}
        items[item_id] = item

        return items, 201

    def get(self):
        """Get all items"""
        return {"items":list(items.values())}

@bp.route("/item/<string:item_id>")
class SpecificItem(MethodView):
    def get(self, item_id):
        """Get specific item using UUID"""
        try:
            return items[item_id]
        except KeyError:
            abort(404,message="Item not found")
    def put(self, item_id):
        """edit a specific items information by item_id"""
        json_data = request.get_json()
        if "name" not in json_data or "price" not in json_data:
            return {"message":"must include 'name' and 'price' in json data."}
        try:
            items[item_id].update(json_data)
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

