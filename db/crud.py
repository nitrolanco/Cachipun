from sqlalchemy.orm import Session
from db import models

################## USER ####################

def get_users(session: Session, skip: int = 0, limit = 20):
    return session.query(models.User).offset(skip).limit(limit).all()

def get_user(session: Session, user_id: int):
    return session.query(models.User).filter(models.User.id == user_id).first()

## Not working
def delete_user(session: Session, user_id: int):
    user = get_user(session, user_id)
    session.delete(user)
    session.commit()
    return user

def update_highscore(session: Session, user_id: int, points: int):
    user = get_user(session, user_id)
    user.highscore = points
    session.commit()

################## HISTORIAL ####################

def get_historial(session: Session, user_id: int, skip: int = 0, limit: int = 10):
    return session.query(models.Historial).filter(models.Historial.user_id == user_id).order_by("id").offset(skip).limit(limit).all()

def add_historial(session: Session, user_id: int, points: int):
    historial = models.Historial(user_id=user_id, points=points)
    session.add(historial)
    session.commit()
    session.refresh(historial)
    if historial.user.highscore < historial.points:
        update_highscore(session, user_id, historial.points)
    return historial
