#!/usr/bin/env python3
"""
FDWA Automated Marketing Scheduler - Smart Template Selection
Runs every hour, randomly selects templates, creates unique FDWA content
"""

import asyncio
import random
import schedule
import time
from datetime import datetime, timedelta
from typing import List, Dict
import structlog

# Import our FDWA agent
from fdwa_complete_agent import get_fdwa_agent

# Set up logging
logger = structlog.get_logger()

class FDWAAutoMarketing:
    """Automated FDWA marketing with smart template rotation and unique content"""
    
    def __init__(self):
        self.agent = get_fdwa_agent()
        
        # FDWA Business Topics - Comprehensive list for content variety
        self.fdwa_topics = [
            # AI Consulting Topics
            "AI Strategy Consulting for Modern Enterprises",
            "Custom AI Solutions That Drive ROI",
            "AI Implementation Roadmap for Success", 
            "Intelligent Automation for Business Growth",
            "AI-Powered Decision Making Systems",
            "Machine Learning Integration Services",
            
            # Digital Transformation Topics  
            "Complete Digital Transformation Journey",
            "Cloud Migration and Modernization",
            "Digital Workflow Optimization",
            "Future-Ready Business Technology",
            "Digital Innovation Consulting",
            "Smart Business Process Automation",
            
            # Business Growth Topics
            "Digital Wealth Creation Strategies",
            "Technology-Driven Business Scaling", 
            "AI-Enhanced Competitive Advantage",
            "Data-Driven Business Intelligence",
            "Digital Revenue Stream Development",
            "Automated Business Operations",
            
            # Industry Solutions
            "AI Solutions for Financial Services",
            "Digital Transformation for Healthcare",
            "Smart Manufacturing with AI",
            "Retail Automation and AI",
            "Real Estate Technology Innovation",
            "AI in Professional Services",
            
            # Thought Leadership
            "The Future of AI in Business",
            "Digital Wealth in the AI Era",
            "Building AI-First Organizations",
            "Sustainable AI Implementation",
            "Ethical AI for Business Growth",
            "AI ROI Measurement and Optimization"
        ]
        
        # Template styles with weights (higher = more likely)
        self.template_styles = {
            "single_scene": 30,    # Professional content
            "multi_scene": 35,     # Social media content  
            "quote": 35           # Educational content
        }
        
        # Track used topics to ensure variety
        self.recent_topics = []
        self.max_recent_topics = 10  # Remember last 10 topics
        
        logger.info("🤖 FDWA Auto Marketing initialized with smart template selection")
        logger.info("📱 Multi-platform posting: YouTube + Facebook")
    
    def get_unique_topic(self) -> str:
        """Get a unique topic that hasn't been used recently"""
        
        # Get available topics (not recently used)
        available_topics = [topic for topic in self.fdwa_topics 
                          if topic not in self.recent_topics]
        
        # If all topics used recently, reset the recent list
        if not available_topics:
            logger.info("🔄 All topics used recently, resetting variety tracker")
            self.recent_topics = []
            available_topics = self.fdwa_topics
        
        # Select random topic
        selected_topic = random.choice(available_topics)
        
        # Track usage
        self.recent_topics.append(selected_topic)
        if len(self.recent_topics) > self.max_recent_topics:
            self.recent_topics.pop(0)  # Remove oldest
        
        logger.info(f"📝 Selected unique topic: {selected_topic}")
        return selected_topic
    
    def select_random_template(self) -> str:
        """Randomly select a template style based on weights"""
        
        # Create weighted list
        weighted_templates = []
        for template, weight in self.template_styles.items():
            weighted_templates.extend([template] * weight)
        
        selected = random.choice(weighted_templates)
        logger.info(f"🎨 Selected template style: {selected}")
        return selected
    
    async def create_automated_content(self) -> Dict:
        """Create unique FDWA marketing content automatically"""
        
        try:
            # Get unique topic and random template
            topic = self.get_unique_topic()
            template_style = self.select_random_template()
            
            logger.info(f"🚀 Creating FDWA content: '{topic}' using '{template_style}' template")
            
            # Create the video with selected parameters
            result = await self.agent.create_and_post_video(
                topic=topic,
                video_type="promotional",  # Always promotional for FDWA
                template_style=template_style
            )
            
            return {
                "status": "success",
                "topic": topic,
                "template_style": template_style, 
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Automated content creation failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def run_hourly_marketing(self):
        """Run the automated marketing (called by scheduler)"""
        
        logger.info("⏰ Hourly FDWA marketing automation triggered")
        
        # Run async content creation
        try:
            result = asyncio.run(self.create_automated_content())
            
            if result["status"] == "success":
                logger.info(f"✅ Hourly marketing completed successfully")
                logger.info(f"📊 Topic: {result['topic']}")  
                logger.info(f"🎨 Template: {result['template_style']}")
            else:
                logger.error(f"❌ Hourly marketing failed: {result['error']}")
                
        except Exception as e:
            logger.error(f"💥 Critical error in hourly marketing: {e}")
    
    def start_scheduler(self):
        """Start the hourly scheduler"""
        
        logger.info("🕐 Starting FDWA hourly marketing scheduler")
        
        # Schedule every hour
        schedule.every().hour.do(self.run_hourly_marketing)
        
        # Optional: Run immediately on startup (for testing)
        logger.info("🎬 Running initial marketing content...")
        self.run_hourly_marketing()
        
        logger.info("✅ Scheduler active - FDWA marketing will run every hour")
        
        # Keep the scheduler running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

# Railway deployment function
async def railway_deployment_test():
    """Test function for Railway deployment"""
    
    logger.info("🚂 Railway deployment test starting...")
    
    auto_marketing = FDWAAutoMarketing()
    
    # Test content creation
    result = await auto_marketing.create_automated_content()
    
    if result["status"] == "success":
        logger.info("✅ Railway deployment test successful!")
        logger.info(f"Created content with topic: {result['topic']}")
        logger.info(f"Using template: {result['template_style']}")
        return True
    else:
        logger.error("❌ Railway deployment test failed")
        return False

# Main execution
if __name__ == "__main__":
    print("🤖 FDWA Automated Marketing System")
    print("=" * 50)
    print("✨ Features:")
    print("• Smart template rotation (single_scene, multi_scene, quote)")
    print("• Unique FDWA content generation every hour")  
    print("• Topic variety tracking (no repeats)")
    print("• LangSmith integration for monitoring")
    print("• Railway deployment ready")
    print()
    
    # Initialize the auto marketing system
    auto_marketing = FDWAAutoMarketing()
    
    print("Available Templates:")
    for template, weight in auto_marketing.template_styles.items():
        print(f"  • {template}: {weight}% likelihood")
    
    print(f"\nFDWA Business Topics: {len(auto_marketing.fdwa_topics)} unique topics")
    print("🕐 Starting hourly scheduler...")
    
    # Start the automated system
    auto_marketing.start_scheduler()