import requests
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import  schemas, utils
from db import SessionLocal, engine

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/signup/", response_model=schemas.UserDetail)
def signeup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = utils.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return utils.create_user(db=db, user=user)

@app.post("/get-token/", response_model=schemas.TokenSchema)
def get_token(token: schemas.CreateTokenSchema):
    response = requests.post("http://auth:8000/get-token/", json={
        "email": token.email,
        "password": token.password,
    })
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=400, detail="Wrong credentials")
