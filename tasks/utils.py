from sqlalchemy.orm import Session
import models, schemas


def get_task_by_id(db: Session, id: int):
    return db.query(models.Task).filter(models.Task.id == id).first()


def create_task(db: Session, task: schemas.TaskBase, owner_id: int):
    db_task = models.Task(title=task.title, description=task.description, owner_id=owner_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks_by_owner_id(db: Session, owner_id: int):
    return db.query(models.Task).filter(models.Task.owner_id == owner_id).all()
