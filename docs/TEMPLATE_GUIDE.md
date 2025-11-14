# FDWA AI Marketing Agent - Template Guide

## 🎬 Available Template Options

The FDWA AI Marketing Agent now supports **two distinct template styles** for different marketing needs:

### 1️⃣ Single Scene Template (Professional Business)
- **Format**: 1080x1080 (Square)
- **Style**: Professional quote with FDWA branding and background image
- **Best For**: LinkedIn, business presentations, professional content
- **Elements**: Main quote text, FDWA logo, company name, handle, background image
- **Template ID**: `cc493b27-5a2c-4218-b307-26a2420f2569`

### 2️⃣ Multi Scene Template (Social Media)
- **Format**: 720x1280 (Vertical)
- **Style**: 4-scene TikTok/Instagram style with dynamic backgrounds and music
- **Best For**: TikTok, Instagram Reels, social media engagement
- **Elements**: 4 scenes with backgrounds, dynamic text per scene, background music, FDWA branding
- **Template ID**: `e0634967-3006-4703-8e1b-548af7ba7629`

### 3️⃣ Quote Template (Educational/Q&A)
- **Format**: 720x1280 (Vertical)
- **Style**: Animated question/answer with professional quote design
- **Best For**: Educational content, expert insights, thought leadership, Q&A videos
- **Elements**: Animated question text, detailed answer quote, professional design, FDWA handle
- **Template ID**: `95cdcf77-6ed7-42f3-9e94-6f7f1b25a870`

## 🚀 Usage Examples

### Basic Usage
```python
from fdwa_complete_agent import get_fdwa_agent

# Get the AI agent
agent = get_fdwa_agent()

# Create professional video (square format)
result = await agent.create_and_post_video(
    topic="AI Consulting Services", 
    template_style="single_scene"
)

# Create social media video (vertical format)
result = await agent.create_and_post_video(
    topic="Digital Transformation", 
    template_style="multi_scene"
)

# Create educational Q&A video (vertical format)
result = await agent.create_and_post_video(
    topic="AI Benefits for Business", 
    template_style="quote"
)
```

### Quick Helpers
```python
from fdwa_complete_agent import create_professional_video, create_social_video, create_educational_video

# One-line professional video
create_professional_video("Business Automation")

# One-line social media video
create_social_video("AI Strategy")

# One-line educational video
create_educational_video("AI Myths Debunked")
```

### Check Available Options
```python
from fdwa_complete_agent import show_template_options, get_template_info

# Display all template options with usage examples
show_template_options()

# Get detailed template information
template_info = get_template_info()
print(template_info)
```

## 🤖 AI Features (Both Templates)

✅ **Gemini 2.5 AI Content Generation**
- Professional marketing messages
- Brand-consistent tone and style
- Topic-specific content variations

✅ **FDWA Brand Consistency**
- Company colors (#0066FF, #00FFAA, #FFFFFF)
- Professional messaging
- Consistent logo and branding

✅ **YouTube Integration**
- OAuth authentication
- Automatic upload after creation
- SEO-optimized titles and descriptions

✅ **Complete Workflow Automation**
- Generate content → Create video → Upload → Report
- Full traceability with LangSmith
- Error handling and fallbacks

## 📱 When to Use Each Template

### Use Single Scene When:
- Creating content for LinkedIn
- Business presentations
- Professional demonstrations
- Corporate communications
- B2B marketing

### Use Multi Scene When:
- TikTok content creation
- Instagram Reels
- Social media engagement
- B2C marketing
- Viral content attempts

### Use Quote When:
- Educational content creation
- Answering common questions
- Thought leadership positioning
- Expert insights sharing
- FAQ videos
- Myth-busting content

## 🎯 Complete Workflow

Both template styles follow the same complete workflow:

1. **AI Content Generation**: Uses Gemini 2.5 to create compelling marketing messages
2. **Professional Video Creation**: Applies FDWA branding and creates MP4 video
3. **YouTube Upload**: Automatically uploads with OAuth and optimized metadata
4. **Result Reporting**: Provides URLs, status, and performance metrics

## 💡 Demo and Testing

Run the demo to see both templates in action:

```bash
python demo_both_templates.py
```

This will create both a professional and social media video with the same topic, showing the differences between template styles.

## 🔧 Configuration

Make sure you have:
- ✅ Creatomate API key configured
- ✅ Google/Gemini API key configured  
- ✅ YouTube OAuth credentials set up
- ✅ All dependencies installed

## 📈 Results

The agent creates:
- **High-quality MP4 videos** (both formats)
- **Professional FDWA branding** (consistent across templates)
- **AI-generated content** (tailored to your topic)
- **YouTube uploads** (automatic with metadata)
- **Complete reporting** (URLs, status, metrics)

Both template styles maintain FDWA's professional brand while adapting to different platform requirements and audience expectations.