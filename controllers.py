from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import Boolean, cast # type: ignore
from schema import ItemCreate
from model import Item
from fastapi import HTTPException # type: ignore

def create_item(item: ItemCreate, db: Session):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def read_item(item_id: int, db: Session):
    db_item = db.query(Item).filter(cast(Item.id == item_id, Boolean)).first()
    return db_item

def read_items(db: Session):
    db_item = db.query(Item).all()
    return db_item

def update_item(item_id: int, item: ItemCreate, db: Session):
    db_item = db.query(Item).filter(cast(Item.id == item_id, Boolean)).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(item_id: int, db:Session):
    db_item = db.query(Item).filter(cast(Item.id == item_id, Boolean)).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return { 'message': 'Item deleted successfully' }