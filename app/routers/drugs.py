from fastapi import FastAPI, Depends, HTTPException, status, APIRouter, Form
from ..db import engine, get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from typing import Optional

router = APIRouter(
    prefix="/drugs",
    tags=["Drugs"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.DrugReturn)
def add_drug(drug_data: schemas.DrugCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """ POST request for updating the drug database"""

    # Check if user is authorized 
    oauth2.verify_admin(current_user)
    
    # Check if the hospital exists
    drug = db.query(models.Drug).filter(models.Drug.drug_name == drug_data.drug_name).first()
    if drug:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Drug already exists.")
    
    # Convert the dictionary to a model dictionary
    drug_data = models.Drug(**drug_data.dict())

    # Add new hospital to the database
    db.add(drug_data)
    db.commit()
    db.refresh(drug_data)
    return drug_data

# GET request for a user to search for a drug
@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.DrugReturn])
def get_drug(current_user: int = Depends(oauth2.get_current_user), db: Session = (Depends(get_db)), limit: int = 10, skip: int = 0, search_term: Optional[str] = Form(default="")):
    """
    GET request for a user to search for a drug with defined query parameters allowing for modification of returned results.
    """

    drugs = db.query(models.Drug).filter(models.Drug.drug_name.like(f"%{search_term}%")).limit(limit).offset(skip).all()

    if not drugs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are currently no drugs with that name.")

    return [
        {   
            'id': drug.id,
            'drug_name': drug.drug_name,
            'price': drug.price,
            'stock': "In Stock" if drug.quantity > 0 else "Out of Stock"
        }
        for drug in drugs
    ]


@router.post('/build/', status_code=status.HTTP_201_CREATED)
def build_drugs(current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    # verify the user is an admin
    oauth2.verify_admin(current_user)

    hosp_list = {
        "DTG": ["Dolutegravir", 800, 20],
        "ABC": ["Abacavir", 540, 28],
        "LAM": ["Lamivudine", 1220, 5],
        "TDF": ["Tenofovir", 250, 50],
        "RTV": ["Ritonavir", 2000, 12],
        "EFV": ["Efavirenz", 100, 47],
        
    }

    for _, v in hosp_list.items():
        drug = {
            'drug_name': v[0],
            'price': v[1],
            'quantity': v[2],
        }

        drug = models.Drug(**drug)

        add_drug(drug_data=drug, db=db, current_user=current_user)
    return 'Successfully added all drugs!'

@router.patch("/{id}", status_code=status.HTTP_201_CREATED)
def update_quantity(drug_detail: schemas.DrugUpdate, drug_id: int, current_user: str = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    
    # Verify user is an admin
    # oauth2.verify_admin(current_user)
    
    # Query the db fo the drug
    drug = db.query(models.Drug).filter(models.Drug.id == drug_id)
    
    # Check drug exists
    if not drug.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Drug with id {drug_id} does not exist")
    
    # Update drug
    drug.update(drug_detail, synchronize_session=False)
    return "Succesfully updated drug quantity."