from sqlalchemy import Column, Integer, String, DateTime, Float
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

    # Borrower profile data
    income = Column(Integer, nullable=True)
    employment_days = Column(Integer, nullable=True)
    age = Column(Integer, nullable=True)

    # Extracted from CSV
    amt_credit = Column(Integer, nullable=True, default=0)
    amt_annuity = Column(Integer, nullable=True, default=0)

    # Derived from UPI analysis
    ext_source_2 = Column(Float, nullable=True, default=0.5)
    ext_source_3 = Column(Float, nullable=True, default=0.5)

    # Relationship
    scores = relationship("Score", back_populates="user")