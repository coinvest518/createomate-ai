#!/usr/bin/env python3

import asyncio
from fdwa_complete_agent import get_fdwa_agent

async def test_full_flow():
    """Simple test for the complete FDWA AI agent flow"""
    try:
        print("🚀 Starting FDWA AI Agent Test...")
        
        # Get agent instance
        agent = get_fdwa_agent()
        print("✅ Agent initialized")
        
        # Test single video creation and posting
        result = await agent.create_and_post_video(
            topic="AI Business Solutions",
            template_style="single_scene"
        )
        
        if result:
            print("✅ Full flow completed successfully!")
            print(f"📹 Video created and posted: {result}")
        else:
            print("❌ Flow failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_full_flow())