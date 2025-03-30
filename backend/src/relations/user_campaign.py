from src.users.models import User
from datetime import datetime, timezone
from src.campaigns.models import Campaign
from sqlalchemy import Table, Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.core.database import Base  




"""def setup_relationships():
    User.joined_campaigns = relationship(
        "Campaign",
        secondary=user_campaign_association,
        back_populates="participants"
    )
    
    Campaign.participants = relationship(
        "User",
        secondary=user_campaign_association,
        back_populates="joined_campaigns"
    )
    
    Campaign.owner = relationship("User", back_populates="campaigns")
    User.campaigns = relationship("Campaign", back_populates="owner")"""
