from flask import Flask, request
from db import stores,items
import uuid
from flask_smorest import abort ## can use status code
app = Flask(__name__)



@app.get("/store") #http://127.0.0.1:5000/store
def get_stores():
    return {"stores":list(stores.values())}

@app.post("/store")
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(404, message="must contain store name")

    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(404, message = "Error. Store already exists in DB.")
    store_id=uuid.uuid4().hex
    store = {**store_data, "id": store_id} #unpacks the dict with any info we have with **, then we add on an id after
    stores[store_id] = store                # ** makes it more scalable as we add more key/values to stores
    return store,201

# add new item to existing store
@app.post("/item")
def create_item():
    item_data = request.get_json()

    if ("price" not in item_data 
    or "name" not in item_data 
    or "store_id" not in item_data):
        abort(404, message="Bas request. Make sure 'price', 'name', and 'store_id' are in JSON payload")

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

@app.get('/item')
def get_all_items():
    return {"items":list(items.values())}

    
# get specific store info
@app.get("/store/<string:store_id>")
def get_store_info(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404,message="Store ID not found")

# get specific store items
@app.get("/items/<string:item_id>")
def get_store_items(item_id):
    try:
        return items['item_id']
    except KeyError:
        abort(404,message="Item not found")