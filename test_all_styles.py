#!/usr/bin/env python3
"""
Test All Template Styles - See Different Video Types
"""
import asyncio
from fdwa_complete_agent import get_fdwa_agent

async def test_all_templates():
    """Test all three template styles"""
    
    agent = get_fdwa_agent()
    
    templates = [
        ("single_scene", "Professional AI Consulting"),
        ("multi_scene", "Digital Transformation Success"), 
        ("quote", "AI Business Benefits")
    ]
    
    for template_style, topic in templates:
        print(f"\n🎬 Testing {template_style}: {topic}")
        print("-" * 40)
        
        try:
            result = await agent.create_and_post_video(
                topic=topic,
                template_style=template_style
            )
            print(f"✅ {template_style} completed")
            print(result[:200] + "..." if len(result) > 200 else result)
            
        except Exception as e:
            print(f"❌ {template_style} failed: {e}")
        
        print("\n" + "="*50)

if __name__ == "__main__":
    asyncio.run(test_all_templates())