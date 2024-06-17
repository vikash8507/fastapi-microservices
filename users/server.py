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

@app.post("/signin/", response_model=schemas.TokenSchema)
def signin(user: schemas.UserLoginSchema, db: Session = Depends(get_db)):
    db_user = utils.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    if db_user.hashed_password != user.password + "notreallyhashed":
        raise HTTPException(status_code=400, detail="Wrong credentials")
    db_token = utils.get_user_token_by_user_id(db, db_user.id)
    if db_token:
        return db_token
    return utils.create_token(db, db_user.id)
