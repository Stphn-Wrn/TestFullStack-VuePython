from sqlalchemy import (
    create_engine, 
    Table, 
    Column, 
    Integer, 
    DateTime, 
    ForeignKey
)
from sqlalchemy.orm import (
    declarative_base, 
    sessionmaker
)
from datetime import datetime, timezone
import os 


engine = create_engine(os.getenv("DATABASE_URL", "postgresql://stephen:test@psql/campaign"), pool_size=20, max_overflow=0)
db_session = sessionmaker(bind=engine)
Base = declarative_base()

user_campaign_association = Table(
    'user_campaign_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey("users.id"), primary_key=True), 
    Column('campaign_id', Integer, ForeignKey("campaigns.id"), primary_key=True), 
    Column('joined_at', DateTime, default=datetime.now(timezone.utc))
)