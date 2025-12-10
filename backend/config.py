import os
from typing import List

class Settings:
    """Application settings and configuration"""
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:8080,http://127.0.0.1:8080"
    ).split(",")
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: str = os.getenv("RATE_LIMIT_PER_MINUTE", "60/minute")
    
    # Contact Information (moved from frontend)
    WHATSAPP_NUMBER: str = os.getenv("WHATSAPP_NUMBER", "5491131095557")
    CONTACT_EMAIL: str = os.getenv("CONTACT_EMAIL", "info@moncton.com.ar")
    
    # Security Headers
    ENABLE_SECURITY_HEADERS: bool = os.getenv("ENABLE_SECURITY_HEADERS", "true").lower() == "true"
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

settings = Settings()
