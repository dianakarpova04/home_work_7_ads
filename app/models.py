"""
Modules for predictions DataBase and column types
"""

from sqlalchemy import Column, Integer, DateTime, String
from .database import Base


class FRAUDORNOT(Base):
    """
    Class for DataBase with predictions
    """
    __tablename__ = "fraud_or_not_predictions"

    id = Column(Integer, primary_key=True)
    message_text = Column(String, nullable=False)
    prediction = Column(String, nullable=False)
    used_base_line = Column(String, nullable=False)
    request_time = Column(DateTime, nullable=False)
