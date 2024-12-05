from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise Exception("Missing Supabase credentials")

supabase: Client = create_client(supabase_url, supabase_key)

# Define data model
class Item(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    completed: bool = False

# CRUD Operations
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    try:
        response = supabase.table("items").insert({
            "title": item.title,
            "description": item.description,
            "completed": item.completed
        }).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/items/", response_model=List[Item])
async def read_items():
    try:
        response = supabase.table("items").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    try:
        response = supabase.table("items").select("*").eq("id", item_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Item not found")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    try:
        response = supabase.table("items").update({
            "title": item.title,
            "description": item.description,
            "completed": item.completed
        }).eq("id", item_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Item not found")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    try:
        response = supabase.table("items").delete().eq("id", item_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"message": "Item deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
