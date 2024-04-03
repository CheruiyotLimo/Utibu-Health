# Utibu Health
This is an inventory tracking application designed to handle orders for medications and allowing administrators to effectively monitor and update their stock as well as track incoming medication orders from users.

## Intro
This is a backend API application built with Python using the FastAPI web framework and PostgresQL database that handles server-side logic including database CRUD operations through well-defined API endpoints
and client-side calls simulated by Postman. Check the link below for my Postman collection of all the endpoints.

## Project Navigation
- ## Regular user:
  - ### User sign-up and login:
      - Sign-up: Both regular and admin users sign up with their email and password credentials.
      - Log-in: On login, every user is granted a unique access token that authorizes them to perform specific actions.
  - ### View drugs in stock:
      - A user can see all the drugs in stock, their quantity and the price.
  - ### Create a medication order:
      - A user can make an order for a drug specifying the name of the drug and quantity then place their order.
  - ## View order history:
      - A user can view all their previous and current orders which includes the drug name, quantity bought, total price and a timestamp of the transaction.

- ## Admin user:
  - ### Drug Management:
    - Responsible for adding, removing and updating the drugs available in the healthcare facility.
  - ### View orders:
    - The admin user can view all current and previous orders which includes the drug name, quantity bought, total price and a timestamp of the transaction.
    - 
## Project Set-up
 - **Install Python 3.10:** You can download it from the official Python website: https://www.python.org/downloads/
 - ***OPTIONAL:*** Create a virtual environment by running `python -m venv venv` the activate it by navigating to `venv\Scripts\activate`
 - **Upgrade pip:** run `python -m pip install --upgrade pip`
 - **Install all required dependencies:** run `python -m pip install -r requirements.txt`
 - **Set-up database:** Create a .env file in the root directory and update it with contents of the [sample_env file](sample_env.txt) I have included here and update the env_file variable in [config.py file](app/config.py) to point to your new .env file. Feel free to update the other fields as necessary.
 - **Apply alembic migrations to new db:** Create an inital revision by running `python -m alembic revision --autogenerate -m "Create all db tables." then run `python -m alembic upgrade head` to apply the migrations.
 - **Initiate uvicorn server:** run `python -m uvicorn app.main:app --reload`
 - **Access sample Postman collection** To access the Utibu Collection, [click here](https://www.postman.com/solar-escape-154656/workspace/new-team-workspace/collection/25454935-910fdf80-d1b7-4410-b887-81ef8d1fa7b8?action=share&creator=25454935&active-environment=25454935-497b3698-b355-48fe-9a27-c9d81ff1f572)
 - **From Postman app:** Run the individual requests in the collection to see how Utibu works.

 ## Tech Stack
* Languages: Python
* DB: Postgresql
* Frameworks: FastAPI, Pydantic, SQLAlchemy, Alembic

## Contact Info
* email: [limzyon@gmail.com](mailto:limzyon@gmail.com)
* phone: +254729458728
