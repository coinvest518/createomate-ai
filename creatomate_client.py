"""
Creatomate API integration module
Handles all interactions with the Creatomate video generation API
"""
import asyncio
import aiohttp
import requests
from typing import Dict, Any, Optional, List
import structlog
from config import config

logger = structlog.get_logger()

class CreatomateClient:
    """Client for interacting with Creatomate API"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or config.api_key
        self.base_url = base_url or config.base_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def create_video_by_template(
        self, 
        template_id: str,
        modifications: Dict[str, Any],
        webhook_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a video using a template with modifications
        
        Args:
            template_id: The ID of the template to use
            modifications: Dictionary of modifications to apply to the template
            webhook_url: Optional webhook URL for notifications
            
        Returns:
            Response from Creatomate API containing render information
        """
        endpoint = f"{self.base_url}/renders"
        
        payload = {
            "template_id": template_id,
            "modifications": modifications
        }
        
        if webhook_url:
            payload["webhook_url"] = webhook_url
        
        try:
            logger.info("Creating video with template", 
                       template_id=template_id, 
                       modifications=modifications)
            
            response = requests.post(endpoint, json=payload, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            logger.info("Video creation initiated", render_id=result.get("id"))
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error("Failed to create video", error=str(e))
            raise
    
    def create_video_from_json(
        self, 
        template_json: Dict[str, Any],
        modifications: Dict[str, Any],
        webhook_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a video using template JSON directly with modifications
        
        Args:
            template_json: The template JSON structure
            modifications: Dictionary of modifications to apply
            webhook_url: Optional webhook URL for notifications
            
        Returns:
            Response from Creatomate API containing render information
        """
        endpoint = f"{self.base_url}/renders"
        
        payload = {
            "source": template_json,
            "modifications": modifications
        }
        
        if webhook_url:
            payload["webhook_url"] = webhook_url
        
        try:
            logger.info("Creating video with JSON template", 
                       modifications=modifications)
            
            response = requests.post(endpoint, json=payload, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            logger.info("Video creation initiated", render_id=result.get("id"))
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error("Failed to create video", error=str(e))
            raise
    
    async def create_video_async(
        self, 
        template_id: str,
        modifications: Dict[str, Any],
        webhook_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Async version of create_video_by_template
        """
        endpoint = f"{self.base_url}/renders"
        
        payload = {
            "template_id": template_id,
            "modifications": modifications
        }
        
        if webhook_url:
            payload["webhook_url"] = webhook_url
        
        async with aiohttp.ClientSession() as session:
            try:
                logger.info("Creating video with template (async)", 
                           template_id=template_id, 
                           modifications=modifications)
                
                async with session.post(endpoint, json=payload, headers=self.headers) as response:
                    response.raise_for_status()
                    result = await response.json()
                    
                    logger.info("Video creation initiated (async)", render_id=result.get("id"))
                    return result
                    
            except aiohttp.ClientError as e:
                logger.error("Failed to create video (async)", error=str(e))
                raise
    
    def get_render_status(self, render_id: str) -> Dict[str, Any]:
        """
        Get the status of a render job
        
        Args:
            render_id: The ID of the render to check
            
        Returns:
            Render status information
        """
        endpoint = f"{self.base_url}/renders/{render_id}"
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error("Failed to get render status", render_id=render_id, error=str(e))
            raise
    
    def wait_for_completion(self, render_id: str, timeout: int = 300) -> Dict[str, Any]:
        """
        Wait for a render to complete with polling
        
        Args:
            render_id: The ID of the render to wait for
            timeout: Maximum time to wait in seconds
            
        Returns:
            Final render status
        """
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.get_render_status(render_id)
            
            if status.get("status") == "succeeded":
                logger.info("Render completed successfully", 
                           render_id=render_id, 
                           url=status.get("url"))
                return status
            elif status.get("status") == "failed":
                logger.error("Render failed", 
                            render_id=render_id, 
                            error=status.get("error_message"))
                raise Exception(f"Render failed: {status.get('error_message')}")
            
            time.sleep(5)  # Poll every 5 seconds
        
        raise TimeoutError(f"Render {render_id} did not complete within {timeout} seconds")

class TemplateModificationBuilder:
    """Helper class to build template modifications"""
    
    def __init__(self):
        self.modifications = {}
    
    def set_text(self, element_name: str, text: str) -> 'TemplateModificationBuilder':
        """Set text content for a text element"""
        self.modifications[element_name] = text
        return self
    
    def set_text_property(self, element_name: str, property_name: str, value: Any) -> 'TemplateModificationBuilder':
        """Set a specific property of a text element"""
        self.modifications[f"{element_name}.{property_name}"] = value
        return self
    
    def set_media(self, element_name: str, url: str) -> 'TemplateModificationBuilder':
        """Set media source for an image/video element"""
        self.modifications[element_name] = url
        return self
    
    def set_color(self, element_name: str, color: str) -> 'TemplateModificationBuilder':
        """Set fill color for an element"""
        self.modifications[f"{element_name}.fill_color"] = color
        return self
    
    def set_font_family(self, element_name: str, font: str) -> 'TemplateModificationBuilder':
        """Set font family for a text element"""
        self.modifications[f"{element_name}.font_family"] = font
        return self
    
    def set_timing(self, element_name: str, start_time: float, duration: Optional[float] = None) -> 'TemplateModificationBuilder':
        """Set timing for an element"""
        self.modifications[f"{element_name}.time"] = start_time
        if duration is not None:
            self.modifications[f"{element_name}.duration"] = duration
        return self
    
    def remove_element(self, element_name: str) -> 'TemplateModificationBuilder':
        """Remove an element from the template"""
        self.modifications[element_name] = {}
        return self
    
    def set_template_dimensions(self, width: int, height: int) -> 'TemplateModificationBuilder':
        """Set template dimensions"""
        self.modifications["width"] = width
        self.modifications["height"] = height
        return self
    
    def build(self) -> Dict[str, Any]:
        """Build and return the modifications dictionary"""
        return self.modifications.copy()

class SocialVideoTemplateBuilder:
    """
    Specialized builder for the social video template with dynamic elements:
    - Text: Main quote text (dynamic)
    - Handle: Social media handle (dynamic) 
    - Name: Brand/profile name (dynamic)
    - Picture: Profile picture (dynamic)
    - Image: Background image (dynamic)
    """
    
    def __init__(self):
        self.modifications = {}
    
    def set_quote_text(self, text: str) -> 'SocialVideoTemplateBuilder':
        """Set the main quote text"""
        self.modifications["Text"] = text
        return self
    
    def set_social_handle(self, handle: str) -> 'SocialVideoTemplateBuilder':
        """Set the social media handle (e.g., @username)"""
        if not handle.startswith("@"):
            handle = f"@{handle}"
        self.modifications["Handle"] = handle
        return self
    
    def set_profile_name(self, name: str) -> 'SocialVideoTemplateBuilder':
        """Set the profile/brand name"""
        self.modifications["Name"] = name
        return self
    
    def set_profile_picture(self, image_url: str) -> 'SocialVideoTemplateBuilder':
        """Set the profile picture URL"""
        self.modifications["Picture"] = image_url
        return self
    
    def set_background_image(self, image_url: str) -> 'SocialVideoTemplateBuilder':
        """Set the background image URL"""
        self.modifications["Image"] = image_url
        return self
    
    def set_text_color(self, color: str) -> 'SocialVideoTemplateBuilder':
        """Set the color of the main text"""
        self.modifications["Text.fill_color"] = color
        return self
    
    def set_text_font_size(self, size: str) -> 'SocialVideoTemplateBuilder':
        """Set the font size of the main text (e.g., '5 vmin')"""
        self.modifications["Text.font_size"] = size
        return self
    
    def set_template_dimensions(self, width: int = 720, height: int = 1280) -> 'SocialVideoTemplateBuilder':
        """Set template dimensions (default is vertical 720x1280 for social media)"""
        self.modifications["width"] = width
        self.modifications["height"] = height
        return self
    
    def build(self) -> Dict[str, Any]:
        """Build and return the modifications dictionary"""
        return self.modifications.copy()

# Default client instance
creatomate_client = CreatomateClient()