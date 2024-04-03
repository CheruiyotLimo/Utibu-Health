from fastapi import FastAPI
from .routers import auth, orders, users, drugs   #replace these with the appropriate routes being imported.

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router) 
app.include_router(drugs.router) 
app.include_router(orders.router) 

@app.get("/")
async def root():
    return {"message": "Hello World from Utibu Healthcare!"}