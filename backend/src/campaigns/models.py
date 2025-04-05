from datetime import datetime, timezone
from src.core.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    DateTime, 
    ForeignKey, 
    Text, 
    Boolean
)
class Campaign(Base):
    __tablename__ = 'campaigns'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    start_date = Column(DateTime, default=datetime.now(timezone.utc))
    end_date = Column(DateTime, default=datetime.now(timezone.utc))
    budget = Column(Integer)
    status = Column(Boolean)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    owner_id = Column(Integer, ForeignKey('users.id'))
       
    owner = relationship("User", lazy='joined')