from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base


class LenderSelection(Base):
    __tablename__ = "lender_selections"

    id = Column(Integer, primary_key=True)

    borrower_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    lender_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    selected_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )