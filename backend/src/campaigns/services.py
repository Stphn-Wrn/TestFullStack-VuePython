from src.core.database import db_session
from src.campaigns.models import Campaign
from src.campaigns.schemas import (
    CampaignSchema, 
    CampaignUpdateSchema
)
from marshmallow import ValidationError
from flask_jwt_extended import get_jwt_identity

class CampaignService:
    @staticmethod
    def create_campaign(data, owner_id):
        session = db_session()
        try:
            schema = CampaignSchema()
            validated_data = schema.load(data)
            validated_data['owner_id'] = owner_id
            campaign = Campaign(**validated_data)
            session.add(campaign)
            session.commit()
            session.refresh(campaign)
            return campaign
        except ValidationError as e:
            session.rollback()
            raise ValueError(f"Validation error: {e.messages}")
        finally:
            session.close()


    @staticmethod
    def get_user_campaign(campaign_id):
        session = db_session()
        try:
            current_user_id = get_jwt_identity()
            campaign = session.query(Campaign).filter(
                Campaign.id == campaign_id,
                Campaign.owner_id == current_user_id
            ).first()
            
            if not campaign:
                raise ValueError("Campaign not found or access denied")
            return campaign
        finally:
            session.close()

    @staticmethod
    def update_campaign(campaign_id, update_data):
        session = db_session()
        try:
            current_user_id = get_jwt_identity()
            campaign = session.query(Campaign).filter(
                Campaign.id == campaign_id,
                Campaign.owner_id == current_user_id
            ).first()

            if not campaign:
                raise ValueError("Campaign not found or access denied")

            schema = CampaignUpdateSchema()
            validated_data = schema.load(update_data, partial=True)

            for key, value in validated_data.items():
                setattr(campaign, key, value)

            session.commit()

            session.refresh(campaign)  
            return campaign

        except ValidationError as e:
            session.rollback()
            raise ValueError(f"Validation error: {e.messages}")
        except Exception as e:
            session.rollback()
            raise RuntimeError(e)
        finally:
            session.close()

    @staticmethod
    def get_user_campaigns(user_id):
        session = db_session()
        try:
            return session.query(Campaign).filter(Campaign.owner_id == user_id).all()
        finally:
            session.close()

    @staticmethod
    def delete_campaign(campaign_id):
        session = db_session()
        try:
            current_user_id = get_jwt_identity()
            campaign = session.query(Campaign).filter(
                Campaign.id == campaign_id,
                Campaign.owner_id == current_user_id
            ).first()
            
            if not campaign:
                raise ValueError("Campaign not found or access denied")
                
            session.delete(campaign)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()