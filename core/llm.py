"""
Multi-Provider LLM Wrapper with Rate Limit Handling
Supports: Gemini, Groq, DeepSeek, TogetherAI
Automatically retries on rate limits and falls back to alternatives
"""
import json
import time
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
from rich.console import Console

from config.settings import (
    GEMINI_API_KEY, GROQ_API_KEY, DEEPSEEK_API_KEY, TOGETHER_API_KEY,
    GEMINI_MODEL, GROQ_MODEL, DEEPSEEK_MODEL, TOGETHER_MODEL,
    GEMINI_TEMPERATURE, GROQ_TEMPERATURE, DEEPSEEK_TEMPERATURE, TOGETHER_TEMPERATURE,
    GEMINI_MAX_TOKENS, GROQ_MAX_TOKENS, DEEPSEEK_MAX_TOKENS, TOGETHER_MAX_TOKENS,
    PRIMARY_AI_MODEL, FALLBACK_AI_MODEL, get_available_ai_providers
)

console = Console()

# Rate limit retry settings
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 65  # Gemini rate limit resets after 60 seconds


class BaseLLM(ABC):
    """Base class for LLM providers"""
    
    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None, 
                 temperature: float = 0.7, max_tokens: int = 8192) -> str:
        pass
    
    def generate_json(self, prompt: str, system_prompt: Optional[str] = None,
                      temperature: float = 0.7) -> Dict[str, Any]:
        """Generate and parse JSON response"""
        response = self.generate(
            prompt=prompt + "\n\nRespond with valid JSON only. No markdown, no code blocks.",
            system_prompt=system_prompt,
            temperature=temperature
        )
        return json.loads(self._clean_json(response))
    
    def _clean_json(self, text: str) -> str:
        """Clean up JSON response"""
        if text.startswith("```"):
            lines = text.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines)
        return text.strip()


class GeminiLLM(BaseLLM):
    """Google Gemini API wrapper with rate limit handling"""
    
    def __init__(self):
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.genai = genai
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None,
                 temperature: float = GEMINI_TEMPERATURE, 
                 max_tokens: int = GEMINI_MAX_TOKENS) -> str:
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        
        config = self.genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
        
        # Retry logic for rate limits
        for attempt in range(MAX_RETRIES):
            try:
                response = self.model.generate_content(full_prompt, generation_config=config)
                return response.text.strip()
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "quota" in error_str.lower() or "rate" in error_str.lower():
                    if attempt < MAX_RETRIES - 1:
                        console.print(f"[yellow]Rate limited. Waiting {RETRY_DELAY_SECONDS}s... (attempt {attempt + 1}/{MAX_RETRIES})[/yellow]")
                        time.sleep(RETRY_DELAY_SECONDS)
                        continue
                raise
        
        raise RuntimeError("Max retries exceeded")


class GroqLLM(BaseLLM):
    """Groq API wrapper - Super fast inference"""
    
    def __init__(self):
        from groq import Groq
        self.client = Groq(api_key=GROQ_API_KEY)
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None,
                 temperature: float = GROQ_TEMPERATURE,
                 max_tokens: int = GROQ_MAX_TOKENS) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()


class DeepSeekLLM(BaseLLM):
    """DeepSeek API wrapper - Strong reasoning"""
    
    def __init__(self):
        from openai import OpenAI
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com/v1"
        )
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None,
                 temperature: float = DEEPSEEK_TEMPERATURE,
                 max_tokens: int = DEEPSEEK_MAX_TOKENS) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()


class TogetherLLM(BaseLLM):
    """TogetherAI wrapper - Multiple open source models"""
    
    def __init__(self):
        from openai import OpenAI
        self.client = OpenAI(
            api_key=TOGETHER_API_KEY,
            base_url="https://api.together.xyz/v1"
        )
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None,
                 temperature: float = TOGETHER_TEMPERATURE,
                 max_tokens: int = TOGETHER_MAX_TOKENS) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=TOGETHER_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()


class MultiProviderLLM:
    """
    Multi-provider LLM that automatically:
    1. Uses the primary provider with retry on rate limits
    2. Falls back to secondary on failure
    3. Tries all available providers if needed
    """
    
    def __init__(self):
        self.providers: Dict[str, BaseLLM] = {}
        self.provider_order: List[str] = []
        self._init_providers()
    
    def _init_providers(self):
        """Initialize available providers in order of preference"""
        available = get_available_ai_providers()
        
        # Order: primary, fallback, then rest
        order = []
        if PRIMARY_AI_MODEL in available:
            order.append(PRIMARY_AI_MODEL)
        if FALLBACK_AI_MODEL in available and FALLBACK_AI_MODEL not in order:
            order.append(FALLBACK_AI_MODEL)
        for p in available:
            if p not in order:
                order.append(p)
        
        self.provider_order = order
        console.print(f"[cyan]Available AI providers: {order}[/cyan]")
        
        # Initialize providers lazily
        self._provider_classes = {
            "gemini": GeminiLLM,
            "groq": GroqLLM,
            "deepseek": DeepSeekLLM,
            "together": TogetherLLM,
        }
    
    def _get_provider(self, name: str) -> BaseLLM:
        """Get or create a provider instance"""
        if name not in self.providers:
            if name in self._provider_classes:
                self.providers[name] = self._provider_classes[name]()
        return self.providers.get(name)
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None,
                 temperature: float = 0.7, max_tokens: int = 8192,
                 json_mode: bool = False) -> str:
        """Generate text with automatic retry and fallback"""
        
        if json_mode:
            prompt += "\n\nRespond with valid JSON only. No markdown, no code blocks."
        
        last_error = None
        for provider_name in self.provider_order:
            try:
                provider = self._get_provider(provider_name)
                if provider:
                    console.print(f"[blue]Using {provider_name}...[/blue]")
                    result = provider.generate(prompt, system_prompt, temperature, max_tokens)
                    if json_mode:
                        result = provider._clean_json(result)
                    return result
            except Exception as e:
                console.print(f"[yellow]{provider_name} failed: {e}, trying next...[/yellow]")
                last_error = e
                continue
        
        raise RuntimeError(f"All AI providers failed. Last error: {last_error}")
    
    def generate_json(self, prompt: str, system_prompt: Optional[str] = None,
                      temperature: float = 0.7) -> Dict[str, Any]:
        """Generate and parse JSON with automatic fallback"""
        response = self.generate(prompt, system_prompt, temperature, json_mode=True)
        return json.loads(response)
    
    # Convenience methods for blog generation
    def analyze_trends(self, trends: List[str], niche: str) -> Dict[str, Any]:
        """Analyze trending topics and select the best one"""
        prompt = f"""Analyze these trending topics and select the BEST one for a {niche} blog:

Trending Topics:
{json.dumps(trends, indent=2)}

Consider:
1. Relevance to {niche} niche
2. Potential for engaging content
3. Evergreen value vs trending timeliness
4. Audience interest level

Return JSON with:
{{
    "selected_topic": "the best topic",
    "reason": "why this topic was selected",
    "angle": "unique angle to cover this topic",
    "target_audience": "who would read this",
    "content_type": "listicle/how-to/news/analysis/guide"
}}"""
        return self.generate_json(prompt)
    
    def generate_keywords(self, topic: str, niche: str) -> Dict[str, Any]:
        """Generate SEO keywords and hashtags for a topic"""
        prompt = f"""Generate comprehensive SEO data for this blog topic:

Topic: {topic}
Niche: {niche}

Return JSON with:
{{
    "primary_keyword": "main keyword to target",
    "secondary_keywords": ["list", "of", "secondary", "keywords"],
    "long_tail_keywords": ["longer", "more specific", "keyword phrases"],
    "hashtags": ["#Hashtag1", "#Hashtag2", "#Hashtag3"],
    "meta_title": "SEO optimized title (50-60 chars)",
    "meta_description": "Compelling meta description (150-160 chars)",
    "suggested_headings": ["H2 heading ideas"],
    "related_topics": ["related topics for internal linking"]
}}"""
        return self.generate_json(prompt)
    
    def write_blog_post(self, topic: str, keywords: Dict[str, Any],
                        min_words: int = 2000, max_words: int = 3000) -> str:
        """Write a comprehensive blog post"""
        system_prompt = """You are an expert content writer who creates engaging, informative, and SEO-optimized blog posts.
Your content is well-researched, accurate, engaging, properly structured, and SEO optimized naturally."""

        prompt = f"""Write a comprehensive blog post about: {topic}

SEO Data:
- Primary Keyword: {keywords.get('primary_keyword', topic)}
- Secondary Keywords: {', '.join(keywords.get('secondary_keywords', []))}
- Target Title: {keywords.get('meta_title', topic)}

Requirements:
1. Word count: {min_words}-{max_words} words
2. Use markdown formatting with H2 and H3 headings
3. Include engaging introduction and compelling conclusion
4. Add [IMAGE: description] placeholders (4-5 throughout)
5. Add [VIDEO: topic] placeholders (1-2)
6. Include FAQ section with 4-5 questions

Write the complete blog post now:"""

        return self.generate(prompt, system_prompt, temperature=0.7)


# Singleton instance
_llm_instance = None

def get_llm() -> MultiProviderLLM:
    """Get or create the multi-provider LLM instance"""
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = MultiProviderLLM()
    return _llm_instance
