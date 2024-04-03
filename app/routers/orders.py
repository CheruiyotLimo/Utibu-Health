from fastapi import FastAPI, Depends, HTTPException, status, APIRouter, Form
from ..db import engine, get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from . import drugs
from typing import Optional
import random

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

# @router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.OrderReturn)
def create_order(order_details: schemas.OrderCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """ POST request for creating an order"""
    if current_user:
        order_data = models.Sales(**order_details)
        
        # Add new hospital to the database
        db.add(order_data)
        db.commit()
        db.refresh(order_data)
        return order_data
        
    
@router.post("/create", status_code=status.HTTP_201_CREATED)
def add_order(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), drug_name: str = Form(),
                drug_qty: int = Form()):
    """ POST request for creating an order"""

    # Check the curent user
    user = current_user
    
    
    # Check if the drug exists
    drug = db.query(models.Drug).filter(models.Drug.drug_name == drug_name).first()
    
    # Check if drug is in stock
    if drug.quantity <= 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Drug is out of stock.")
    elif drug.quantity < drug_qty:
        raise HTTPException(status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE, detail=f"Unable to complete order. Only {drug.quantity} left in stock.")
    else:
        new_quantity = drug.quantity - drug_qty
       
    
    order_details = {
        "order_id": random.randint(1, 1000000),
        "user_name": user.name,
        "user_email": user.email,
        "drug_name": drug.drug_name,
        "drug_quantity": drug_qty,
        "total_price": drug.price * drug_qty
    }
    
    # Update the drug db to update the new drug quantity.
    qty_data = {"quantity": new_quantity}
    drugs.update_quantity(qty_data, drug_id=drug.id, current_user=current_user, db=db)
    
    order_data = create_order(order_details=order_details, db=db, current_user=current_user)
    return "Order successfully created."