"""
FDWA Template Definition - Exact structure from your Creatomate template
This tells the AI exactly which fields to modify and how
"""

# Your actual single scene template ID  
FDWA_TEMPLATE_ID = "1718b538-daff-478d-ac9c-0235dca6680e"

# Exact template structure from your JSON
FDWA_TEMPLATE_STRUCTURE = {
    "template_id": FDWA_TEMPLATE_ID,
    "dynamic_elements": {
        # Main quote text - the big text in the middle
        "Text": {
            "id": "text-element", 
            "type": "text",
            "field_name": "Text.text",
            "current_value": "It is unwise to be too sure of one's own wisdom. It is healthy to be reminded that the strongest might weaken and the wisest might err.",
            "properties": {
                "text": "The main message content",
                "font_size": "4.7477 vmin",
                "font_weight": "600", 
                "fill_color": "rgba(255,255,255,1)",
                "line_height": "132%"
            },
            "purpose": "Main marketing message - this is what AI should change"
        },
        
        # Social media handle
        "Handle": {
            "id": "handle-element",
            "type": "text",
            "field_name": "Handle.text", 
            "current_value": "@fdwa",
            "properties": {
                "text": "@fdwa",
                "font_weight": "600",
                "fill_color": "rgba(255,255,255,1)"
            },
            "purpose": "Social media handle - keep as @fdwa"
        },
        
        # Company name
        "Name": {
            "id": "name-element",
            "type": "text",
            "field_name": "Name.text",
            "current_value": "Futuristic Digital Wealth Agency", 
            "properties": {
                "text": "Futuristic Digital Wealth Agency",
                "font_weight": "700",
                "fill_color": "rgba(255,255,255,1)"
            },
            "purpose": "Company name - keep as FDWA full name"
        },
        
        # Profile picture/logo
        "Picture": {
            "id": "picture-element",
            "type": "image",
            "field_name": "Picture.source",
            "current_value": "6f9e0623-95a6-429f-91f1-a27272434083",
            "properties": {
                "source": "6f9e0623-95a6-429f-91f1-a27272434083",
                "border_radius": "100 vmin"
            },
            "purpose": "FDWA logo - keep same image ID"
        },
        
        # Background image 
        "Image": {
            "id": "background-image-element",
            "type": "image",
            "field_name": "Image.source", 
            "current_value": "4217ad24-5d65-44cd-88f9-deb70c58531b",
            "properties": {
                "source": "4217ad24-5d65-44cd-88f9-deb70c58531b"
            },
            "purpose": "Background image - could be changed for different themes"
        }
    }
}

# AI Content Generation Rules
AI_CONTENT_RULES = {
    "Text": {
        "max_length": 120,
        "style": "Professional, compelling, action-oriented",
        "themes": {
            "ai_consulting": [
                "Transform your business with AI consulting excellence",
                "Smart AI solutions for competitive advantage",
                "Professional AI consulting that delivers results",
                "Unlock AI potential for business growth",
                "Expert AI guidance for modern enterprises"
            ],
            "digital_transformation": [
                "Modernize. Optimize. Succeed with FDWA",
                "Digital transformation made simple", 
                "Your digital future starts today",
                "Technology solutions that drive results",
                "Bridge vision and digital reality"
            ],
            "business_automation": [
                "Automate intelligently. Grow exponentially", 
                "Smart automation for business efficiency",
                "Streamline operations with FDWA expertise",
                "Transform workflows with automation",
                "Efficiency through intelligent automation"
            ]
        }
    },
    "Handle": {
        "fixed_value": "@fdwa",
        "never_change": True
    },
    "Name": {
        "fixed_value": "Futuristic Digital Wealth Agency",
        "never_change": True
    },
    "Picture": {
        "fixed_value": "6f9e0623-95a6-429f-91f1-a27272434083", 
        "never_change": True
    }
}

# FDWA Brand Colors 
FDWA_BRAND_COLORS = {
    "primary": "#0066FF",      # Blue
    "secondary": "#00FFAA",    # Green/Teal  
    "text": "#FFFFFF",          # White text
    "accent": "#FF3366"        # Red accent
}

def get_ai_modifications(theme: str = "ai_consulting") -> dict:
    """
    Generate AI modifications for the template based on theme
    Returns the exact modification format Creatomate expects
    """
    import random
    
    theme_messages = AI_CONTENT_RULES["Text"]["themes"].get(
        theme, AI_CONTENT_RULES["Text"]["themes"]["ai_consulting"]
    )
    
    return {
        "Image.source": "https://creatomate.com/files/assets/4217ad24-5d65-44cd-88f9-deb70c58531b",
        "Text.text": random.choice(theme_messages),
        "Handle.text": "@fdwa",
        "Name.text": "Futuristic Digital Wealth Agency",
        "Picture.source": "6f9e0623-95a6-429f-91f1-a27272434083"
    }

def get_available_themes() -> list:
    """Get list of available content themes"""
    return list(AI_CONTENT_RULES["Text"]["themes"].keys())

# Test function
if __name__ == "__main__":
    print("🎯 FDWA Template Structure Loaded")
    print(f"Template ID: {FDWA_TEMPLATE_ID}")
    print(f"Dynamic Elements: {len(FDWA_TEMPLATE_STRUCTURE['dynamic_elements'])}")
    print()
    
    print("Available Themes:")
    for theme in get_available_themes():
        print(f"  • {theme}")
    print()
    
    # Test AI modifications
    test_theme = "ai_consulting"
    mods = get_ai_modifications(test_theme)
    
    print(f"AI Modifications for '{test_theme}':")
    for key, value in mods.items():
        print(f"  {key}: {value}")

def get_multi_scene_ai_content(theme: str, main_message: str) -> dict:
    """Generate content for multi-scene template based on theme and main message"""
    
    content_map = {
        "ai_consulting": {
            "scene_1": f"{main_message} 🚀",
            "scene_2": "FDWA delivers custom AI strategies that increase efficiency by 40%! 💼", 
            "scene_3": "Our proven process: Assessment → Strategy → Implementation → Results 📈",
            "scene_4": "Ready to unlock AI's potential? Visit fdwa.site to get started today! ✨"
        },
        "digital_transformation": {
            "scene_1": f"{main_message} 🌐",
            "scene_2": "FDWA transforms operations with cutting-edge digital solutions! 💡",
            "scene_3": "Cloud migration, automation, and AI integration - we handle it all 🔧", 
            "scene_4": "Transform your business today! Contact FDWA at fdwa.site 🚀"
        }
    }
    
    return content_map.get(theme, {
        "scene_1": f"{main_message} 🎯",
        "scene_2": "FDWA delivers expert AI consulting that drives real results! 💪",
        "scene_3": "Custom solutions, proven methodologies, measurable outcomes 📊",
        "scene_4": "Start your AI journey with FDWA! Visit fdwa.site today 🌟"
    })

def get_quote_ai_content(theme: str, main_message: str) -> dict:
    """Generate question/answer content for quote template based on theme"""
    
    content_map = {
        "ai_consulting": {
            "question": "How can AI transform my business operations?",
            "answer": f"{main_message} FDWA's AI consulting identifies process bottlenecks, automates repetitive tasks, and implements intelligent solutions that increase efficiency by 40% while reducing operational costs. Our proven methodology ensures measurable ROI within 90 days."
        },
        "digital_transformation": {
            "question": "What does digital transformation really mean for my company?",
            "answer": f"{main_message} FDWA guides businesses through comprehensive digital modernization - from cloud migration and automation to AI integration. We don't just digitize existing processes; we reimagine workflows for the digital age, creating competitive advantages that drive sustainable growth."
        },
        "business_automation": {
            "question": "Can automation actually improve my team's productivity?",
            "answer": f"{main_message} FDWA's smart automation solutions eliminate manual, repetitive tasks while empowering your team to focus on high-value strategic work. Our clients typically see 60% time savings on routine operations, leading to increased job satisfaction and business performance."
        }
    }
    
    return content_map.get(theme, {
        "question": "Why should I choose FDWA for my digital transformation?",
        "answer": f"{main_message} FDWA combines deep AI expertise with practical business knowledge to deliver transformation that works. We're not just consultants - we're your strategic partners in building a future-ready, digitally empowered organization that thrives in the modern economy."
    })