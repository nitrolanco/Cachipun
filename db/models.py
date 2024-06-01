from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import *
from typing import List


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    kind: Mapped[str] = mapped_column(String(50))
    highscore: Mapped[int]
    historial: Mapped[List["Historial"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "kind": self.kind,
            "highscore": self.highscore,
        }


class Historial(db.Model):
    __tablename__ = "historial"

    id: Mapped[int] = mapped_column(primary_key=True)
    points: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="historial")
