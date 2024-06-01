from sqlalchemy.orm import Session
from db import models

def get_users(session: Session):
    return session.query(models.User).first()

def get_user(session: Session, user_id: int):
    return session.query(models.User).filter(models.User.id == user_id).first()

def get_historial(session: Session, user_id: int, skip: int = 0, limit: int = 10):
    return session.query(models.Historial).filter(models.Historial.user_id == user_id).order_by("id").offset(skip).limit(limit).all()
