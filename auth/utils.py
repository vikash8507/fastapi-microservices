import uuid
from sqlalchemy.orm import Session
import models


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_token_by_user_id(db: Session, user_id: int):
    return db.query(models.Token).filter(models.Token.user_id == user_id).first()

def create_token(db: Session, user_id: int):
    db_token = models.Token(user_id=user_id, token=str(uuid.uuid4()))
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def get_user_id_by_token(db: Session, token: str):
    return db.query(models.Token).filter(models.Token.token == token).first()
