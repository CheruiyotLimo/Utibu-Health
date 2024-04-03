from .db import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.sql.expression import text, null


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable= False, unique=True)
    password = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text("now()"))
    role = Column(String)
    

class Drug(Base):
    __tablename__= "drugs"
    id = Column(Integer, nullable=False, primary_key=True)
    drug_name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer)
    
class Sales(Base):
    __tablename__ = "sales"
    order_id = Column(Integer, nullable=False, primary_key=True)
    user_name = Column(String, nullable=False)
    user_email = Column(String, ForeignKey("users.email", ondelete="CASCADE"), nullable=False)
    drug_name = Column(String, ForeignKey("drugs.drug_name", ondelete="CASCADE"), nullable=False)
    drug_quantity = Column(Integer, default=1)
    total_price = Column(Integer)
    payment = Column(Boolean, default=False)
    transaction_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))