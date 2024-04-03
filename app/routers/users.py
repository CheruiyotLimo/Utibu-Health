from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from ..db import engine, get_db
from ..config import settings
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2, config
from typing import Literal
from scripts.verifier import email_verifier
import json, io



router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserReturn)
def register_user(data: schemas.UserSignUp, db: Session = Depends(get_db)):
    """Sign up a user to the system."""

    # Check if provided email and/or registration number exists in database
    user_email = db.query(models.User).filter(models.User.email == data.email)

    # Raise HTTP error if any exists.
    if user_email.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A user already exists with similar email!!")
    
    # If an admin, hash the email to abstract the admin secret in the database.
    if data.role == settings.admin_reg:
        data.role = "admin"

    # Hash password before storing in the database.
    new_password = utils.hash(data.password)
    data.password = new_password

    # Convert provided dictionary into a model dictionary.
    data = models.User(**data.dict())

    # Add user to the database.
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

@router.get("/get_orders/", status_code=status.HTTP_200_OK, response_model=list[schemas.OrderReturn])
def retrieve_orders(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    """Retrieve user's order hitory"""
    
    # Query order db for orders filtered for currently logged in email.
    orders = db.query(models.Sales).filter(models.Sales.user_email == current_user.email).all()

    # Verify orders exist
    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You have no previous orders.")
    print(type(orders[0]))
    return [ schemas.OrderReturn.from_orm(order) for order in orders]
    
    