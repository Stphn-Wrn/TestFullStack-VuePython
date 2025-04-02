swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Campaign API",
        "description": "API for managing marketing campaigns and user authentication",
        "version": "1.0.0",
        "contact": {
            "email": "contact@example.com"
        }
    },
    "basePath": "/",  
    "schemes": ["http", "https"],
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
        }
    },
    "definitions": {
        "Campaign": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "description": {"type": "string"},
                "start_date": {"type": "string", "format": "date-time"},
                "end_date": {"type": "string", "format": "date-time"},
                "budget": {"type": "integer"},
                "status": {"type": "boolean"},
                "created_at": {"type": "string", "format": "date-time"},
                "owner_id": {"type": "integer"}
            }
        },
        "User": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "username": {"type": "string"},
                "email": {"type": "string"},
                "created_at": {"type": "string", "format": "date-time"}
            }
        },
        "LoginRequest": {
            "type": "object",
            "required": ["email", "password"],
            "properties": {
                "email": {"type": "string"},
                "password": {"type": "string"}
            }
        },
        "RegisterRequest": {
            "type": "object",
            "required": ["username", "email", "password"],
            "properties": {
                "username": {"type": "string"},
                "email": {"type": "string"},
                "password": {"type": "string"}
            }
        },
        
    }
}