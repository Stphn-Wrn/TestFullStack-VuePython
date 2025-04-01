from src.core.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

class Campaign(Base):
    __tablename__ = 'campaigns'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    start_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    end_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    budget = Column(Integer)
    status = Column(Boolean)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    owner_id = Column(Integer, ForeignKey('users.id'))
    
    owner = relationship("src.users.models.User", back_populates="campaigns", lazy='joined')