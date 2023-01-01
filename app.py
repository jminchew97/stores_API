from flask import Flask, request
from db import stores,items
import uuid
app = Flask(__name__)



@app.get("/store") #http://127.0.0.1:5000/store
def get_stores():
    return {"stores":list(stores.values())}

@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id=uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store,201

# add new item to existing store
@app.post("/item")
def create_item():
    item_data = request.get_json()
    if item_data['store_id'] not in stores:
        return {"message":"Invalid store_id"},404
    
    # store ID is valid
    # create item UUID
    item_id =uuid.uuid4().hex
    item = {**item_data,"item_id":item_id}
    items[item_id] = item

    return item, 201

@app.get('/item')
def get_all_items():
    return {"items":list(items.values())}

    
# get specific store info
@app.get("/store/<string:store_id>")
def get_store_info(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {"message":"Store ID not found"}, 404

# get specific store items
@app.get("/items/<string:item_id>")
def get_store_items(item_id):
    try:
        return items['item_id']
    except KeyError:
        return {"message":"item not found"}, 404