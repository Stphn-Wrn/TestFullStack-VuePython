from src.core.database import db_session
from src.campaigns.models import Campaign
from src.campaigns.schemas import CampaignSchema, CampaignUpdateSchema
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

class CampaignService:
    @staticmethod
    def get_all_campaigns():
        campaigns = db_session.query(Campaign).all()
        return CampaignSchema(many=True).dump(campaigns)

    @staticmethod
    def get_campaign_by_id(campaign_id):
        campaign = db_session.query(Campaign).filter_by(id=campaign_id).first()
        if not campaign:
            raise ValueError("Campaign not found")
        return CampaignSchema().dump(campaign)

    @staticmethod
    def create_campaign(data):
        schema = CampaignSchema()
        campaign_data = schema.load(data)
        
        campaign = Campaign(**campaign_data)
        
        try:
            db_session.add(campaign)
            db_session.commit()
            return schema.dump(campaign)
        except SQLAlchemyError as e:
            db_session.rollback()
            raise ValueError(str(e))

    @staticmethod
    def update_campaign(campaign_id, data):
        schema = CampaignUpdateSchema()
        campaign_data = schema.load(data, partial=True)
        
        campaign = db_session.query(Campaign).filter_by(id=campaign_id).first()
        if not campaign:
            raise ValueError("Campaign not found")
            
        for key, value in campaign_data.items():
            setattr(campaign, key, value)
            
        try:
            db_session.commit()
            return CampaignSchema().dump(campaign)
        except SQLAlchemyError as e:
            db_session.rollback()
            raise ValueError(str(e))

    @staticmethod
    def delete_campaign(campaign_id):
        campaign = db_session.query(Campaign).filter_by(id=campaign_id).first()
        if not campaign:
            raise ValueError("Campaign not found")
            
        try:
            db_session.delete(campaign)
            db_session.commit()
            return True
        except SQLAlchemyError as e:
            db_session.rollback()
            raise ValueError(str(e))