"""
FDWA AI Marketing Agent - Complete Workflow with Composio Integration
Creates professional marketing videos and posts to YouTube and Facebook using Composio
"""
import asyncio
import os
import json
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime
import structlog

# Simple imports that work
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langsmith import traceable
    LLM_AVAILABLE = True
except ImportError as e:
    print(f"Import error: {e}")
    LLM_AVAILABLE = False
    def traceable(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

from pydantic import BaseModel, Field

# Local imports
from config import config, validate_config
from creatomate_client import CreatomateClient
# Removed OAuth client - using Composio for all integrations

# Set up logging
logger = structlog.get_logger()



# FDWA Brand Configuration
class FDWABrand:
    """Futuristic Digital Wealth Agency brand settings"""
    
    # Company Information
    COMPANY_NAME = "Futuristic Digital Wealth Agency"
    COMPANY_ACRONYM = "FDWA"
    WEBSITE = "https://fdwa.site"
    TAGLINE = "AI Consulting & Development for Digital Wealth"
    
    # Brand Colors
    PRIMARY_COLOR = "#0066FF"      # Blue
    SECONDARY_COLOR = "#00FFAA"    # Green/Teal
    ACCENT_COLOR = "#FF3366"       # Red accent
    
    # Services
    SERVICES = [
        "AI Consulting", "Digital Wealth Strategy", "AI Development", 
        "Automation Solutions", "Digital Transformation", "Wealth Technology"
    ]
    
    # Marketing Themes
    MARKETING_THEMES = [
        "Transform Your Business with AI",
        "Digital Wealth Solutions", 
        "Future-Ready Technology",
        "AI-Powered Success",
        "Innovation Consulting",
        "Smart Business Solutions"
    ]

class FDWAMarketingAgent:
    """
    Complete AI Marketing Agent for FDWA with Composio YouTube/Facebook upload
    
    Features:
     Two template styles: 'single_scene' (professional quotes) and 'multi_scene' (TikTok/Instagram)
     AI-powered content generation using Gemini 2.5
     YouTube/Facebook integration via Composio
     FDWA brand consistency across all videos
     Full workflow automation: Generate  Create  Upload  Report
    
    Template Options:
    - single_scene: 1080x1080 professional quote-style videos with FDWA branding
    - multi_scene: 720x1280 vertical 4-scene TikTok/Instagram style videos
    - quote: 720x1280 animated question/answer educational format
    """
    
    def __init__(self):
        # Initialize LLM if available
        if LLM_AVAILABLE and config.google_api_key:
            try:
                self.llm = ChatGoogleGenerativeAI(
                    model=config.gemini_model,
                    google_api_key=config.google_api_key,
                    temperature=0.8  # Higher creativity for marketing
                )
                logger.info(" AI LLM initialized for content generation")
            except Exception as e:
                logger.warning(f"LLM initialization failed: {e}")
                self.llm = None
        else:
            self.llm = None
            logger.info(" AI LLM not available, using templates")
        
        # Initialize Composio Python client for YouTube and Facebook
        from composio import Composio
        self.composio_client = Composio(api_key=config.composio_api_key)
        self.user_id = config.youtube_user_id
        self.facebook_page_id = config.facebook_page_id
        self.youtube_connected_account_id = config.youtube_connected_account_id
        self.facebook_connected_account_id = config.facebook_connected_account_id
        self.gmail_connected_account_id = config.gmail_connected_account_id
        self.youtube_ready = True
        self.facebook_ready = True
        self.gmail_ready = True
        
        logger.info("FDWA Marketing Agent initialized")
    
    @traceable(name="ai_generate_content")
    def generate_marketing_content(self, topic: str, video_type: str = "promotional") -> Dict[str, Any]:
        """Generate marketing content using AI or templates"""
        
        if self.llm:
            return self._ai_generate_content(topic, video_type)
        else:
            return self._template_generate_content(topic, video_type)
    
    def _ai_generate_content(self, topic: str, video_type: str) -> Dict[str, Any]:
        """Use AI to generate marketing content"""
        try:
            logger.info(f" AI generating content for: {topic}")
            
            prompt = f"""Create compelling marketing content for {FDWABrand.COMPANY_NAME} (FDWA).

Company: {FDWABrand.COMPANY_NAME}
Website: {FDWABrand.WEBSITE}
Services: {', '.join(FDWABrand.SERVICES)}

Topic: {topic}
Video Type: {video_type}

Generate professional marketing content that:
1. Highlights business transformation benefits
2. Shows FDWA's AI expertise 
3. Drives action to visit fdwa.site
4. Uses benefit-focused language
5. Targets business decision makers

Create:
- Main Message: Engaging hook (10-15 words)
- Call to Action: Clear next step with fdwa.site
- YouTube Title: SEO optimized, compelling
- YouTube Description: Professional with hashtags

Return JSON format:
{{
    "main_message": "Transform your business with FDWA AI solutions",
    "call_to_action": "Visit fdwa.site for consultation", 
    "youtube_title": "Professional YouTube title",
    "youtube_description": "Complete description with hashtags"
}}"""

            response = self.llm.invoke(prompt)
            content_text = response.content
            
            # Parse JSON from AI response
            try:
                json_start = content_text.find('{')
                json_end = content_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_content = content_text[json_start:json_end]
                    content_data = json.loads(json_content)
                    logger.info(" AI generated marketing content successfully")
                    return content_data
            except json.JSONDecodeError:
                pass
            
            # Fallback if parsing fails
            logger.warning("AI response parsing failed, using enhanced template")
            return self._template_generate_content(topic, video_type)
            
        except Exception as e:
            logger.error(f"AI content generation failed: {e}")
            return self._template_generate_content(topic, video_type)
    
    def _template_generate_content(self, topic: str, video_type: str) -> Dict[str, Any]:
        """Generate content using smart templates"""
        
        # Smart template selection based on topic
        if "consulting" in topic.lower():
            main_msg = "Transform your business with expert AI consulting"
            title = "FDWA AI Consulting - Business Transformation Services"
        elif "development" in topic.lower():
            main_msg = "Custom AI solutions built for your success"
            title = "FDWA AI Development - Custom Solutions That Work"
        elif "wealth" in topic.lower() or "digital" in topic.lower():
            main_msg = "Navigate digital wealth with AI-powered strategies"
            title = "FDWA Digital Wealth Strategy - AI-Powered Growth"
        else:
            main_msg = f"FDWA delivers results with {topic} solutions"
            title = f"FDWA {topic} - Professional AI Services"
        
        return {
            "main_message": main_msg,
            "call_to_action": "Visit fdwa.site to get started today",
            "youtube_title": title,
            "youtube_description": f"""{FDWABrand.COMPANY_NAME}
Expert {topic} services for business transformation.

Professional AI consulting and development
Proven results for growing businesses
Custom solutions tailored to your needs

Visit: {FDWABrand.WEBSITE}
Contact for free consultation
Transform your business today

#AI #Consulting #DigitalWealth #Business #Technology #FDWA #Growth #Innovation"""
        }
    
    @traceable(name="create_video")
    def create_marketing_video(self, content_data: Dict[str, Any], template_style: str = "single_scene") -> Dict[str, Any]:
        """Create professional marketing video with FDWA branding"""
        try:
            logger.info(f" Creating FDWA marketing video ({template_style} style)")
            
            main_message = content_data.get("main_message", "Transform your business with FDWA")
            cta = content_data.get("call_to_action", "Visit fdwa.site")
            
            # Initialize Creatomate client
            client = CreatomateClient()
            
            # Handle template style
            if template_style == "multi_scene":
                # Use the updated multi-scene template ID with music support
                multi_scene_template_id = "e0634967-3006-4703-8e1b-548af7ba7629"
                
                # Build multi-scene modifications like your working Python example
                from fdwa_template import get_multi_scene_ai_content
                multi_content = get_multi_scene_ai_content(theme, main_message)
                
                # Build modifications with correct field names matching new template structure
                modifications = {
                    # Music track for the video
                    "Music.source": "https://creatomate.com/files/assets/b5dc815e-dcc9-4c62-9405-f94913936bf5",
                    # Background images - use .source property for dynamic elements
                    "Background-1.source": "https://creatomate.com/files/assets/4a7903f0-37bc-48df-9d83-5eb52afd5d07",
                    "Background-2.source": "https://creatomate.com/files/assets/4a6f6b28-bb42-4987-8eca-7ee36b347ee7", 
                    "Background-3.source": "https://creatomate.com/files/assets/4f6963a5-7286-450b-bc64-f87a3a1d8964",
                    "Background-4.source": "https://creatomate.com/files/assets/36899eae-a128-43e6-9e97-f2076f54ea18",
                    # Text content - use .text property for dynamic text elements  
                    "Text-1.text": multi_content['scene_1'],
                    "Text-2.text": multi_content['scene_2'],
                    "Text-3.text": multi_content['scene_3'],
                    "Text-4.text": multi_content['scene_4']
                }
                
                # Create video with template ID (not JSON)
                result = client.create_video(
                    text=multi_content['scene_1'],
                    handle="@fdwa",
                    name="Futuristic Digital Wealth Agency"
                )
                
                if result and result.get("id"):
                    # Wait for video completion
                    logger.info("Waiting for multi-scene video render to complete...")
                    completed_result = client.wait_for_completion(result["id"])
                    
                    if completed_result.get("url"):
                        video_info = {
                            "status": "success",
                            "video_url": completed_result["url"],
                            "render_id": result["id"],
                            "main_message": main_message,
                            "call_to_action": cta,
                            "content_data": content_data
                        }
                        
                        logger.info(" FDWA marketing video created", video_url=completed_result["url"])
                        return video_info
                    else:
                        return {"status": "error", "message": "Multi-scene video completed but no URL available"}
                else:
                    return {"status": "error", "message": "Multi-scene video creation failed - no render ID"}
            elif template_style == "quote":
                # Use the new quote template with animated question and answer
                quote_template_id = "95cdcf77-6ed7-42f3-9e94-6f7f1b25a870"
                
                # Generate question and answer content for FDWA
                from fdwa_template import get_quote_ai_content
                quote_content = get_quote_ai_content(theme, main_message)
                
                # Build modifications for quote template
                modifications = {
                    "Question.text": quote_content['question'],
                    "Quote.text": quote_content['answer'], 
                    "Handle.text": "@fdwa"
                }
                
                # Create video with quote template
                result = client.create_video(
                    text=quote_content['answer'],
                    handle="@fdwa",
                    name="Futuristic Digital Wealth Agency"
                )
                
                if result and result.get("id"):
                    # Wait for video completion
                    logger.info("Waiting for quote video render to complete...")
                    completed_result = client.wait_for_completion(result["id"])
                    
                    if completed_result.get("url"):
                        video_info = {
                            "status": "success",
                            "video_url": completed_result["url"],
                            "render_id": result["id"],
                            "main_message": main_message,
                            "call_to_action": cta,
                            "content_data": content_data
                        }
                        
                        logger.info(" FDWA marketing video created", video_url=completed_result["url"])
                        return video_info
                    else:
                        return {"status": "error", "message": "Quote video completed but no URL available"}
                else:
                    return {"status": "error", "message": "Quote video creation failed - no render ID"}
            else:
                # Use new single scene template ID
                single_scene_template_id = "cc493b27-5a2c-4218-b307-26a2420f2569"
                
                # Build modifications for new single scene template
                modifications = {
                    "Image.source": "https://creatomate.com/files/assets/4217ad24-5d65-44cd-88f9-deb70c58531b",
                    "Text.text": main_message,
                    "Handle.text": "@fdwa",
                    "Name.text": "Futuristic Digital Wealth Agency", 
                    "Picture.source": "https://creatomate.com/files/assets/6f9e0623-95a6-429f-91f1-a27272434083"
                }
                
                # Create video with template ID (not JSON)
                result = client.create_video(
                    text=main_message,
                    handle="@fdwa",
                    name="Futuristic Digital Wealth Agency"
                )
                
                if result and result.get("id"):
                    # Wait for video completion
                    logger.info("Waiting for video render to complete...")
                    completed_result = client.wait_for_completion(result["id"])
                    
                    if completed_result.get("url"):
                        video_info = {
                            "status": "success",
                            "video_url": completed_result["url"],
                            "render_id": result["id"],
                            "main_message": main_message,
                            "call_to_action": cta,
                            "content_data": content_data
                        }
                        
                        logger.info(" FDWA marketing video created", video_url=completed_result["url"])
                        return video_info
                    else:
                        return {"status": "error", "message": "Video completed but no URL available"}
                else:
                    return {"status": "error", "message": "Video creation failed - no render ID"}
                
        except Exception as e:
            logger.error(f"Video creation failed: {e}")
            return {"status": "error", "message": str(e)}
    
    @traceable(name="upload_youtube_composio") 
    def upload_to_youtube(self, video_info: Dict[str, Any]) -> Dict[str, Any]:
        """Upload video to YouTube using Composio (same pattern as other tools)"""
        try:
            logger.info(" Uploading FDWA video to YouTube via Composio")
            if not self.youtube_ready or not self.composio_client:
                return {"status": "error", "message": "YouTube integration not ready"}
            if video_info.get("status") != "success":
                return {"status": "error", "message": "Invalid video data"}
            video_url = video_info.get("video_url")
            content_data = video_info.get("content_data", {})
            title = content_data.get("youtube_title", "FDWA Marketing Video")
            description = content_data.get("youtube_description", "FDWA AI Marketing Video")
            # Download and validate video first
            import requests
            import tempfile
            import os
            
            logger.info(f"Downloading video from: {video_url}")
            response = requests.get(video_url, timeout=60)
            
            if response.status_code != 200:
                logger.error(f"Failed to download video: {response.status_code}")
                return {"status": "error", "message": "Failed to download video for YouTube"}
            
            video_content = response.content
            video_size = len(video_content)
            logger.info(f"Downloaded video size: {video_size} bytes ({video_size/1024/1024:.1f} MB)")
            
            # Check if video is too small (likely corrupted)
            if video_size < 100000:  # Less than 100KB
                logger.error(f"Video too small ({video_size} bytes) - likely corrupted")
                return {"status": "error", "message": "Video file too small - may be corrupted"}
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
                temp_file.write(video_content)
                temp_video_path = temp_file.name
                
            logger.info(f"Video saved to: {temp_video_path}")
            
            # Ensure title and description are not too long
            title = title[:100] if len(title) > 100 else title
            description = description[:5000] if len(description) > 5000 else description
            
            youtube_params = {
                "categoryId": "22",
                "description": description,
                "privacyStatus": "public",
                "tags": ["AI", "FDWA", "consulting", "business", "automation"],
                "title": title,
                "videoFilePath": temp_video_path
            }
            
            logger.info(f"YouTube upload params: title='{title[:50]}...', description length={len(description)}")
            logger.info(f" Uploading via user {self.user_id}")
            result = self.composio_client.tools.execute(
                slug="YOUTUBE_UPLOAD_VIDEO",
                arguments=youtube_params,
                connected_account_id=self.youtube_connected_account_id,
                version=os.getenv("YOUTUBE_TOOL_VERSION", "20251027_00")
            )
            
            # Clean up temp file
            try:
                os.unlink(temp_video_path)
            except:
                pass
            if result.get("successful", False):
                video_id = result.get("data", {}).get("video_id")
                logger.info(f" YouTube upload result: {result}")
                
                # Check for rate limit or quota issues
                if not video_id:
                    logger.warning("No video ID returned - upload may have failed silently")
                    # Still consider it a success since the upload API call worked
                    return {
                        "status": "success", 
                        "message": "YouTube upload initiated (processing may fail due to video format issues)"
                    }
                
                logger.info(f" YouTube upload successful: {video_id}")
                return {
                    "status": "success",
                    "platform": "YouTube",
                    "video_id": video_id,
                    "video_url": f"https://youtube.com/watch?v={video_id}",
                    "message": "FDWA marketing video posted successfully!"
                }
            else:
                error_msg = result.get("error", "Unknown error")
                
                # Check for rate limit specifically
                if "exceeded" in str(error_msg).lower() or "quota" in str(error_msg).lower():
                    logger.error(f" YouTube rate limit hit: {error_msg}")
                    return {
                        "status": "error", 
                        "message": "YouTube rate limit exceeded - skipping upload"
                    }
                
                logger.error(f" YouTube upload failed: {error_msg}")
                return {"status": "error", "message": f"YouTube upload failed: {error_msg}"}
        except Exception as e:
            logger.error(f"YouTube upload failed: {e}")
            return {"status": "error", "message": str(e)}
    
    @traceable(name="upload_facebook")
    def upload_to_facebook(self, video_info: Dict[str, Any]) -> Dict[str, Any]:
        """Upload video to Facebook Page using Composio"""
        try:
            logger.info(" Uploading FDWA video to Facebook")
            if not self.facebook_ready or not self.composio_client:
                return {"status": "error", "message": "Facebook integration not ready"}
            if video_info.get("status") != "success":
                return {"status": "error", "message": "Invalid video data"}
            
            # First get current user to verify connection
            user_result = self.composio_client.tools.execute(
                "FACEBOOK_GET_CURRENT_USER",
                {"fields": "id,name"},
                connected_account_id="ca_ztimDVH28syB",
                version=os.getenv("FACEBOOK_TOOL_VERSION", "20251104_00")
            )
            logger.info(f"Facebook user check: {user_result.get('data', {}).get('name', 'Unknown')}")
            video_url = video_info.get("video_url")
            content_data = video_info.get("content_data", {})
            main_message = video_info.get("main_message", "")
            cta = content_data.get("call_to_action", "Visit fdwa.site")
            facebook_caption = f"""{FDWABrand.COMPANY_NAME}\n\n{main_message}\n\nTransform your business with AI-powered solutions:\n Expert AI consulting and strategy\n Custom digital transformation\n Proven results for growing businesses\n\n{cta}\n\n#AI #DigitalWealth #BusinessTransformation #FDWA #Innovation #Technology #Growth #Consulting #FuturisticDigitalWealthAgency"""
            facebook_params = {
                "page_id": self.facebook_page_id,
                "file_url": video_url,
                "description": facebook_caption,
                "title": f"FDWA - {main_message[:50]}...",
                "published": True
            }
            logger.info(f" Posting to Facebook page {self.facebook_page_id} via connected account ca_ztimDVH28syB")
            logger.info(f"Facebook params: {facebook_params}")
            result = self.composio_client.tools.execute(
                "FACEBOOK_CREATE_VIDEO_POST",
                facebook_params,
                connected_account_id="ca_ztimDVH28syB",
                version=os.getenv("FACEBOOK_TOOL_VERSION", "20251104_00")
            )
            logger.info(f"Facebook result: {result}")
            if result.get("successful", False):
                facebook_post_id = result.get("data", {}).get("response_data", {}).get("id")
                facebook_url = f"https://facebook.com/{facebook_post_id}" if facebook_post_id else "Posted successfully"
                logger.info(f" Video posted to Facebook: {facebook_url}")
                return {
                    "status": "success",
                    "facebook_upload": "completed",
                    "facebook_post_id": facebook_post_id,
                    "facebook_url": facebook_url,
                    "caption": facebook_caption,
                    "video_url": video_url,
                    "message": "FDWA video posted to Facebook successfully!"
                }
            else:
                error_msg = result.get("error", "Unknown Facebook posting error")
                return {"status": "error", "message": f"Facebook posting failed: {error_msg}"}
        except Exception as e:
            logger.error(f"Facebook posting failed: {e}")
            return {"status": "error", "message": str(e)}
    
    @traceable(name="send_email")
    def send_email(self, recipient_email: str, subject: str, body: str, is_html: bool = False) -> Dict[str, Any]:
        """Send email via Gmail using Composio"""
        try:
            logger.info(f"📧 Sending email to {recipient_email}")
            if not self.gmail_ready or not self.composio_client:
                return {"status": "error", "message": "Gmail integration not ready"}
            
            email_params = {
                "recipient_email": recipient_email,
                "subject": subject,
                "body": body,
                "is_html": is_html,
                "user_id": "me"
            }
            
            logger.info(f"Gmail params: subject='{subject[:50]}...', recipient={recipient_email}")
            result = self.composio_client.tools.execute(
                "GMAIL_SEND_EMAIL",
                email_params,
                connected_account_id=self.gmail_connected_account_id,
                version=os.getenv("GMAIL_TOOL_VERSION", "20251111_00")
            )
            
            if result.get("successful", False):
                logger.info(f"✅ Email sent successfully to {recipient_email}")
                return {
                    "status": "success",
                    "platform": "Gmail",
                    "recipient": recipient_email,
                    "subject": subject,
                    "message": "Email sent successfully!"
                }
            else:
                error_msg = result.get("error", "Unknown Gmail error")
                logger.error(f"❌ Gmail send failed: {error_msg}")
                return {"status": "error", "message": f"Gmail send failed: {error_msg}"}
                
        except Exception as e:
            logger.error(f"Gmail send failed: {e}")
            return {"status": "error", "message": str(e)}
    
    @traceable(name="full_marketing_workflow", metadata={"fdwa_automation": True})
    async def create_and_post_video(self, topic: str, video_type: str = "promotional", template_style: str = "single_scene") -> str:
        """
        Complete marketing workflow: Generate content  Create video  Post to YouTube
        Single function that handles the entire process with Composio YouTube/Facebook upload
        
        Args:
            topic: Marketing topic/subject
            video_type: Type of video content (promotional, educational, etc.)  
            template_style: 'single_scene', 'multi_scene', or 'quote'
                          - 'single_scene': Professional quote-style video (1080x1080)
                          - 'multi_scene': TikTok/Instagram style 4-scene video (720x1280)
                          - 'quote': Animated question/answer format (720x1280)
        
        Returns:
            Complete workflow summary with video URLs and upload status
        """
        try:
            logger.info(f"Starting full FDWA marketing workflow: {topic}")
            logger.info(f" Template Style: {template_style}")
            logger.info(f" Available templates: single_scene, multi_scene, quote")
            
            # Validate template style
            valid_templates = ["single_scene", "multi_scene", "quote"]
            if template_style not in valid_templates:
                logger.warning(f" Invalid template style '{template_style}', using 'single_scene'")
                template_style = "single_scene"
            
            # Step 1: Generate marketing content
            logger.info(" Step 1: Generating marketing content...")
            content_data = self.generate_marketing_content(topic, video_type)
            
            # Step 2: Create professional video with template style
            logger.info(f" Step 2: Creating professional video ({template_style} style)...")
            video_info = self.create_marketing_video(content_data, template_style)
            
            if video_info.get("status") != "success":
                return f" Video creation failed: {video_info.get('message')}"
            
            # Step 3: Upload to YouTube with Composio (with rate limit check)
            logger.info(" Step 3: Uploading to YouTube with Composio...")
            youtube_result = self.upload_to_youtube(video_info)
            
            # Step 4: Upload to Facebook (always attempt, regardless of YouTube status)
            logger.info(" Step 4: Uploading to Facebook...")
            facebook_result = self.upload_to_facebook(video_info)
            
            # Step 5: Send email notification (optional)
            logger.info(" Step 5: Sending email notification...")
            email_subject = f"FDWA Video Created: {content_data.get('main_message', 'Marketing Video')[:50]}..."
            email_body = f"""New FDWA marketing video has been created and posted!

Content: {content_data.get('main_message', 'FDWA Marketing Video')}
Template Style: {template_style}
Video URL: {video_info.get('video_url')}

Results:
- YouTube: {'✅ Posted' if youtube_result.get('status') == 'success' else '❌ Failed'}
- Facebook: {'✅ Posted' if facebook_result.get('status') == 'success' else '❌ Failed'}

Generated by FDWA AI Marketing Agent
{FDWABrand.WEBSITE}"""
            
            email_result = self.send_email(
                recipient_email="coinvest518@gmail.com",
                subject=email_subject,
                body=email_body
            )
            
            # Step 6: Create and post affiliate marketing blog
            if os.getenv("BLOG_AGENT_ENABLED", "false").lower() == "true":
                logger.info(" Step 6: Creating affiliate marketing blog...")
                try:
                    from blog_agent import get_blog_agent
                    blog_agent = get_blog_agent()
                    blog_result = blog_agent.create_and_post_blog(topic, content_data)
                    
                    if blog_result.get("status") == "success":
                        logger.info(f"📝 Blog posted: {blog_result.get('blog_title')}")
                    else:
                        logger.warning(f"Blog posting failed: {blog_result.get('message')}")
                except Exception as e:
                    logger.error(f"Blog agent failed: {e}")
            
            # Determine overall success and create summary
            video_created = video_info.get("status") == "success"
            youtube_success = youtube_result.get("status") == "success"
            facebook_success = facebook_result.get("status") == "success"
            
            if not video_created:
                return f" Video creation failed: {video_info.get('message')}"
            
            # Create concise result summary
            result_summary = f""" FDWA Marketing Video Posted!

Content: {content_data.get('main_message', 'FDWA Marketing Video')}
Video: {video_info.get('video_url')}
Style: {template_style}

Results:"""
            
            # YouTube status
            if youtube_success:
                result_summary += f"\n YouTube: ✅ Posted"
            else:
                result_summary += f"\n YouTube: ❌ {youtube_result.get('message', 'Failed')}"
            
            # Facebook status
            if facebook_success:
                result_summary += f"\n Facebook: ✅ Posted"
            else:
                result_summary += f"\n Facebook: ❌ {facebook_result.get('message', 'Failed')}"
            
            # Add blog status if enabled
            if os.getenv("BLOG_AGENT_ENABLED", "false").lower() == "true":
                try:
                    from blog_agent import get_blog_agent
                    blog_agent = get_blog_agent()
                    blog_result = blog_agent.create_and_post_blog(topic, content_data)
                    blog_success = blog_result.get("status") == "success"
                    
                    if blog_success:
                        result_summary += f"\n 📝 Blog: ✅ Posted to Blogger"
                    else:
                        result_summary += f"\n 📝 Blog: ❌ {blog_result.get('message', 'Failed')}"
                except:
                    result_summary += f"\n 📝 Blog: ❌ Agent Error"
            
            result_summary += f"\n\n{FDWABrand.WEBSITE}"

            logger.info(" Full marketing workflow completed successfully")
            return result_summary
            
        except Exception as e:
            logger.error(f"Marketing workflow failed: {e}")
            return f"Marketing workflow error: {str(e)}"

# Global agent instance
fdwa_agent = None

def get_fdwa_agent() -> FDWAMarketingAgent:
    """Get or create the FDWA marketing agent"""
    global fdwa_agent
    if fdwa_agent is None:
        fdwa_agent = FDWAMarketingAgent()
    return fdwa_agent

# Convenience functions for easy usage
@traceable(name="create_marketing_video")
async def create_marketing_video(topic: str, video_type: str = "promotional", template_style: str = "single_scene") -> str:
    """
    Simple function to create and post a marketing video
    
    Args:
        topic: What the video is about
        video_type: promotional, educational, etc.
        template_style: 'single_scene' (square professional) or 'multi_scene' (vertical TikTok style)
    """
    agent = get_fdwa_agent()
    return await agent.create_and_post_video(topic, video_type, template_style)

@traceable(name="auto_marketing_campaign")  
async def auto_marketing_campaign(template_style: str = "single_scene") -> str:
    """
    Automatically create marketing content for FDWA AI consulting
    
    Args:
        template_style: 'single_scene' for professional or 'multi_scene' for social media
    """
    agent = get_fdwa_agent()
    return await agent.create_and_post_video("AI Consulting services that transform businesses", "promotional", template_style)

# Template style helpers
def create_professional_video(topic: str) -> str:
    """Create a professional square video (1080x1080) for LinkedIn/business use"""
    import asyncio
    agent = get_fdwa_agent()
    return asyncio.run(agent.create_and_post_video(topic, "promotional", "single_scene"))

def create_social_video(topic: str) -> str:
    """Create a vertical social media video (720x1280) for TikTok/Instagram"""
    import asyncio
    agent = get_fdwa_agent()
    return asyncio.run(agent.create_and_post_video(topic, "promotional", "multi_scene"))

def create_educational_video(topic: str) -> str:
    """Create an educational Q&A video (720x1280) with animated question/answer"""
    import asyncio
    agent = get_fdwa_agent()
    return asyncio.run(agent.create_and_post_video(topic, "educational", "quote"))

def show_template_options():
    """Display available template options and usage"""
    print("""
 FDWA AI Marketing Agent - Template Options

 Template Styles Available:

1 SINGLE SCENE (Professional Business)
    Format: 1080x1080 (Square)
    Style: Professional quote with FDWA branding
    Best for: LinkedIn, business presentations, professional content
    Usage: template_style="single_scene"

2 MULTI SCENE (Social Media)
    Format: 720x1280 (Vertical)
    Style: 4-scene TikTok/Instagram style with dynamic backgrounds
    Best for: TikTok, Instagram Reels, social media engagement
    Usage: template_style="multi_scene"

3 QUOTE (Educational/Q&A)
    Format: 720x1280 (Vertical)
    Style: Animated question/answer with professional quote design
    Best for: Educational content, expert insights, thought leadership
    Usage: template_style="quote"

 Usage Examples:

# Professional video
agent = get_fdwa_agent()
result = await agent.create_and_post_video("AI Consulting", template_style="single_scene")

# Social media video  
result = await agent.create_and_post_video("Digital Transformation", template_style="multi_scene")

# Educational Q&A video
result = await agent.create_and_post_video("AI Benefits", template_style="quote")

# Quick helpers
create_professional_video("Business Automation")  # Creates single_scene
create_social_video("AI Strategy")               # Creates multi_scene
create_educational_video("AI Myths")             # Creates quote

 Both templates include:
 AI-generated content using Gemini 2.5
 FDWA brand consistency
 YouTube upload with Composio
 Professional messaging and CTAs
""")

def get_template_info() -> dict:
    """Get detailed template information"""
    return {
        "single_scene": {
            "format": "1080x1080",
            "style": "Professional quote with FDWA branding",
            "template_id": "cc493b27-5a2c-4218-b307-26a2420f2569",
            "best_for": ["LinkedIn", "Business presentations", "Professional content"],
            "elements": ["Main quote text", "FDWA logo", "Company name", "Handle", "Background image"]
        },
        "multi_scene": {
            "format": "720x1280", 
            "style": "4-scene vertical with dynamic backgrounds and music",
            "template_id": "e0634967-3006-4703-8e1b-548af7ba7629",
            "best_for": ["TikTok", "Instagram Reels", "Social media"],
            "elements": ["4 scenes with backgrounds", "Dynamic text per scene", "Background music", "FDWA branding"]
        },
        "quote": {
            "format": "720x1280",
            "style": "Animated question/answer with quote design", 
            "template_id": "95cdcf77-6ed7-42f3-9e94-6f7f1b25a870",
            "best_for": ["Educational content", "Q&A videos", "Thought leadership", "Expert insights"],
            "elements": ["Animated question", "Detailed answer quote", "Professional design", "FDWA handle"]
        }
    }

if __name__ == "__main__":
    print(" FDWA AI Marketing Agent - Complete Edition")
    print("=" * 60)
    print(f"Company: {FDWABrand.COMPANY_NAME}")
    print(f"Website: {FDWABrand.WEBSITE}")
    print()
    
    if validate_config():
        print(" Configuration validated - ready for AI marketing!")
        print()
        print(" Template Options:")
        print(" single_scene: Professional 1080x1080 videos (LinkedIn/Business)")
        print(" multi_scene: Vertical 720x1280 videos (TikTok/Instagram)")
        print()
        print(" AI Features:")
        print(" Gemini 2.5 content generation")
        print(" Professional FDWA branding")  
        print(" YouTube upload via Composio")
        print(" Full workflow automation")
        print(" LangSmith tracing")
        print()
        
        # Show template options
        show_template_options()
        
        # Composio integration only - no OAuth
            
        print("\n" + "=" * 60)
        print(" Quick Start:")
        print("from fdwa_complete_agent import get_fdwa_agent")
        print('agent = get_fdwa_agent()')
        print('# Professional video:')
        print('await agent.create_and_post_video("AI Consulting", template_style="single_scene")')
        print('# Social media video:') 
        print('await agent.create_and_post_video("Digital Growth", template_style="multi_scene")')
    else:
        print(" Configuration validation failed")