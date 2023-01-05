import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema

bp = Blueprint("stores",__name__, description="Operation on stores")

"""each methodview is """
@bp.route("/store/<string:store_id>")
class Store(MethodView):
    @bp.response(201, StoreSchema)
    def get(self, store_id):
        """Get store information using UUID"""
        try:
            return stores[store_id]
        except KeyError:
            abort(404,message="Store ID not found")

    @bp.arguments(StoreSchema)
    @bp.response(201, StoreSchema)
    def put(self, json_data, store_id):
        """Edit store name using UUID"""
        
        if store_id not in stores:
            return {"message":"this store does not exist enter a valid UUID"}
        
        """Make sure needed information is in JSON payload"""
        if "name" not in json_data:
            return {"message":"Make sure to have 'name' in payload to edit"} 
        if json_data['name'] == stores[store_id]['name']:
            return {"message":"you entered the current name of a store, to edit enter a different name."}

        # passes all test, change the store information
        stores[store_id]['name'] = json_data['name']
        return stores[store_id]

    def delete(self, store_id):
        """Delete a store using store UUID"""
        try:
            del stores[store_id]
            return {"message":"item deleted"}
        except KeyError:
            abort(404,message="Item not found")

@bp.route("/store")
class StoreList(MethodView):

    @bp.response(200, StoreSchema(many=True))
    def get(self):
        """Get all stores"""
        return stores.values()

    @bp.arguments(StoreSchema) # using schema for data validation
    @bp.response(200, StoreSchema)
    def post(self, store_data):
        """Create store"""
        
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(404, message = "Error. Store already exists in DB.")
        store_id=uuid.uuid4().hex
        store = {**store_data, "id": store_id} #unpacks the dict with any info we have with **, then we add on an id after
        stores[store_id] = store                # ** makes it more scalable as we add more key/values to stores
        return store,201
