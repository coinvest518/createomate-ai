"""
FDWA Automated Marketing Scheduler
Runs hourly/daily to create and post marketing videos automatically
"""
import asyncio
import schedule
import time
from datetime import datetime, timedelta
from config import validate_config
import logging

# Import the working FDWA agent
try:
    from fdwa_complete_agent import get_fdwa_agent, FDWABrand
    AGENT_AVAILABLE = True
except ImportError as e:
    print(f"Import error: {e}")
    AGENT_AVAILABLE = False

# Set up logging for scheduler
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fdwa_marketing_scheduler.log'),
        logging.StreamHandler()
    ]
)

class FDWAMarketingScheduler:
    """Automated marketing video creation and posting scheduler"""
    
    def __init__(self):
        self.running = False
        self.last_run = None
        self.video_count = 0
        
        # Marketing topics rotation
        self.marketing_topics = [
            "AI Consulting services that transform businesses",
            "Digital Wealth Strategy for modern enterprises", 
            "Custom AI Development solutions",
            "Business Automation with AI technology",
            "Digital Transformation consulting",
            "AI-powered analytics for better decisions",
            "Smart technology solutions for growth",
            "Future-ready business with AI consulting"
        ]
        self.current_topic_index = 0
    
    async def create_scheduled_video(self):
        """Create and post a marketing video automatically"""
        try:
            print(f"\n🚀 FDWA Automated Marketing Run #{self.video_count + 1}")
            print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 60)
            
            # Validate configuration
            if not validate_config():
                logging.error("Configuration validation failed")
                return
            
            # Get current topic
            topic = self.marketing_topics[self.current_topic_index]
            self.current_topic_index = (self.current_topic_index + 1) % len(self.marketing_topics)
            
            print(f"📝 Topic: {topic}")
            print("🧠 AI generating content and creating video...")
            
            # Create marketing video with AI using the working agent
            if AGENT_AVAILABLE:
                agent = get_fdwa_agent()
                result = await agent.create_and_post_video(topic, template_style="single_scene")
                print(f"✅ Video created and posted: {result}")
            else:
                print("❌ FDWA agent not available")
                return
            
            self.video_count += 1
            self.last_run = datetime.now()
            
            print("✅ Automated marketing video created and posted!")
            print(f"📊 Videos created today: {self.video_count}")
            print(f"🌐 Promoting: {FDWABrand.WEBSITE}")
            print("=" * 60)
            
            # Log success
            logging.info(f"Successfully created marketing video #{self.video_count}")
            logging.info(f"Topic: {topic}")
            
        except Exception as e:
            logging.error(f"Scheduled video creation failed: {e}")
            print(f"❌ Scheduled run failed: {e}")
    
    def schedule_hourly(self):
        """Schedule marketing videos every hour"""
        schedule.every().hour.do(lambda: asyncio.create_task(self.create_scheduled_video()))
        print("📅 Scheduled: Hourly marketing videos")
    
    def schedule_daily(self, time_str="09:00"):
        """Schedule marketing videos daily at specified time"""
        schedule.every().day.at(time_str).do(lambda: asyncio.create_task(self.create_scheduled_video()))
        print(f"📅 Scheduled: Daily marketing videos at {time_str}")
    
    def schedule_business_hours(self):
        """Schedule videos during business hours (9 AM, 1 PM, 5 PM)"""
        schedule.every().day.at("09:00").do(lambda: asyncio.create_task(self.create_scheduled_video()))
        schedule.every().day.at("13:00").do(lambda: asyncio.create_task(self.create_scheduled_video()))
        schedule.every().day.at("17:00").do(lambda: asyncio.create_task(self.create_scheduled_video()))
        print("📅 Scheduled: Business hours marketing (9 AM, 1 PM, 5 PM)")
    
    async def run_scheduler(self):
        """Run the scheduler continuously"""
        self.running = True
        print("🚀 FDWA Marketing Scheduler Started")
        print(f"Company: {FDWABrand.COMPANY_NAME}")
        print(f"Website: {FDWABrand.WEBSITE}")
        print()
        
        try:
            while self.running:
                schedule.run_pending()
                await asyncio.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            print("\n👋 Scheduler stopped by user")
            self.running = False
        except Exception as e:
            logging.error(f"Scheduler error: {e}")
            print(f"❌ Scheduler error: {e}")
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        self.running = False
        print("⏹️ Scheduler stopping...")

# CLI for scheduler
async def main():
    """Main CLI for the scheduler"""
    scheduler = FDWAMarketingScheduler()
    
    print("🎯 FDWA Automated Marketing Scheduler")
    print("=" * 50)
    print("Choose scheduling option:")
    print("1. Run once now (test)")
    print("2. Schedule hourly")
    print("3. Schedule daily (9 AM)")
    print("4. Schedule business hours (9 AM, 1 PM, 5 PM)")
    print("5. Exit")
    print()
    
    choice = input("Select option (1-5): ").strip()
    
    if choice == "1":
        print("\n🧪 Running single test video creation...")
        await scheduler.create_scheduled_video()
        
    elif choice == "2":
        scheduler.schedule_hourly()
        print("\n⏰ Starting hourly scheduler...")
        print("Press Ctrl+C to stop")
        await scheduler.run_scheduler()
        
    elif choice == "3":
        scheduler.schedule_daily("09:00")
        print("\n📅 Starting daily scheduler (9 AM)...")
        print("Press Ctrl+C to stop")
        await scheduler.run_scheduler()
        
    elif choice == "4":
        scheduler.schedule_business_hours()
        print("\n🏢 Starting business hours scheduler...")
        print("Press Ctrl+C to stop")
        await scheduler.run_scheduler()
        
    elif choice == "5":
        print("👋 Goodbye!")
        return
        
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    print("🚀 Starting FDWA Marketing Scheduler...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Scheduler stopped.")
    except Exception as e:
        print(f"\n❌ Error: {e}")