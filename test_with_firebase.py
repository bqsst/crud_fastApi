from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from firebase_admin import credentials, firestore, initialize_app
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Initialize Firebase
cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS"))
initialize_app(cred)
db = firestore.client()

# Define data model
class Item(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    completed: bool = False

# CRUD Operations
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    try:
        doc_ref = db.collection('items').document()
        item_data = {
            "title": item.title,
            "description": item.description,
            "completed": item.completed
        }
        doc_ref.set(item_data)
        item_data['id'] = doc_ref.id
        return item_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/items/", response_model=List[Item])
async def read_items():
    try:
        items = []
        docs = db.collection('items').stream()
        for doc in docs:
            item_data = doc.to_dict()
            item_data['id'] = doc.id
            items.append(item_data)
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    try:
        doc = db.collection('items').document(item_id).get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Item not found")
        item_data = doc.to_dict()
        item_data['id'] = doc.id
        return item_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    try:
        doc_ref = db.collection('items').document(item_id)
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="Item not found")
        
        item_data = {
            "title": item.title,
            "description": item.description,
            "completed": item.completed
        }
        doc_ref.update(item_data)
        item_data['id'] = item_id
        return item_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    try:
        doc_ref = db.collection('items').document(item_id)
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="Item not found")
        doc_ref.delete()
        return {"message": "Item deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
