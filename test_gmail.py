#!/usr/bin/env python3
"""
Test Gmail functionality only
"""
import os
from dotenv import load_dotenv
from composio import Composio

# Load environment variables
load_dotenv()

def test_gmail():
    """Test Gmail send functionality"""
    
    print("🧪 Testing Gmail functionality...")
    
    # Initialize Composio client
    composio_client = Composio(api_key=os.getenv("COMPOSIO_API_KEY"))
    gmail_connected_account_id = os.getenv("GMAIL_CONNECTED_ACCOUNT_ID")
    user_id = os.getenv("GMAIL_USER_ID")
    
    print(f"Gmail Connected Account ID: {gmail_connected_account_id}")
    print(f"Gmail User ID: {user_id}")
    
    # Test email parameters
    email_params = {
        "recipient_email": "coinvest518@gmail.com",
        "subject": "FDWA Gmail Test",
        "body": "This is a test email from FDWA AI Marketing Agent",
        "is_html": False,
        "entity_id": user_id or "me"
    }
    
    print(f"Email params: {email_params}")
    
    try:
        result = composio_client.tools.execute(
            "GMAIL_SEND_EMAIL",
            email_params,
            connected_account_id=gmail_connected_account_id,
            version=os.getenv("GMAIL_TOOL_VERSION", "20251111_00")
        )
        
        print(f"✅ Gmail result: {result}")
        
        if result.get("successful", False):
            print("✅ Gmail test PASSED - Email sent successfully!")
            return True
        else:
            print(f"❌ Gmail test FAILED: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Gmail test ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_gmail()
    if success:
        print("\n🎉 Gmail integration working!")
    else:
        print("\n💥 Gmail integration needs fixing")