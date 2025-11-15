# YouTube Processing Abandoned — Troubleshooting & Fixes

This document explains why YouTube may report "Processing abandoned" after a successful upload and how to fix it within this project.

## Common causes
- Incompatible video codec (e.g., H.265/HEVC, AV1, VP9 in some containers)
- Unsupported audio codec (e.g., ipcm, PCM). YouTube requires AC3/AAC or other common audio codecs; AAC is recommended.
- Corrupted/truncated file (small file size or incomplete upload)
- Mismatched container metadata
- YouTube-side temporary processing issues

## What we changed in the codebase
- We added an automatic probe using `ffprobe` to inspect downloaded video codecs.
- If the video uses non-standard codecs (video not `h264` or audio not `aac`), the agent will try to re-encode the video to H.264 (libx264) + AAC using `ffmpeg` before uploading.
- This behavior can be disabled using environment variable `REENCODE_BEFORE_UPLOAD=false` if you prefer not to re-encode.

## Requirements
- `ffmpeg` and `ffprobe` installed and available on your PATH

Windows install via Chocolatey (recommended):
```powershell
choco install ffmpeg -y
```

Or download a static build from https://ffmpeg.org and add it to your PATH.

## Useful Commands
- Inspect codecs with ffprobe:
```powershell
ffprobe -v error -print_format json -show_streams -show_format "C:\path\to\file.mp4" | jq
```
- Re-encode to H.264 + AAC with ffmpeg:
```powershell
ffmpeg -y -i input.mp4 -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 128k output.mp4
```

## Local testing steps
1. Run the built-in test script (it uploads via Composio):
```powershell
python test_youtube_upload.py
```
2. If a "Processing abandoned" error appears in YouTube after upload, re-run the test with `REENCODE_BEFORE_UPLOAD=true` (default), or set `FFMPEG` to be installed.

## Notes
- Re-encoding will increase the CPU time and can take some time depending on length and complexity.
- If the original file is large, you may want a different preset or bitrate for performance.
- If the uploaded file still fails, verify the exact codecs used, try re-encoding with different parameters, and consult YouTube support or the debug logs for more details.
 - The updated agent will now probe a remote `video_url` using `ffprobe` before allowing Composio to fetch it server-side. If remote `video_url` codecs are not H.264 + AAC, the agent will fallback to downloading the file and re-encoding locally before upload. This prevents many "Processing abandoned" errors.

---
Thanks for using FDWA automation — this code tries to handle most common reasons for YouTube processing failures by re-encoding automatically before upload. If you see specific codec errors in the logs, please paste them and I’ll help tailor the encoding settings.