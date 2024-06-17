import uuid
from sqlalchemy.orm import Session
import models, schemas


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, first_name=user.first_name, is_active=True, last_name=user.last_name, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_token_by_user_id(db: Session, user_id: int):
    return db.query(models.Token).filter(models.Token.user_id == user_id).first()

def create_token(db: Session, user_id: int):
    db_token = models.Token(user_id=user_id, token=str(uuid.uuid4()))
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token
