from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemOut


router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=list[ItemOut])
def list_items(db: Session = Depends(get_db)):
    return db.query(Item).all()


@router.post("/", response_model=ItemOut)
def create_item(item_in: ItemCreate, db: Session = Depends(get_db)):
    item = Item(title=item_in.title, owner_id=item_in.owner_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


