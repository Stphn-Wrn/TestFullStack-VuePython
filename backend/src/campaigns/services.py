from src.core.database import db_session
from src.campaigns.models import Campaign
from src.campaigns.schemas import (
    CampaignSchema, 
    CampaignUpdateSchema
)
from datetime import datetime, timezone
from marshmallow import ValidationError
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import joinedload
class CampaignService:
    @staticmethod
    def create_campaign(data, owner_id):
        session = db_session()
        try:
            schema = CampaignSchema()
            validated_data = schema.load(data)
            
            if validated_data['end_date'] <= validated_data['start_date']:
                raise ValueError("end_date must be after start_date")
            
            campaign = Campaign(
                **validated_data,
                owner_id=owner_id,
                created_at=datetime.now(timezone.utc)
            )
            
            session.add(campaign)
            session.commit()
            
            session.refresh(campaign)
            if hasattr(campaign, 'owner'):
                session.refresh(campaign.owner)
            
            return campaign
            
        except ValidationError as e:
            session.rollback()
            raise ValueError({"message": "Validation failed", "errors": e.messages})
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Database error: {str(e)}")
        finally:
            session.close()

    @staticmethod
    def update_campaign(campaign_id, update_data):
        session = db_session()
        try:
            campaign = session.query(Campaign)\
                .options(joinedload(Campaign.owner))\
                .filter(
                    Campaign.id == campaign_id,
                    Campaign.owner_id == get_jwt_identity()
                ).first()
                
            if not campaign:
                raise ValueError("Campaign not found or access denied")

            if 'status' in update_data:
                update_data['is_active'] = update_data.pop('status')

            validated_data = CampaignUpdateSchema().load(update_data, partial=True)
            
            if 'start_date' in validated_data or 'end_date' in validated_data:
                new_start = validated_data.get('start_date', campaign.start_date)
                new_end = validated_data.get('end_date', campaign.end_date)
                if new_end <= new_start:
                    raise ValueError("end_date must be after start_date")

            for key, value in validated_data.items():
                setattr(campaign, key, value)
                
            session.commit()
            
            session.refresh(campaign)
            if hasattr(campaign, 'owner'):
                session.refresh(campaign.owner)
                
            return campaign
            
        except ValidationError as e:
            session.rollback()
            raise ValueError({"message": "Validation error", "errors": e.messages})
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Database error: {str(e)}")
        finally:
            session.close()

    @staticmethod
    def get_campaign(campaign_id):
        session = db_session()
        try:
            current_user_id = get_jwt_identity()
            campaign = session.query(Campaign)\
                .options(joinedload(Campaign.owner))\
                .filter(
                    Campaign.id == campaign_id,
                    Campaign.owner_id == current_user_id
                ).first()
                
            if not campaign:
                raise ValueError("Campaign not found or access denied")
            return campaign
        except SQLAlchemyError as e:
            raise ValueError(f"Database error: {str(e)}")
        finally:
            session.close()

    @staticmethod
    def get_user_campaigns():
        session = db_session()
        try:
            user_id = get_jwt_identity()
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