from fastapi import FastAPI, Depends # type: ignore
from typing import List
from sqlalchemy.orm import Session # type: ignore
from database import engine, Base, get_db
from schema import ItemCreate, ItemResponse
from controllers import create_item, read_item, read_items, update_item, delete_item
from fastapi.middleware.cors import CORSMiddleware # type: ignore

Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/test', response_model=ItemResponse)
def create_item_route(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item(item, db)

@app.get('/test/{item_id}', response_model=ItemResponse)
def read_item_route(item_id: int, db: Session = Depends(get_db)):
    return read_item(item_id, db)

@app.get('/test', response_model=List[ItemResponse])
def read_items_route(db: Session = Depends(get_db)):
    return read_items(db)

@app.put('/test/{item_id}', response_model=ItemResponse)
def update_item_route(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    return update_item(item_id, item, db)

@app.delete('/test/{item_id}')
def delete_item_route(item_id: int, db:Session = Depends(get_db)):
    return delete_item(item_id, db)
