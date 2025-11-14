"""
Creatomate API integration module
Handles all interactions with the Creatomate video generation API
"""
import requests
from typing import Dict, Any, Optional
import structlog
from config import config

logger = structlog.get_logger()

class CreatomateClient:
    """Client for interacting with Creatomate API"""
    
    def __init__(self, api_key: Optional[str] = None):
        # Use new API key and template ID
        self.api_key = "3361417c09d14983ac1116769b28491eae8342072897a144656fbfa8c3d3f0c76581a79b453d5fc1bfe10c476c9211f0"
        self.base_url = "https://api.creatomate.com/v2"
        self.template_id = "1718b538-daff-478d-ac9c-0235dca6680e"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def create_video(self, text: str, handle: str = "@elisabethparker", name: str = "Elisabeth Parker") -> Dict[str, Any]:
        """
        Create a video using the single template with modifications
        
        Args:
            text: The main text content for the video
            handle: Social media handle (default: @elisabethparker)
            name: Name to display (default: Elisabeth Parker)
            
        Returns:
            Response from Creatomate API containing render information
        """
        url = f"{self.base_url}/renders"
        
        data = {
            "template_id": self.template_id,
            "modifications": {
                "Image.source": "https://creatomate.com/files/assets/4217ad24-5d65-44cd-88f9-deb70c58531b",
                "Text.text": text,
                "Handle.text": handle,
                "Name.text": name,
                "Picture.source": "https://creatomate.com/files/assets/d6628425-8e35-4fee-9de8-a18d21309546"
            }
        }
        
        try:
            logger.info("Creating video with template", 
                       template_id=self.template_id, 
                       text=text)
            
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            logger.info("Video creation initiated", render_id=result.get("id"))
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error("Failed to create video", error=str(e))
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

# Simple helper function for creating videos
def create_quote_video(text: str, handle: str = "@elisabethparker", name: str = "Elisabeth Parker") -> Dict[str, Any]:
    """Simple function to create a quote video"""
    client = CreatomateClient()
    return client.create_video(text, handle, name)

# Test the new simplified API
if __name__ == "__main__":
    client = CreatomateClient()
    test_text = "It is unwise to be too sure of one's own wisdom. It is healthy to be reminded that the strongest might weaken and the wisest might err."
    
    try:
        result = client.create_video(test_text)
        print(f"Video creation successful: {result}")
    except Exception as e:
        print(f"Error: {e}")