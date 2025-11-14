"""
FDWA Marketing Trigger - Single Command Video Creation & Posting
One command creates AI-generated video and posts to YouTube
"""
import asyncio
from fdwa_complete_agent import get_fdwa_agent, create_marketing_video, auto_marketing_campaign, FDWABrand
from config import validate_config
import sys

async def single_trigger_marketing():
    """Single trigger that creates and posts a marketing video"""
    
    if not validate_config():
        print("❌ Configuration failed!")
        return
    
    try:
        result = await auto_marketing_campaign()
        print(result)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🎯 FDWA Single-Trigger Marketing System")
    print("This will create and post a marketing video automatically.")
    print()
    
    try:
        asyncio.run(single_trigger_marketing())
    except KeyboardInterrupt:
        print("\n👋 Marketing workflow stopped.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)