# Creatomate AI Agent 🎬🤖

Automated AI-powered video creation and social media posting system for FDWA (Futuristic Digital Wealth Agency).

## Features ✨

- **AI Content Generation**: Uses Google Gemini 2.5 for intelligent marketing content
- **Multi-Template Support**: Professional, social media, and educational video formats
- **Automated Posting**: YouTube and Facebook integration via Composio
- **Brand Consistency**: FDWA branding across all videos
- **Hourly Automation**: Continuous content creation with smart variety tracking
- **Template Styles**:
  - `single_scene`: Professional 1080x1080 videos
  - `multi_scene`: Vertical 720x1280 TikTok/Instagram style
  - `quote`: Educational Q&A format

## Quick Start 🚀

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/coinvest518/createomate-ai.git
cd createomate-ai

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file with your API keys:

```env
# Creatomate API
CREATOMATE_API_KEY=your_creatomate_api_key
DEFAULT_TEMPLATE_ID=your_template_id

# Google Gemini AI
GOOGLE_AI_API_KEY=your_google_api_key

# Composio (for social media)
COMPOSIO_API_KEY=your_composio_api_key
YOUTUBE_CONNECTED_ACCOUNT_ID=your_youtube_account_id
FACEBOOK_CONNECTED_ACCOUNT_ID=your_facebook_account_id
FACEBOOK_PAGE_ID=your_facebook_page_id
```

### 3. Usage

```bash
# Test single video creation
python test_flow.py

# Test all template styles
python test_all_styles.py

# Start automated hourly marketing
python fdwa_auto_marketing.py

# Single trigger marketing
python trigger_marketing.py
```

## API Usage 📝

```python
from fdwa_complete_agent import get_fdwa_agent

# Get agent instance
agent = get_fdwa_agent()

# Create different video styles
await agent.create_and_post_video("AI Consulting", template_style="single_scene")
await agent.create_and_post_video("Digital Growth", template_style="multi_scene")
await agent.create_and_post_video("AI Benefits", template_style="quote")
```

## Project Structure 📁

```
createomate-ai/
├── .env                    # Environment variables (not in repo)
├── .gitignore             # Git ignore rules
├── requirements.txt       # Python dependencies
├── config.py             # Configuration management
├── creatomate_client.py  # Creatomate API client
├── fdwa_template.py      # Template definitions
├── fdwa_complete_agent.py # Main AI agent
├── fdwa_auto_marketing.py # Automated scheduler
├── trigger_marketing.py  # Single trigger script
├── test_flow.py          # Test single video
└── test_all_styles.py    # Test all templates
```

## Deployment 🚀

### Railway/Cloud Deployment

```bash
# For continuous automation
python fdwa_auto_marketing.py
```

### Environment Variables Required

- `CREATOMATE_API_KEY`: Your Creatomate API key
- `GOOGLE_AI_API_KEY`: Google Gemini API key
- `COMPOSIO_API_KEY`: Composio API key for social media
- `YOUTUBE_CONNECTED_ACCOUNT_ID`: YouTube account ID
- `FACEBOOK_CONNECTED_ACCOUNT_ID`: Facebook account ID
- `FACEBOOK_PAGE_ID`: Facebook page ID

## Features in Detail 🔧

### Automated Marketing System
- Creates 24 unique videos per day
- Smart topic rotation (32 business themes)
- Template variety (professional, social, educational)
- Multi-platform posting (YouTube + Facebook)

### AI Content Generation
- Google Gemini 2.5 integration
- Professional marketing copy
- SEO-optimized titles and descriptions
- Brand-consistent messaging

### Template System
- **Single Scene**: Professional business videos (1080x1080)
- **Multi Scene**: TikTok/Instagram style (720x1280)
- **Quote**: Educational Q&A format (720x1280)

## License 📄

This project is for educational and development purposes. Ensure compliance with all API terms of service.

## Support 🆘

1. Check configuration: `python fdwa_complete_agent.py`
2. Test single video: `python test_flow.py`
3. Verify environment variables in `.env`
4. Check API key validity and quotas

---

**Transform your business with AI-powered video marketing! 🎬✨**