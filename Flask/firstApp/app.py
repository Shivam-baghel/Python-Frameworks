from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name":"My store",
        "items":[
            {
                "name": "chair",
                "price": 15.99
            }
        ]
    }
]

@app.get("/store")
def get_stores():
    return {"stores": stores}

@app.get("/store/<string:storeName>")
def get_store(storeName):
    
    for store in stores:
        if store["name"] == storeName:
            return store
    
    return {"message": "store not found"}, 404

@app.get("/store/<string:storeName>/item")
def get_item_in_store(storeName):
    
    for store in stores:
        if store["name"] == storeName:
            return {"items": store["items"], "message": "Successfully retrieved the items"}
        
    return {"message": "store not found"}, 404


@app.post("/createStore")
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"],"items":[]}
    stores.append(new_store)
    
    return {"message": "successfully created the store."}, 201

@app.post("/addItem/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            
            return new_item, 201
        
    return {"message": "store not found"}, 404
