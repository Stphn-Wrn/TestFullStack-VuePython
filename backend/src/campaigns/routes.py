from flask import Blueprint, request, jsonify
from src.campaigns.services import CampaignService
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

campaigns_bp = Blueprint('campaigns', __name__, url_prefix='/campaigns')

@campaigns_bp.route('/', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Campaigns'],
    'description': 'Get all campaigns',
    'responses': {
        200: {
            'description': 'List of all campaigns',
            'schema': {
                'type': 'array',
                'items': {'$ref': '#/definitions/Campaign'}
            }
        },
        401: {'description': 'Unauthorized'},
        404: {'description': 'No campaigns found'}
    },
    'security': [{'BearerAuth': []}]
})
def get_all_campaigns():
    try:
        campaigns = CampaignService.get_all_campaigns()
        return jsonify(campaigns), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@campaigns_bp.route('/<int:campaign_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Campaigns'],
    'description': 'Get a specific campaign by ID',
    'parameters': [{
        'name': 'campaign_id',
        'in': 'path',
        'type': 'integer',
        'required': True,
        'description': 'ID of the campaign to retrieve'
    }],
    'responses': {
        200: {
            'description': 'Campaign details',
            'schema': {'$ref': '#/definitions/Campaign'}
        },
        401: {'description': 'Unauthorized'},
        404: {'description': 'Campaign not found'}
    },
    'security': [{'BearerAuth': []}]
})
def get_campaign(campaign_id):
    try:
        campaign = CampaignService.get_campaign_by_id(campaign_id)
        return jsonify(campaign), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@campaigns_bp.route('/', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Campaigns'],
    'description': 'Create a new campaign',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'name': {'type': 'string'},
                'description': {'type': 'string'},
                'start_date': {'type': 'string', 'format': 'date-time'},
                'end_date': {'type': 'string', 'format': 'date-time'},
                'budget': {'type': 'integer'},
                'status': {'type': 'boolean'}
            },
            'required': ['name']
        }
    }],
    'responses': {
        201: {
            'description': 'Campaign created successfully',
            'schema': {'$ref': '#/definitions/Campaign'}
        },
        400: {'description': 'Bad request'},
        401: {'description': 'Unauthorized'}
    },
    'security': [{'BearerAuth': []}]
})
def create_campaign():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    data['owner_id'] = current_user_id
    
    try:
        campaign = CampaignService.create_campaign(data)
        return jsonify(campaign), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@campaigns_bp.route('/<int:campaign_id>', methods=['PUT'])
@jwt_required()
@swag_from({
    'tags': ['Campaigns'],
    'description': 'Update an existing campaign',
    'parameters': [
        {
            'name': 'campaign_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the campaign to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'description': {'type': 'string'},
                    'start_date': {'type': 'string', 'format': 'date-time'},
                    'end_date': {'type': 'string', 'format': 'date-time'},
                    'budget': {'type': 'integer'},
                    'status': {'type': 'boolean'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Campaign updated successfully',
            'schema': {'$ref': '#/definitions/Campaign'}
        },
        400: {'description': 'Bad request'},
        401: {'description': 'Unauthorized'},
        403: {'description': 'Forbidden - Not the owner'}
    },
    'security': [{'BearerAuth': []}]
})
def update_campaign(campaign_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    try:
        campaign = CampaignService.get_campaign_by_id(campaign_id)
        if campaign['owner_id'] != current_user_id:
            return jsonify({"error": "Unauthorized"}), 403
            
        updated_campaign = CampaignService.update_campaign(campaign_id, data)
        return jsonify(updated_campaign), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@campaigns_bp.route('/<int:campaign_id>', methods=['DELETE'])
@jwt_required()
@swag_from({
    'tags': ['Campaigns'],
    'description': 'Delete a campaign',
    'parameters': [{
        'name': 'campaign_id',
        'in': 'path',
        'type': 'integer',
        'required': True,
        'description': 'ID of the campaign to delete'
    }],
    'responses': {
        200: {'description': 'Campaign deleted successfully'},
        401: {'description': 'Unauthorized'},
        403: {'description': 'Forbidden - Not the owner'},
        404: {'description': 'Campaign not found'}
    },
    'security': [{'BearerAuth': []}]
})
def delete_campaign(campaign_id):
    current_user_id = get_jwt_identity()
    
    try:
        campaign = CampaignService.get_campaign_by_id(campaign_id)
        if campaign['owner_id'] != current_user_id:
            return jsonify({"error": "Unauthorized"}), 403
            
        CampaignService.delete_campaign(campaign_id)
        return jsonify({"message": "Campaign deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400