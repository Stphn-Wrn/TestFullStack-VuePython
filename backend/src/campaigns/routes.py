from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.campaigns.services import CampaignService
from src.core.database import db_session
from src.campaigns.schemas import CampaignSchema

campaign_bp = Blueprint('campaigns', __name__, url_prefix='/api/campaigns')

@campaign_bp.route('/', methods=['POST'])
@jwt_required()
def create_campaign():
    session = db_session()
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        campaign = CampaignService.create_campaign(data, owner_id=current_user_id)
        
        return jsonify({
            "id": campaign.id,
            "name": campaign.name,
            "message": "Campaign created successfully"
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@campaign_bp.route('/<int:campaign_id>', methods=['GET'])
@jwt_required()
def get_campaign(campaign_id):
    try:
        campaign = CampaignService.get_user_campaign(campaign_id)
        if not campaign:
            return jsonify({"error": "Campaign not found"}), 404
            
        schema = CampaignSchema()
        return jsonify(schema.dump(campaign)), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@campaign_bp.route('/<int:campaign_id>', methods=['PUT'])
@jwt_required()
def update_campaign(campaign_id):
    session = db_session()
    try:
        data = request.get_json()
        campaign = CampaignService.update_campaign(campaign_id, data)
        return jsonify({
            "id": campaign.id,
            "name": campaign.name,
            "message": "Campaign updated successfully"
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        session.rollback()
        return jsonify({"error": "Internal server error"}), 500
    finally:
        session.close()

@campaign_bp.route('/<int:campaign_id>', methods=['DELETE'])
@jwt_required()
def delete_campaign(campaign_id):
    session = db_session()
    try:
        CampaignService.delete_campaign(campaign_id)
        return jsonify({"message": "Campaign deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        session.rollback()
        return jsonify({"error": "Internal server error"}), 500
    finally:
        session.close()