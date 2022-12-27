from flask import Flask, request

app = Flask(__name__)


stores = [
    {
        "name":"store",
        "items": [
            {
                "name":"Chair",
                "price":15.99
            }
        ]
    }

]

@app.get("/store") #http://127.0.0.1:5000/store
def get_stores():
    return {"stores":stores}

@app.post("/store")
def create_store():
    request_data = request.get_json()
    new_store = {"name":request_data['name'], "items":[]}
    stores.append(new_store)
    return stores,201

# add new item to existing store
@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    new_item = {'name':request_data['name'],'price':request_data['price']}

    for store in stores:
        if store['name'] == name:
            # add new item
            store['items'].append(new_item)
            return store['items']
    return {'message':'error store not found'},404
@app.get("/store/<string:name>")
def get_store_info(name):
    for store in stores:
        if store['name'] == name:
            return store