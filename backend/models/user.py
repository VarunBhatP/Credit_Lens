from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    password_hash = Column(String, nullable=False)

    role = Column(String, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


scores = relationship(
    "Score",
    back_populates="user"
)