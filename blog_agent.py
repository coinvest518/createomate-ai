"""
FDWA Blog AI Sub-Agent - Affiliate Marketing Blog Generator
Converts video content into profitable HTML blog posts with affiliate links
"""
import json
import random
import os
from typing import Dict, Any
import structlog
from datetime import datetime

# Import main agent components
from config import config
from blog_templates import get_template_by_topic

# Set up logging
logger = structlog.get_logger()

class FDWABlogAgent:
    """
    AI Blog Sub-Agent that converts video content into affiliate marketing blog posts
    
    Features:
    - Converts video topics into engaging blog content
    - Automatically inserts relevant affiliate links
    - Creates SEO-optimized HTML blog posts
    - Emails blogs to Google Blogger for auto-posting
    - Tracks affiliate link performance
    """
    
    def __init__(self):
        self.blogger_email = "mildhighent.moneyovereverything@blogger.com"
        self.affiliate_links = self._load_affiliate_links()
        
        # Initialize AI for content generation
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            self.llm = ChatGoogleGenerativeAI(
                model=config.gemini_model,
                google_api_key=config.google_api_key,
                temperature=0.7  # Creative but focused
            )
            logger.info("🤖 Blog AI initialized for content generation")
        except Exception as e:
            logger.warning(f"Blog AI initialization failed: {e}")
            self.llm = None
        
        # Initialize Gmail client for blog posting
        try:
            from composio import Composio
            self.composio_client = Composio(api_key=config.composio_api_key)
            self.gmail_connected_account_id = config.gmail_connected_account_id
            logger.info("📧 Gmail client initialized for blog posting")
        except Exception as e:
            logger.error(f"Gmail initialization failed: {e}")
            self.composio_client = None
    
    def _load_affiliate_links(self) -> Dict:
        """Load affiliate links from JSON file"""
        try:
            with open('affiliate_links.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load affiliate links: {e}")
            return {}
    
    def generate_blog_content(self, video_topic: str, video_content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate blog content from video topic and content"""
        
        if self.llm:
            return self._ai_generate_blog(video_topic, video_content)
        else:
            return self._template_generate_blog(video_topic, video_content)
    
    def _ai_generate_blog(self, video_topic: str, video_content: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to generate engaging blog content"""
        try:
            main_message = video_content.get('main_message', video_topic)
            
            prompt = f"""Create an engaging blog post for entrepreneurs and business owners.
            
Video Topic: {video_topic}
Main Message: {main_message}
Company: FDWA (Futuristic Digital Wealth Agency)

Write a professional blog post that:
1. Hooks readers with a compelling title
2. Provides valuable business insights
3. Naturally mentions tools and solutions (for affiliate links)
4. Drives action toward FDWA services
5. Uses an engaging, authoritative tone
6. Focuses on business growth and AI automation

Generate:
- Title: Compelling, SEO-friendly (60 chars max)
- Intro: Hook paragraph that draws readers in
- Main Content Header: Engaging subheading
- Main Content: 2-3 paragraphs of valuable content
- Focus: Business transformation, AI, automation, growth

Return JSON format:
{{
    "title": "Compelling blog title here",
    "intro_paragraph": "Engaging opening paragraph",
    "main_content_header": "Compelling subheading",
    "main_content": "Valuable main content paragraphs"
}}"""

            response = self.llm.invoke(prompt)
            content_text = response.content
            
            # Parse JSON from AI response
            try:
                json_start = content_text.find('{')
                json_end = content_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_content = content_text[json_start:json_end]
                    blog_data = json.loads(json_content)
                    logger.info("🤖 AI generated blog content successfully")
                    return blog_data
            except json.JSONDecodeError:
                pass
            
            # Fallback to template
            logger.warning("AI blog parsing failed, using template")
            return self._template_generate_blog(video_topic, video_content)
            
        except Exception as e:
            logger.error(f"AI blog generation failed: {e}")
            return self._template_generate_blog(video_topic, video_content)
    
    def _template_generate_blog(self, video_topic: str, video_content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate blog content using smart templates"""
        
        main_message = video_content.get('main_message', video_topic)
        
        # Smart title generation
        if "ai" in video_topic.lower():
            title = f"How AI is Revolutionizing {video_topic.replace('AI', '').strip()}"
        elif "digital" in video_topic.lower():
            title = f"Digital Transformation: {main_message[:40]}..."
        else:
            title = f"Business Growth: {main_message[:40]}..."
        
        return {
            "title": title[:60],  # SEO limit
            "intro_paragraph": f"In today's competitive business landscape, {main_message.lower()} This comprehensive guide shows you exactly how to leverage cutting-edge tools and strategies to transform your business operations and accelerate growth.",
            "main_content_header": "Proven Strategies That Drive Results",
            "main_content": f"Successful entrepreneurs understand that {main_message.lower()} By implementing the right systems and tools, you can automate routine tasks, improve efficiency, and focus on high-value activities that drive revenue. The key is choosing solutions that scale with your business and provide measurable ROI."
        }
    
    def create_html_blog(self, video_topic: str, video_content: Dict[str, Any]) -> str:
        """Create complete HTML blog post with affiliate links and AI-generated image"""
        
        # Generate blog content
        blog_content = self.generate_blog_content(video_topic, video_content)
        
        # No image generation - clean blog content only
        blog_image_html = ""  # No image needed
        
        # Select appropriate template
        template = get_template_by_topic(video_topic)
        
        # Prepare affiliate links for template
        affiliate_vars = {
            'affiliate_hostinger': self.affiliate_links.get('website_hosting', {}).get('hostinger', {}).get('url', '#'),
            'affiliate_lovable': self.affiliate_links.get('ai_tools', {}).get('lovable', {}).get('url', '#'),
            'affiliate_openphone': self.affiliate_links.get('business_tools', {}).get('openphone', {}).get('url', '#'),
            'affiliate_veed': self.affiliate_links.get('content_tools', {}).get('veed', {}).get('url', '#'),
            'affiliate_elevenlabs': self.affiliate_links.get('ai_tools', {}).get('elevenlabs', {}).get('url', '#'),
            'affiliate_manychat': self.affiliate_links.get('business_tools', {}).get('manychat', {}).get('url', '#'),
            'affiliate_n8n': self.affiliate_links.get('business_tools', {}).get('n8n', {}).get('url', '#'),
            'affiliate_brightdata': self.affiliate_links.get('data_tools', {}).get('brightdata', {}).get('url', '#'),
            'affiliate_cointiply': self.affiliate_links.get('financial', {}).get('cointiply', {}).get('url', '#'),
            'affiliate_ava': self.affiliate_links.get('financial', {}).get('ava', {}).get('url', '#'),
            'affiliate_theleap': self.affiliate_links.get('digital_products', {}).get('theleap', {}).get('url', '#'),
            'affiliate_amazon': self.affiliate_links.get('digital_products', {}).get('amazon', {}).get('url', '#')
        }
        
        # Merge blog content, affiliate links, and image
        template_vars = {**blog_content, **affiliate_vars, "blog_image": blog_image_html}
        
        # Generate final HTML
        html_blog = template.format(**template_vars)
        
        logger.info(f"📝 Created HTML blog: {blog_content['title']}")
        return html_blog
    
    def email_blog_to_blogger(self, html_content: str, blog_title: str) -> Dict[str, Any]:
        """Email HTML blog to Google Blogger"""
        
        if not self.composio_client:
            return {"status": "error", "message": "Gmail not configured"}
        
        try:
            # Create email subject (Blogger uses this as post title)
            email_subject = blog_title
            
            # Send clean HTML email to Blogger
            email_params = {
                "recipient_email": self.blogger_email,
                "subject": email_subject,
                "body": html_content,
                "is_html": True,
                "user_id": "me"
            }
            
            logger.info(f"📧 Sending blog to Blogger: {blog_title[:50]}...")
            result = self.composio_client.tools.execute(
                "GMAIL_SEND_EMAIL",
                email_params,
                connected_account_id=self.gmail_connected_account_id,
                version=os.getenv("GMAIL_TOOL_VERSION", "20251111_00")
            )
            
            if result.get("successful", False):
                logger.info(f"✅ Blog posted to Blogger successfully")
                return {
                    "status": "success",
                    "platform": "Google Blogger",
                    "title": blog_title,
                    "message": "Blog posted successfully to Blogger!"
                }
            else:
                error_msg = result.get("error", "Unknown error")
                logger.error(f"❌ Blogger posting failed: {error_msg}")
                return {"status": "error", "message": f"Blogger posting failed: {error_msg}"}
                
        except Exception as e:
            logger.error(f"Blog posting failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def create_and_post_blog(self, video_topic: str, video_content: Dict[str, Any]) -> Dict[str, Any]:
        """Complete workflow: Create blog from video content and post to Blogger"""
        
        try:
            logger.info(f"📝 Creating affiliate blog from: {video_topic}")
            
            # Step 1: Create HTML blog with affiliate links
            html_blog = self.create_html_blog(video_topic, video_content)
            
            # Step 2: Extract title for email subject
            title_start = html_blog.find('<h1>') + 4
            title_end = html_blog.find('</h1>')
            blog_title = html_blog[title_start:title_end] if title_start > 3 and title_end > title_start else video_topic
            
            # Step 3: Email to Blogger (text only)
            result = self.email_blog_to_blogger(html_blog, blog_title)
            
            if result.get("status") == "success":
                logger.info("🎯 Blog workflow completed successfully")
                return {
                    "status": "success",
                    "blog_title": blog_title,
                    "html_content": html_blog[:200] + "...",  # Preview
                    "posted_to": "Google Blogger",
                    "affiliate_links_included": len([k for k in html_blog if 'affiliate_' in k]),
                    "message": "Affiliate marketing blog created and posted!"
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"Blog workflow failed: {e}")
            return {"status": "error", "message": str(e)}

# Global blog agent instance
blog_agent = None

def get_blog_agent() -> FDWABlogAgent:
    """Get or create the blog agent"""
    global blog_agent
    if blog_agent is None:
        blog_agent = FDWABlogAgent()
    return blog_agent

# Quick test function
def test_blog_creation():
    """Test blog creation with sample content"""
    agent = get_blog_agent()
    
    test_content = {
        "main_message": "Transform your business with AI automation",
        "youtube_title": "AI Business Transformation",
        "youtube_description": "Learn how AI can revolutionize your business operations"
    }
    
    result = agent.create_and_post_blog("AI Business Automation", test_content)
    print("Blog Test Result:", result)

if __name__ == "__main__":
    print("🤖 FDWA Blog AI Sub-Agent")
    print("=" * 50)
    print("✨ Features:")
    print("• Converts video content to affiliate marketing blogs")
    print("• Automatically inserts relevant affiliate links")
    print("• Posts directly to Google Blogger via email")
    print("• SEO-optimized HTML content")
    print("• AI-powered content generation")
    print()
    
    # Test the blog agent
    test_blog_creation()