#!/usr/bin/env python3
"""Test runner for `subagents.youtube_subagent`.

This script is safe to run in two modes:
- Dry-run (default): does remote probe and local probe/download + re-encode checks, but does NOT call Composio.
- Live: when `COMPOSIO_API_KEY` and `YOUTUBE_CONNECTED_ACCOUNT_ID` are set, it will call the subagent's
  `upload_rendered_video_to_youtube` and attempt an upload.

Usage:
  - Set `TEST_RENDER_URL` to point to a Creatomate/Backblaze render URL.
  - Optionally set `COMPOSIO_API_KEY` and `YOUTUBE_CONNECTED_ACCOUNT_ID` to perform a real upload.

Examples:
  # Dry run (no API keys set)
  python test_youtube_subagent.py

  # Live run (will upload if API keys present)
  COMPOSIO_API_KEY=... YOUTUBE_CONNECTED_ACCOUNT_ID=... python test_youtube_subagent.py
"""

import os
import tempfile
import requests
from dotenv import load_dotenv
from utils.video_utils import probe_codecs, reencode_to_h264_aac
from subagents.youtube_subagent import upload_rendered_video_to_youtube
import structlog

logger = structlog.get_logger(__name__)


def stream_download_to_temp(url: str) -> str:
    """Stream-download a URL to a temporary file and return its path."""
    r = requests.get(url, stream=True, timeout=60)
    r.raise_for_status()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tf:
        for chunk in r.iter_content(chunk_size=64 * 1024):
            if chunk:
                tf.write(chunk)
        return tf.name


def main():
    load_dotenv()

    render_url = os.getenv("TEST_RENDER_URL") or (
        "https://f002.backblazeb2.com/file/creatomate-c8xg3hsxdu/5b1ff05f-4f99-4217-96d1-98e47fe60423.mp4"
    )

    composio_key = os.getenv("COMPOSIO_API_KEY")
    connected_account = os.getenv("YOUTUBE_CONNECTED_ACCOUNT_ID")

    print(f"Render URL: {render_url}")

    # Try remote probe first (ffprobe can often inspect URLs)
    try:
        remote_info = probe_codecs(render_url)
        if remote_info:
            streams = remote_info.get("streams", [])
            vcodec = next((s.get("codec_name") for s in streams if s.get("codec_type") == "video"), None)
            acodec = next((s.get("codec_name") for s in streams if s.get("codec_type") == "audio"), None)
            print(f"Remote probe: video={vcodec}, audio={acodec}")
        else:
            print("Remote probe returned no info (ffprobe may not support remote inspect).")
    except Exception as e:
        print(f"Remote probe failed: {e}")

    # If credentials are present, perform a real upload via subagent
    if composio_key and connected_account:
        print("COMPOSIO keys present — performing real upload via subagent (be careful!)")
        resp = upload_rendered_video_to_youtube(
            render_url=render_url,
            title="FDWA Subagent Test Upload",
            description="Test upload via youtube_subagent.py",
            tags=["fdwa", "test"],
            categoryId="22",
            connected_account_id=connected_account,
            reencode_before_upload=True,
            allow_remote_fetch=True,
        )
        print("Composio response:")
        print(resp)
        return

    # Dry-run: download and probe locally, then optionally re-encode
    print("No COMPOSIO keys — running dry-run locally (download -> probe -> maybe re-encode)")
    local_path = None
    try:
        local_path = stream_download_to_temp(render_url)
        print(f"Downloaded to: {local_path}")

        info = probe_codecs(local_path)
        streams = info.get("streams", []) if info else []
        vcodec = next((s.get("codec_name") for s in streams if s.get("codec_type") == "video"), None)
        acodec = next((s.get("codec_name") for s in streams if s.get("codec_type") == "audio"), None)
        print(f"Local probe: video={vcodec}, audio={acodec}")

        need_reencode = False
        if vcodec and vcodec.lower() not in ("h264", "avc1"):
            need_reencode = True
        if acodec and acodec.lower() not in ("aac",):
            need_reencode = True

        if need_reencode:
            print("Re-encoding locally to h264+aac...")
            reencoded = reencode_to_h264_aac(local_path)
            if reencoded:
                print(f"Re-encoded file: {reencoded}")
                os.unlink(local_path)
                local_path = reencoded
            else:
                print("Re-encode failed or ffmpeg not available.")
        else:
            print("No re-encode needed — codecs look compatible.")

        print("Dry-run complete — would now call Composio with the file above if keys were provided.")

    finally:
        try:
            if local_path and os.path.exists(local_path):
                os.unlink(local_path)
        except Exception:
            pass


if __name__ == "__main__":
    main()
