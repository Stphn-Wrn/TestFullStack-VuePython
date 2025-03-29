from datetime import datetime
from backend.src.core.database import Base

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    start_date = Column(datetime, default=datetime.utcnow)
    end_date = Column(datetime, default=datetime.utcnow)
    budget = Column(Integer)
    status = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey('users.id'))