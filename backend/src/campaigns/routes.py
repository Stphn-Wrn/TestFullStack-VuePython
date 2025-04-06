from flask import (
    Blueprint, 
    request, 
    jsonify
)
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity
)
from src.campaigns.schemas import (
    CampaignSchema, 
    CampaignUpdateSchema
)
from src.campaigns.services import CampaignService
from src.core.database import db_session
from marshmallow import ValidationError


campaign_schema = CampaignSchema()
campaign_update_schema = CampaignUpdateSchema()

campaign_bp = Blueprint('campaigns', __name__)

@campaign_bp.route('/', methods=['POST', 'OPTIONS'])
@jwt_required()
def create_campaign():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = campaign_schema.load(request.get_json())
        owner_id = get_jwt_identity()

        campaign = CampaignService.create_campaign(data, owner_id)
        return jsonify({
            "data": campaign_schema.dump(campaign),
            "message": "Campaign created successfully"
        }), 201
        
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@campaign_bp.route('/<int:campaign_id>', methods=['GET'])
@jwt_required()
def get_campaign(campaign_id):
    try:
        campaign = CampaignService.get_user_campaign(campaign_id)
        if not campaign:
            return jsonify({"error": "Campaign not found"}), 404
            
        return jsonify({
            "data": campaign_schema.dump(campaign)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@campaign_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_campaigns():
    try:
        current_user_id = get_jwt_identity()
        campaigns = CampaignService.get_user_campaigns(current_user_id)
        
        return jsonify({
            "data": campaign_schema.dump(campaigns, many=True)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@campaign_bp.route('/<int:campaign_id>', methods=['PUT', 'OPTIONS'])
@jwt_required()
def update_campaign(campaign_id):
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = campaign_update_schema.load(request.get_json(), partial=True)
        campaign = CampaignService.update_campaign(campaign_id, data)
        
        return jsonify({
            "data": campaign_schema.dump(campaign),
            "message": "Campaign updated successfully"
        }), 200
        
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@campaign_bp.route('/<int:campaign_id>', methods=['DELETE', 'OPTIONS'])
@jwt_required()
def delete_campaign(campaign_id):
    if request.method == 'OPTIONS':
        return '', 200
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