swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Campaign Management API",
        "description": "API for managing campaigns with JWT cookie-based authentication",
        "version": "1.0.0",
        "contact": {
            "email": "contact@example.com"
        },
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        }
    },
    "host": "localhost:5000",
    "basePath": "/",
    "schemes": ["http", "https"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "securityDefinitions": {
        "JWT": {
            "type": "apiKey",
            "name": "X-CSRF-TOKEN",
            "in": "header",
            "description": "CSRF protection for JWT cookies. Include the CSRF token in headers for state-changing requests."
        }
    },
    "security": [{"JWT": []}],
    "tags": [
        {
            "name": "Authentication",
            "description": "User registration, login, and token management"
        },
        {
            "name": "Campaigns",
            "description": "Operations related to campaign management"
        }
    ],
    "paths": {
        "/api/auth/register": {
            "post": {
                "tags": ["Authentication"],
                "summary": "Register a new user",
                "description": "Creates a new user account and returns authentication cookies",
                "parameters": [
                    {
                        "in": "body",
                        "name": "body",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "username": {"type": "string", "example": "johndoe"},
                                "email": {"type": "string", "format": "email", "example": "user@example.com"},
                                "password": {"type": "string", "format": "password", "example": "securePassword123"}
                            },
                            "required": ["username", "email", "password"]
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "User created successfully",
                        "headers": {
                            "Set-Cookie": {
                                "type": "string",
                                "description": "Sets HTTP-only JWT cookies (access_token_cookie and refresh_token_cookie)"
                            }
                        },
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string", "example": "User created successfully"},
                                "user_id": {"type": "integer", "example": 1}
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid input data",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "error": {"type": "string", "example": "Email already registered"}
                            }
                        }
                    }
                }
            }
        },
        "/api/auth/login": {
            "post": {
                "tags": ["Authentication"],
                "summary": "Authenticate user",
                "description": "Logs in a user and returns authentication cookies",
                "parameters": [
                    {
                        "in": "body",
                        "name": "body",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "email": {"type": "string", "format": "email", "example": "user@example.com"},
                                "password": {"type": "string", "format": "password", "example": "securePassword123"}
                            },
                            "required": ["email", "password"]
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Login successful",
                        "headers": {
                            "Set-Cookie": {
                                "type": "string",
                                "description": "Sets HTTP-only JWT cookies (access_token_cookie and refresh_token_cookie)"
                            }
                        },
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string", "example": "Login successful"},
                                "user": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "integer"},
                                        "username": {"type": "string"},
                                        "email": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Invalid credentials",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "error": {"type": "string", "example": "Invalid email or password"}
                            }
                        }
                    }
                }
            }
        },
        "/api/auth/me": {
            "get": {
                "tags": ["Authentication"],
                "summary": "Get current user info",
                "description": "Returns information about the currently authenticated user",
                "security": [{"JWT": []}],
                "responses": {
                    "200": {
                        "description": "User information",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "username": {"type": "string"},
                                "email": {"type": "string"}
                            }
                        }
                    },
                    "401": {
                        "description": "Unauthorized",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "error": {"type": "string", "example": "Missing authorization token"}
                            }
                        }
                    }
                }
            }
        },
        "/api/auth/refresh": {
            "post": {
                "tags": ["Authentication"],
                "summary": "Refresh access token",
                "description": "Generates a new access token using the refresh token",
                "security": [{"JWT": []}],
                "responses": {
                    "200": {
                        "description": "Token refreshed successfully",
                        "headers": {
                            "Set-Cookie": {
                                "type": "string",
                                "description": "Sets new HTTP-only access_token_cookie"
                            }
                        },
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string", "example": "Token refreshed successfully"}
                            }
                        }
                    },
                    "401": {
                        "description": "Invalid or expired refresh token",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "error": {"type": "string", "example": "Token refresh failed"}
                            }
                        }
                    }
                }
            }
        },
        "/api/auth/logout": {
            "post": {
                "tags": ["Authentication"],
                "summary": "Logout user",
                "description": "Invalidates authentication cookies",
                "security": [{"JWT": []}],
                "responses": {
                    "200": {
                        "description": "Logout successful",
                        "headers": {
                            "Set-Cookie": {
                                "type": "string",
                                "description": "Clears JWT cookies"
                            }
                        },
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string", "example": "Logout successful"}
                            }
                        }
                    }
                }
            }
        },
        "/api/campaigns/": {
            "post": {
                "tags": ["Campaigns"],
                "summary": "Create a new campaign",
                "description": "Creates a new campaign for the authenticated user",
                "security": [{"JWT": []}],
                "parameters": [
                    {
                        "in": "body",
                        "name": "body",
                        "required": True,
                        "schema": {
                            "$ref": "#/definitions/Campaign"
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Campaign created successfully",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "data": {"$ref": "#/definitions/Campaign"},
                                "message": {"type": "string", "example": "Campaign created successfully"}
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid input data",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "error": {"type": "string"}
                            }
                        }
                    },
                    "401": {
                        "description": "Unauthorized"
                    }
                }
            }
        },
        "/api/campaigns/all": {
            "get": {
                "tags": ["Campaigns"],
                "summary": "Get all user campaigns",
                "description": "Returns all campaigns for the authenticated user",
                "security": [{"JWT": []}],
                "responses": {
                    "200": {
                        "description": "List of campaigns",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "data": {
                                    "type": "array",
                                    "items": {"$ref": "#/definitions/Campaign"}
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Unauthorized"
                    }
                }
            }
        },
        "/api/campaigns/{campaign_id}": {
            "get": {
                "tags": ["Campaigns"],
                "summary": "Get a specific campaign",
                "description": "Returns details for a specific campaign",
                "security": [{"JWT": []}],
                "parameters": [
                    {
                        "name": "campaign_id",
                        "in": "path",
                        "required": True,
                        "type": "integer",
                        "description": "ID of the campaign to retrieve"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Campaign details",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "data": {"$ref": "#/definitions/Campaign"}
                            }
                        }
                    },
                    "404": {
                        "description": "Campaign not found",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "error": {"type": "string", "example": "Campaign not found"}
                            }
                        }
                    }
                }
            },
            "patch": {
                "tags": ["Campaigns"],
                "summary": "Update a campaign",
                "description": "Updates an existing campaign",
                "security": [{"JWT": []}],
                "parameters": [
                    {
                        "name": "campaign_id",
                        "in": "path",
                        "required": True,
                        "type": "integer",
                        "description": "ID of the campaign to update"
                    },
                    {
                        "in": "body",
                        "name": "body",
                        "required": True,
                        "schema": {
                            "$ref": "#/definitions/CampaignUpdate"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Campaign updated successfully",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "data": {"$ref": "#/definitions/Campaign"},
                                "message": {"type": "string", "example": "Campaign updated successfully"}
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid input data",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "error": {"type": "string"}
                            }
                        }
                    }
                }
            },
            "delete": {
                "tags": ["Campaigns"],
                "summary": "Delete a campaign",
                "description": "Deletes an existing campaign",
                "security": [{"JWT": []}],
                "parameters": [
                    {
                        "name": "campaign_id",
                        "in": "path",
                        "required": True,
                        "type": "integer",
                        "description": "ID of the campaign to delete"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Campaign deleted successfully",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string", "example": "Campaign deleted successfully"}
                            }
                        }
                    },
                    "404": {
                        "description": "Campaign not found",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "error": {"type": "string", "example": "Campaign not found"}
                            }
                        }
                    }
                }
            }
        }
    },
    "definitions": {
        "Campaign": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "name": {"type": "string", "example": "Summer Sale"},
                "description": {"type": "string", "example": "Promotion for summer products"},
                "start_date": {"type": "string", "format": "date-time"},
                "end_date": {"type": "string", "format": "date-time"},
                "budget": {"type": "number", "format": "float", "example": 1000.0},
                "status": {"type": "string", "example": "active"},
                "owner_id": {"type": "integer", "example": 1}
            }
        },
        "CampaignUpdate": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "example": "Summer Sale"},
                "description": {"type": "string", "example": "Promotion for summer products"},
                "start_date": {"type": "string", "format": "date-time"},
                "end_date": {"type": "string", "format": "date-time"},
                "budget": {"type": "number", "format": "float", "example": 1000.0},
                "status": {"type": "string", "example": "active"}
            }
        }
    }
}