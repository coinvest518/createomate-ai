#!/usr/bin/env python3
"""
Simple Test Flow - Create and Upload Video
"""
import asyncio
from fdwa_complete_agent import get_fdwa_agent

async def test_video_creation():
    """Test the complete video creation and upload flow"""
    
    print("🎬 Testing FDWA Video Creation Flow...")
    print("=" * 50)
    
    try:
        # Get the agent
        agent = get_fdwa_agent()
        print("✅ Agent initialized")
        
        # Create a simple video
        print("\n🎯 Creating video: 'AI Consulting Excellence'")
        print("📱 Template: single_scene (professional)")
        
        result = await agent.create_and_post_video(
            topic="AI Consulting Excellence",
            video_type="promotional", 
            template_style="single_scene"
        )
        
        print("\n" + "=" * 50)
        print("📊 RESULT:")
        print(result)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 FDWA Video Creation Test")
    asyncio.run(test_video_creation())