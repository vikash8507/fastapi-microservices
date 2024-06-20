import requests

from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request, db: Session = Depends(get_db)):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            user_id = self.verify_jwt(credentials.credentials)
            if user_id:
                return db.query(models.User).filter(models.User.id == user_id).first()
            raise HTTPException(status_code=403, detail="Invalid authentication token.")
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, token: str) -> bool:
        response = requests.post("http://auth:8000/validate-token/", json={"token": token})
        if response.status_code == 200:
            res = response.json()
            return res.get("user_id")

@app.post("/tasks/", response_model=schemas.TaskDetail)
def create_task(task: schemas.TaskBase, user: models.User = Depends(JWTBearer()), db: Session = Depends(get_db)):
    return utils.create_task(db=db, task=task, owner_id=user.id)

@app.get("/tasks/", response_model=list[schemas.TaskDetail])
def create_task(user: models.User = Depends(JWTBearer()), db: Session = Depends(get_db)):
    return utils.get_tasks_by_owner_id(db=db, owner_id=user.id)
