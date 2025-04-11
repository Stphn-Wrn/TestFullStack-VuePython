from datetime import datetime, timezone
from src.core.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, 
    Text, Numeric, Boolean, CheckConstraint
)

class Campaign(Base):
    __tablename__ = 'campaigns'
    __table_args__ = (
        CheckConstraint('end_date > start_date', name='check_dates'),
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    budget = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True, 
                     doc="True=Active, False=Deactivated")
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    owner_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    
    owner = relationship("User", lazy='joined')

