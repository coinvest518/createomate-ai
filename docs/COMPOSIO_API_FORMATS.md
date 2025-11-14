# Composio API Parameter Formats

## YouTube Upload Video (YOUTUBE_UPLOAD_VIDEO)


Now I see - it's tools.execute():

Perfect! It's slug not action, and arguments not params:



**Required Parameters:**
```json
{
  "categoryId": "22",
  "description": "Video description text",
  "privacyStatus": "public",
  "tags": ["tag1", "tag2", "tag3"],
  "title": "Video title",
  "videoFilePath": "https://video-url.mp4"
}
```

**API Call Format:**
```python
url = "https://backend.composio.dev/api/v3/tools/execute/YOUTUBE_UPLOAD_VIDEO"
payload = {
    "connected_account_id": "ca_XTs3Hgh8E_k7",
    "arguments": {
        "categoryId": "22",
        "description": description,
        "privacyStatus": "public", 
        "tags": ["AI", "FDWA", "consulting"],
        "title": title,
        "videoFilePath": video_url
    }
}
```

## Facebook Create Video Post (FACEBOOK_CREATE_VIDEO_POST)

**Required Parameters:**
```json
{
  "page_id": "5183998",
  "file_url": "https://video-url.mp4",
  "description": "Post description",
  "title": "Post title",
  "published": true
}
```

**API Call Format:**
```python
url = "https://backend.composio.dev/api/v3/tools/execute/FACEBOOK_CREATE_VIDEO_POST"
payload = {
    "connected_account_id": "ca_ztimDVH28syB",
    "arguments": {
        "page_id": "5183998",
        "file_url": video_url,
        "description": description,
        "title": title,
        "published": True
    }
}
```

## Common API Structure

**Headers:**
```python
headers = {
    "x-api-key": "ak_DwpxD6774KW52z0qVb-m",
    "Content-Type": "application/json"
}
```

**Response Format:**
```json
{
  "data": {},
  "error": "string or null",
  "successful": boolean
}
```

## Key Differences from Previous Attempts:

1. **YouTube:** Use `videoFilePath` NOT `file_url`
2. **YouTube:** Use `privacyStatus` NOT `privacy_status` 
3. **YouTube:** `categoryId` is REQUIRED (use "22" for People & Blogs)
4. **Facebook:** Use `file_url` NOT `videoFilePath`
5. **Both:** Use `connected_account_id` in payload, NOT `user_id`
6. **Response:** Check `successful` field, NOT `success`