from sqlalchemy import BigInteger, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime

from app.db.database import Base


class Task(Base):
    __tablename__ = 'Task'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(57), nullable=False, unique=True)
    description: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())


class User(Base):
    __tablename__ = 'User'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    firstName: Mapped[str]
    lastName: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(unique=True)
