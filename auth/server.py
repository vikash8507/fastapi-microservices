from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import  models, schemas, utils
from db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/get-token/", response_model=schemas.TokenSchema)
def get_token(user: schemas.CreateTokenSchema, db: Session = Depends(get_db)):
    db_user = utils.get_user_by_email(db, email=user.email)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found")
    if db_user.hashed_password != user.password + "notreallyhashed":
        raise HTTPException(status_code=400, detail="User credential is wrong")
    db_token = utils.get_user_token_by_user_id(db, db_user.id)
    if db_token:
        return db_token
    return utils.create_token(db=db, user_id=db_user.id)

@app.post("/validate-token/", response_model=schemas.TokenValidateResponseSchema)
def validate_token(token: schemas.TokenSchema, db: Session = Depends(get_db)):
    db_token = utils.get_user_id_by_token(db, token.token)
    if db_token is None:
        raise HTTPException(status_code=400, detail="Wrong token")
    return {"user_id": db_token.user_id}
