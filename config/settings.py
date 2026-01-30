"""
Configuration settings for the Agentic AI Blog System
Supports multiple AI providers: Gemini, Groq, DeepSeek, TogetherAI
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
POSTS_DIR = DATA_DIR / "posts"
IMAGES_DIR = DATA_DIR / "images"
BLOG_DIR = BASE_DIR / "blog"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
POSTS_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)

# ============================================
# API Keys
# ============================================
# Primary AI APIs
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "")

# Image & Media APIs
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY", "")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")

# ============================================
# AI Model Selection
# ============================================
# Options: gemini, groq, deepseek, together
PRIMARY_AI_MODEL = os.getenv("PRIMARY_AI_MODEL", "gemini")
FALLBACK_AI_MODEL = os.getenv("FALLBACK_AI_MODEL", "groq")

# Image source: pexels, stability
IMAGE_SOURCE = os.getenv("IMAGE_SOURCE", "pexels")

# ============================================
# Model Configurations
# ============================================
# Gemini
GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_TEMPERATURE = 0.7
GEMINI_MAX_TOKENS = 8192

# Groq (uses Llama, Mixtral, etc.)
GROQ_MODEL = "llama-3.3-70b-versatile"  # Fast and capable
GROQ_TEMPERATURE = 0.7
GROQ_MAX_TOKENS = 8192

# DeepSeek
DEEPSEEK_MODEL = "deepseek-chat"
DEEPSEEK_TEMPERATURE = 0.7
DEEPSEEK_MAX_TOKENS = 8192

# TogetherAI
TOGETHER_MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo"
TOGETHER_TEMPERATURE = 0.7
TOGETHER_MAX_TOKENS = 8192

# ============================================
# Blog Configuration
# ============================================
BLOG_NICHE = os.getenv("BLOG_NICHE", "technology")
BLOG_NAME = os.getenv("BLOG_NAME", "My AI Blog")
BLOG_URL = os.getenv("BLOG_URL", "http://localhost:3000")

# Content Settings
MIN_WORD_COUNT = int(os.getenv("MIN_WORD_COUNT", "2000"))
MAX_WORD_COUNT = int(os.getenv("MAX_WORD_COUNT", "3000"))
IMAGES_PER_POST = int(os.getenv("IMAGES_PER_POST", "5"))
VIDEOS_PER_POST = int(os.getenv("VIDEOS_PER_POST", "2"))

# Publishing Settings
AUTO_PUBLISH = os.getenv("AUTO_PUBLISH", "false").lower() == "true"
REVIEW_BEFORE_PUBLISH = os.getenv("REVIEW_BEFORE_PUBLISH", "true").lower() == "true"

# Trend Settings
TREND_REGION = os.getenv("TREND_REGION", "united_states")
TREND_CATEGORY = os.getenv("TREND_CATEGORY", "")  # Empty for all categories

# Global Trend Analysis
USE_GLOBAL_TRENDS = os.getenv("USE_GLOBAL_TRENDS", "true").lower() == "true"
TREND_FETCH_DELAY = float(os.getenv("TREND_FETCH_DELAY", "1.5"))  # Seconds between API calls
COMPETITION_THRESHOLD = int(os.getenv("COMPETITION_THRESHOLD", "50"))  # Prefer topics below this
MIN_TREND_SCORE = int(os.getenv("MIN_TREND_SCORE", "20"))  # Minimum score to consider

# ============================================
# Validation
# ============================================
def get_available_ai_providers():
    """Get list of configured AI providers"""
    providers = []
    if GEMINI_API_KEY:
        providers.append("gemini")
    if GROQ_API_KEY:
        providers.append("groq")
    if DEEPSEEK_API_KEY:
        providers.append("deepseek")
    if TOGETHER_API_KEY:
        providers.append("together")
    return providers

def validate_config():
    """Validate that at least one AI provider is configured"""
    providers = get_available_ai_providers()
    
    if not providers:
        raise ValueError(
            "No AI API keys configured. Please set at least one of:\n"
            "- GEMINI_API_KEY (recommended)\n"
            "- GROQ_API_KEY (fast)\n"
            "- DEEPSEEK_API_KEY\n"
            "- TOGETHER_API_KEY"
        )
    
    # Check image source
    if IMAGE_SOURCE == "pexels" and not PEXELS_API_KEY:
        print("Warning: PEXELS_API_KEY not set. Images will be disabled.")
    elif IMAGE_SOURCE == "stability" and not STABILITY_API_KEY:
        print("Warning: STABILITY_API_KEY not set. Falling back to Pexels.")
    
    return True
