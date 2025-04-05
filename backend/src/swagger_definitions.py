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
        },
        "CSRFToken": {
            "type": "apiKey",
            "name": "X-CSRF-TOKEN",
            "in": "header",
            "description": "CSRF Token for protection against cross-site request forgery"
        }
    },
    "definitions": {
        "Campaign": {
            "type": "object",
            "required": ["name", "start_date", "end_date", "owner_id"],
            "properties": {
                "id": {"type": "integer", "readOnly": True},
                "name": {"type": "string", "minLength": 3, "maxLength": 100},
                "description": {"type": "string"},
                "start_date": {"type": "string", "format": "date-time"},
                "end_date": {"type": "string", "format": "date-time"},
                "budget": {"type": "integer", "minimum": 0},
                "status": {"type": "boolean"},
                "created_at": {"type": "string", "format": "date-time", "readOnly": True},
                "owner_id": {"type": "integer"},
                "owner": {"$ref": "#/definitions/User"}
            }
        },
        "CampaignCreate": {
            "type": "object",
            "required": ["name", "start_date", "end_date"],
            "properties": {
                "name": {"type": "string", "minLength": 3, "maxLength": 100},
                "description": {"type": "string"},
                "start_date": {"type": "string", "format": "date-time"},
                "end_date": {"type": "string", "format": "date-time"},
                "budget": {"type": "integer", "minimum": 0},
                "status": {"type": "boolean"}
            }
        },
        "CampaignUpdate": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "minLength": 3, "maxLength": 100},
                "description": {"type": "string"},
                "start_date": {"type": "string", "format": "date-time"},
                "end_date": {"type": "string", "format": "date-time"},
                "budget": {"type": "integer", "minimum": 0},
                "status": {"type": "boolean"}
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
        "ErrorResponse": {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "errors": {"type": "object"}
            }
        },
        "AuthResponse": {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "user_id": {"type": "integer"},
                "user": {"$ref": "#/definitions/User"},
                "access_token": {"type": "string"},
                "refresh_token": {"type": "string"}
            }
        },
        "TokenRefreshResponse": {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "access_token": {"type": "string"}
            }
        },
        "SuccessResponse": {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "data": {"type": "object"}
            }
        }
    },
    "paths": {
        "/api/campaigns": {
            "get": {
                "tags": ["Campaigns"],
                "summary": "Get all campaigns",
                "description": "Returns a list of all campaigns for the authenticated user",
                "security": [{"BearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "A list of campaigns",
                        "schema": {
                            "type": "array",
                            "items": {"$ref": "#/definitions/Campaign"}
                        }
                    },
                    "401": {"description": "Unauthorized - Invalid or missing JWT"},
                    "500": {"description": "Internal server error"}
                }
            },
            "post": {
                "tags": ["Campaigns"],
                "summary": "Create a new campaign",
                "description": "Creates a new campaign with the provided data",
                "security": [{"BearerAuth": []}, {"CSRFToken": []}],
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {"$ref": "#/definitions/CampaignCreate"}
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Campaign created successfully",
                        "schema": {"$ref": "#/definitions/SuccessResponse"}
                    },
                    "400": {
                        "description": "Validation error",
                        "schema": {"$ref": "#/definitions/ErrorResponse"}
                    },
                    "401": {"description": "Unauthorized - Invalid or missing JWT"},
                    "500": {"description": "Internal server error"}
                }
            }
        },
        "/api/campaigns/{campaign_id}": {
            "get": {
                "tags": ["Campaigns"],
                "summary": "Get a specific campaign",
                "description": "Returns details for a specific campaign",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "campaign_id",
                        "in": "path",
                        "description": "ID of the campaign to retrieve",
                        "required": True,
                        "type": "integer"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Campaign details",
                        "schema": {"$ref": "#/definitions/Campaign"}
                    },
                    "401": {"description": "Unauthorized - Invalid or missing JWT"},
                    "404": {"description": "Campaign not found"},
                    "500": {"description": "Internal server error"}
                }
            },
            "put": {
                "tags": ["Campaigns"],
                "summary": "Update a campaign",
                "description": "Updates an existing campaign",
                "security": [{"BearerAuth": []}, {"CSRFToken": []}],
                "parameters": [
                    {
                        "name": "campaign_id",
                        "in": "path",
                        "description": "ID of the campaign to update",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {"$ref": "#/definitions/CampaignUpdate"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Campaign updated successfully",
                        "schema": {"$ref": "#/definitions/SuccessResponse"}
                    },
                    "400": {
                        "description": "Validation error",
                        "schema": {"$ref": "#/definitions/ErrorResponse"}
                    },
                    "401": {"description": "Unauthorized - Invalid or missing JWT"},
                    "403": {"description": "Forbidden - User doesn't own the campaign"},
                    "404": {"description": "Campaign not found"},
                    "500": {"description": "Internal server error"}
                }
            },
            "delete": {
                "tags": ["Campaigns"],
                "summary": "Delete a campaign",
                "description": "Deletes an existing campaign",
                "security": [{"BearerAuth": []}, {"CSRFToken": []}],
                "parameters": [
                    {
                        "name": "campaign_id",
                        "in": "path",
                        "description": "ID of the campaign to delete",
                        "required": True,
                        "type": "integer"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Campaign deleted successfully",
                        "schema": {"$ref": "#/definitions/SuccessResponse"}
                    },
                    "401": {"description": "Unauthorized - Invalid or missing JWT"},
                    "403": {"description": "Forbidden - User doesn't own the campaign"},
                    "404": {"description": "Campaign not found"},
                    "500": {"description": "Internal server error"}
                }
            }
        },
        "/auth/register": {
            "post": {
                "tags": ["Authentication"],
                "summary": "Register a new user",
                "description": "Creates a new user account",
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {"$ref": "#/definitions/RegisterRequest"}
                    }
                ],
                "responses": {
                    "201": {
                        "description": "User created successfully",
                        "schema": {"$ref": "#/definitions/AuthResponse"}
                    },
                    "400": {
                        "description": "Validation error",
                        "schema": {"$ref": "#/definitions/ErrorResponse"}
                    },
                    "500": {"description": "Registration failed"}
                }
            }
        },
        "/auth/login": {
            "post": {
                "tags": ["Authentication"],
                "summary": "User login",
                "description": "Authenticates a user and returns a JWT token",
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {"$ref": "#/definitions/LoginRequest"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Login successful",
                        "schema": {"$ref": "#/definitions/AuthResponse"}
                    },
                    "400": {
                        "description": "Email and password required",
                        "schema": {"$ref": "#/definitions/ErrorResponse"}
                    },
                    "401": {
                        "description": "Invalid credentials",
                        "schema": {"$ref": "#/definitions/ErrorResponse"}
                    },
                    "500": {"description": "Login failed"}
                }
            }
        },
        "/auth/me": {
            "get": {
                "tags": ["Authentication"],
                "summary": "Get current user info",
                "description": "Returns information about the currently authenticated user",
                "security": [{"BearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "User details",
                        "schema": {"$ref": "#/definitions/User"}
                    },
                    "400": {
                        "description": "Invalid user ID",
                        "schema": {"$ref": "#/definitions/ErrorResponse"}
                    },
                    "401": {"description": "Unauthorized - Invalid or missing JWT"},
                    "404": {"description": "User not found"},
                    "500": {"description": "Server error"}
                }
            }
        },
        "/auth/refresh": {
            "post": {
                "tags": ["Authentication"],
                "summary": "Refresh access token",
                "description": "Generates a new access token using the refresh token",
                "security": [{"BearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "Token refreshed successfully",
                        "schema": {"$ref": "#/definitions/TokenRefreshResponse"}
                    },
                    "401": {
                        "description": "Invalid or expired refresh token",
                        "schema": {"$ref": "#/definitions/ErrorResponse"}
                    },
                    "500": {"description": "Token refresh failed"}
                }
            }
        },
        "/auth/logout": {
            "post": {
                "tags": ["Authentication"],
                "summary": "User logout",
                "description": "Invalidates the current session tokens",
                "security": [{"BearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "Logout successful",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string"}
                            }
                        }
                    },
                    "401": {"description": "Unauthorized - Invalid or missing JWT"},
                    "500": {"description": "Logout failed"}
                }
            }
        }
    },
    "security": [{"BearerAuth": []}]
}