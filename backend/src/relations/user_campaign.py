from backend.src.core.database import db
from backend.src.users.models import User
from backend.src.campaigns.database import Campaign

# Table d'association
user_campaign_association = db.Table(
    'user_campaign_association',
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('campaign_id', Integer, ForeignKey('campaigns.id'), primary_key=True),
    Column('joined_at', DateTime, default=datetime.utcnow)
)

# Configuration des relations (à importer dans vos modèles)
def setup_relationships():
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
    User.campaigns = relationship("Campaign", back_populates="owner")