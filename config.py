"""
Configuration management for Creatomate AI Agent
"""
from typing import Optional
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class CreatomateConfig(BaseSettings):
    """Configuration settings for Creatomate API"""
    
    # Creatomate API Configuration
    api_key: str = os.getenv("CREATOMATE_API_KEY", "")
    base_url: str = os.getenv("CREATOMATE_BASE_URL", "https://api.creatomate.com/v2")
    default_template_id: str = os.getenv("DEFAULT_TEMPLATE_ID", "cc493b27-5a2c-4218-b307-26a2420f2569")
    
    # Google Gemini Configuration
    google_api_key: str = os.getenv("GOOGLE_AI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    # Logging Configuration
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # API Server Configuration
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    
    # Composio Configuration
    composio_api_key: str = os.getenv("COMPOSIO_API_KEY", "")
    
    # YouTube Connected Account Configuration
    youtube_connected_account_id: str = os.getenv("YOUTUBE_CONNECTED_ACCOUNT_ID", "")
    youtube_user_id: str = os.getenv("YOUTUBE_USER_ID", "")
    
    # Facebook Connected Account Configuration
    facebook_connected_account_id: str = os.getenv("FACEBOOK_CONNECTED_ACCOUNT_ID", "")
    facebook_page_id: str = os.getenv("FACEBOOK_PAGE_ID", "")
    facebook_access_token: str = os.getenv("FACEBOOK_ACCESS_TOKEN", "")
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore"  # Allow extra fields from .env
    }

# Global configuration instance
config = CreatomateConfig()

def validate_config() -> bool:
    """Validate that required configuration is present"""
    required_fields = {
        "api_key": "CREATOMATE_API_KEY",
        "google_api_key": "GOOGLE_AI_API_KEY",
        "default_template_id": "DEFAULT_TEMPLATE_ID"
    }
    
    missing_fields = []
    for field, env_var in required_fields.items():
        value = getattr(config, field)
        if not value or value.startswith("your_") or value == "":
            missing_fields.append(env_var)
    
    if missing_fields:
        print(f"❌ Missing required configuration: {', '.join(missing_fields)}")
        print("Please update your .env file with the correct values")
        return False
    
    # Check optional social media integrations
    social_fields = {
        "composio_api_key": "COMPOSIO_API_KEY",
        "youtube_connected_account_id": "YOUTUBE_CONNECTED_ACCOUNT_ID", 
        "youtube_user_id": "YOUTUBE_USER_ID",
        "facebook_page_id": "FACEBOOK_PAGE_ID"
    }
    
    youtube_configured = all(getattr(config, field) for field in ["composio_api_key", "youtube_connected_account_id", "youtube_user_id"])
    facebook_configured = all(getattr(config, field) for field in ["composio_api_key", "facebook_connected_account_id", "facebook_page_id"])
    
    print("✅ Core configuration validated successfully")
    
    if youtube_configured:
        print("✅ YouTube integration configured")
    else:
        print("ℹ️  YouTube integration not configured")
    
    if facebook_configured:
        print("✅ Facebook integration configured")
    else:
        print("ℹ️  Facebook integration not configured")
        
    if not youtube_configured and not facebook_configured:
        print("   Social media uploads will not be available")
    
    return True