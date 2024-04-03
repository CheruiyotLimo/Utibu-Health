from pydantic import BaseModel, EmailStr
from typing import Optional

# Define your pydantic models here.


class UserSignUp(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = None
    
class UserLogin(BaseModel):
    username: EmailStr
    password: str

class UserReturn(BaseModel):
    id: str
    name: str
    
    class Config:
        orm_mode = True
        
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    email: Optional[EmailStr] = None

class DrugCreate(BaseModel):
    drug_name: str
    price: int
    quantity: int

class DrugUpdate(BaseModel):
    quantity: int
    
class DrugReturn(BaseModel):
    id: int
    drug_name: str
    price: int
    stock: Optional[str] = None
    
    class Config:
        orm_mode = True

class OrderCreate(BaseModel):
    order_id: int
    user_name: str
    user_email: str
    drug_name: str
    drug_quantity: int
    total_price: int
    
class OrderReturn(BaseModel):
    order_id: int
    user_name: str
    drug_name: str
    drug_quantity: int
    total_price: int
    
    class Config:
        orm_mode = True