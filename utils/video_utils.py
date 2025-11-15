import subprocess
import shutil
import json
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)


def probe_codecs(path: str) -> Dict:
    """Return codec info using ffprobe (best effort)."""
    if not shutil.which("ffprobe"):
        logger.info("ffprobe not found on PATH - skipping codec probe")
        return {}

    try:
        command = [
            "ffprobe",
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            path,
        ]
        p = subprocess.run(command, capture_output=True, text=True, check=True)
        return json.loads(p.stdout)
    except Exception as e:
        logger.warning(f"ffprobe failed: {e}")
        return {}


def reencode_to_h264_aac(in_path: str, out_path: Optional[str] = None) -> Optional[str]:
    """Re-encode the file to H.264 + AAC using ffmpeg if available.

    Returns path to re-encoded file or None on error.
    """
    if not shutil.which("ffmpeg"):
        logger.info("ffmpeg not found on PATH - cannot re-encode")
        return None

    if out_path is None:
        out_path = in_path + ".reencoded.mp4"

    try:
        logger.info("Re-encoding video to H.264 + AAC for upload compatibility")
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            in_path,
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "23",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            out_path,
        ]
        subprocess.run(cmd, check=True)
        return out_path
    except Exception as e:
        logger.error(f"FFmpeg re-encode failed: {e}")
        return None
