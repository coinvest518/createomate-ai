#!/usr/bin/env python3
"""
Test YouTube Upload Only
"""
import os
import requests
import tempfile
from dotenv import load_dotenv
from composio import Composio
from utils.video_utils import probe_codecs, reencode_to_h264_aac

# Load environment variables
load_dotenv()

def test_youtube_upload():
    """Test YouTube upload with a sample video"""
    
    print("🎬 Testing YouTube Upload...")
    
    # Initialize Composio client
    composio_client = Composio(api_key=os.getenv("COMPOSIO_API_KEY"))
    youtube_connected_account_id = os.getenv("YOUTUBE_CONNECTED_ACCOUNT_ID")
    
    print(f"YouTube Connected Account ID: {youtube_connected_account_id}")
    
    # Use the video from your logs
    video_url = "https://f002.backblazeb2.com/file/creatomate-c8xg3hsxdu/5b1ff05f-4f99-4217-96d1-98e47fe60423.mp4"
    
    try:
        # Download video
        print(f"📥 Downloading video from: {video_url}")
        response = requests.get(video_url, timeout=60)
        
        if response.status_code != 200:
            print(f"❌ Failed to download video: {response.status_code}")
            return False
        
        video_content = response.content
        video_size = len(video_content)
        print(f"✅ Downloaded video size: {video_size} bytes ({video_size/1024/1024:.1f} MB)")
        
        # Save to temp file (simple approach that was working)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
            temp_file.write(video_content)
            temp_video_path = temp_file.name
        
        print(f"💾 Video saved to: {temp_video_path}")

        # Probe codecs and optionally re-encode
        codec_info = probe_codecs(temp_video_path)
        if codec_info:
            streams = codec_info.get("streams", [])
            video_codec = next((s.get("codec_name") for s in streams if s.get("codec_type") == "video"), None)
            audio_codec = next((s.get("codec_name") for s in streams if s.get("codec_type") == "audio"), None)
            print(f"🔍 Codec probe: video={video_codec}, audio={audio_codec}")

            should_reencode = False
            if video_codec and video_codec.lower() not in ("h264", "avc1"):
                should_reencode = True
            if audio_codec and audio_codec.lower() not in ("aac",):
                should_reencode = True

            if os.getenv("REENCODE_BEFORE_UPLOAD", "true").lower() not in ("false", "0") and should_reencode:
                print("🔁 Re-encoding video to H.264 + AAC to improve YouTube compatibility...")
                reencoded = reencode_to_h264_aac(temp_video_path)
                if reencoded:
                    # remove original file
                    try:
                        os.unlink(temp_video_path)
                    except:
                        pass
                    temp_video_path = reencoded
                    print(f"✅ Re-encoded video: {temp_video_path}")
        
        # YouTube upload parameters (simple, working approach)
        youtube_params = {
            "categoryId": "22",
            "description": "Test video upload from FDWA AI Marketing Agent",
            "privacyStatus": "public",
            "tags": ["AI", "FDWA", "test"],
            "title": "FDWA Test Video Upload",
            "videoFilePath": temp_video_path
        }
        
        print(f"📤 Uploading to YouTube...")
        print(f"Parameters: {youtube_params}")
        
        result = composio_client.tools.execute(
            slug="YOUTUBE_UPLOAD_VIDEO",
            arguments=youtube_params,
            connected_account_id=youtube_connected_account_id,
            version=os.getenv("YOUTUBE_TOOL_VERSION", "20251027_00")
        )
        
        print(f"📊 YouTube Result: {result}")
        
        # Clean up temp file
        try:
            os.unlink(temp_video_path)
        except:
            pass
        
        if result.get("successful", False):
            # Check where the video ID actually is
            data = result.get("data", {})
            response_data = data.get("response_data", {})
            video_id = response_data.get("id")  # This is where it actually is!
            
            print(f"✅ YouTube upload successful!")
            print(f"Video ID: {video_id}")
            print(f"Video URL: https://youtube.com/watch?v={video_id}")
            
            return True
        else:
            error_msg = result.get("error", "Unknown error")
            print(f"❌ YouTube upload failed: {error_msg}")
            return False
            
    except Exception as e:
        print(f"❌ YouTube test ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_youtube_upload()
    if success:
        print("\n🎉 YouTube upload working!")
    else:
        print("\n💥 YouTube upload needs fixing")