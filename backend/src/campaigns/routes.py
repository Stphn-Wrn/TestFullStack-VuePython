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


campaign_schema = CampaignSchema()
campaign_update_schema = CampaignUpdateSchema()

campaign_bp = Blueprint('campaigns', __name__, url_prefix='/api/campaigns')

@campaign_bp.route('/', methods=['POST'])
@jwt_required()
def create_campaign():
    try:
        current_user_id = get_jwt_identity()
        data = campaign_schema.load(request.get_json())  # Validation complète
        data['owner_id'] = current_user_id  # Ajout sécurisé
        
        campaign = CampaignService.create_campaign(data)
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

@campaign_bp.route('/<int:campaign_id>', methods=['PUT'])
@jwt_required()
def update_campaign(campaign_id):
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