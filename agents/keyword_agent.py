"""
Keyword Analyst Agent
Responsible for generating SEO keywords, hashtags, and meta data using Google Trends
"""
from typing import Dict, Any, List, Optional
from rich.console import Console

from agents.base_agent import BaseAgent
from services.google_trends import get_trends_service
from config.settings import BLOG_NICHE

console = Console()


class KeywordAgent(BaseAgent):
    """Agent that analyzes keywords and generates SEO data for viral potential"""
    
    def __init__(self):
        super().__init__(
            name="Keyword Analyst Agent",
            description="Generating SEO keywords, hashtags, and meta data"
        )
        self.trends_service = get_trends_service()
    
    async def run(
        self,
        topic: str,
        niche: Optional[str] = None,
        analysis: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive SEO data for a topic using Google Trends
        
        Args:
            topic: The blog topic
            niche: Blog niche
            analysis: Optional trend analysis from TrendAgent
            
        Returns:
            SEO data including keywords, hashtags, and meta information
        """
        self.log_start()
        niche = niche or BLOG_NICHE
        
        try:
            # Step 1: Get SEO keywords from Google Trends/Suggestions
            self.log("Fetching trending keywords from Google...")
            seo_keywords = self.trends_service.get_seo_keywords(topic)
            
            # Step 2: Get related queries
            self.log("Fetching related search queries...")
            related_queries = self.trends_service.get_related_queries(topic)
            
            # Step 3: Generate comprehensive SEO data with AI
            self.log("Generating optimized SEO data for viral potential...")
            seo_data = await self._generate_viral_seo_data(
                topic, niche, seo_keywords, related_queries, analysis
            )
            
            # Step 4: Combine all hashtags
            google_hashtags = seo_keywords.get('hashtags', [])
            ai_hashtags = seo_data.get('hashtags', [])
            all_hashtags = list(dict.fromkeys(google_hashtags + ai_hashtags))[:20]
            seo_data['hashtags'] = all_hashtags
            
            # Step 5: Add Google's suggested keywords
            seo_data['google_suggestions'] = seo_keywords.get('all_suggestions', [])
            seo_data['keyword_patterns'] = seo_keywords.get('keyword_patterns', [])
            
            result = {
                "topic": topic,
                "niche": niche,
                "seo_data": seo_data,
                "related_queries": related_queries,
                "google_keywords": seo_keywords
            }
            
            # Display keywords found
            self._display_seo_summary(seo_data)
            
            self.log_complete()
            return result
            
        except Exception as e:
            self.log(f"Error: {e}", "error")
            raise
    
    async def _generate_viral_seo_data(
        self,
        topic: str,
        niche: str,
        seo_keywords: Dict[str, Any],
        related_queries: Dict[str, List],
        analysis: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate SEO data optimized for viral potential"""
        
        # Extract keywords from Google
        google_suggestions = seo_keywords.get('all_suggestions', [])
        google_patterns = seo_keywords.get('keyword_patterns', [])
        google_hashtags = seo_keywords.get('hashtags', [])
        
        rising_queries = [q.get('query', '') for q in related_queries.get('rising', [])]
        top_queries = [q.get('query', '') for q in related_queries.get('top', [])]
        
        suggested_title = ""
        if analysis:
            suggested_title = analysis.get('suggested_title', '')
        
        prompt = f"""You are an expert SEO specialist. Generate viral-optimized SEO data for this trending blog topic.

Topic: {topic}
Niche: {niche}
Suggested Title: {suggested_title}

GOOGLE TRENDS DATA (USE THESE - THEY'RE WHAT PEOPLE ARE SEARCHING):
- Google Suggestions: {google_suggestions[:10]}
- Rising Queries: {rising_queries[:5]}
- Top Related Queries: {top_queries[:5]}
- Trending Hashtags: {google_hashtags[:10]}
- Keyword Patterns: {google_patterns[:10]}

REQUIREMENTS FOR VIRAL POTENTIAL:
1. Use the EXACT Google suggestions as secondary keywords (people are searching these!)
2. Title should be clickbait-worthy but honest (use numbers, power words, curiosity gaps)
3. Meta description should create urgency and FOMO
4. Include trending hashtags that are currently popular
5. Focus on search intent - what are people REALLY looking for?

Return JSON:
{{
    "primary_keyword": "{topic}",
    "secondary_keywords": ["use Google suggestions here - exactly as shown"],
    "long_tail_keywords": ["4-7 word phrases from the patterns"],
    "meta_title": "Viral-worthy title (60 chars max, include primary keyword, use numbers/power words)",
    "meta_description": "Compelling 155 char description with urgency, FOMO, and call-to-action",
    "slug": "url-friendly-slug",
    "focus_keyphrase": "main 2-4 word phrase to optimize for",
    "suggested_headings": [
        "H2 headings that match search intent and use keywords"
    ],
    "hashtags": ["#Trending", "#TopicHash", "use relevant hashtags"],
    "viral_hooks": [
        "3 attention-grabbing opening lines"
    ],
    "click_triggers": ["words that increase CTR: exclusive, breaking, finally, revealed"],
    "schema_type": "NewsArticle"
}}"""

        return self.llm.generate_json(prompt)
    
    def _display_seo_summary(self, seo_data: Dict[str, Any]):
        """Display a summary of SEO data found"""
        console.print("\n[bold cyan]📊 SEO Keywords Summary:[/bold cyan]")
        console.print(f"  Primary: [white]{seo_data.get('primary_keyword', 'N/A')}[/white]")
        
        secondary = seo_data.get('secondary_keywords', [])[:5]
        if secondary:
            console.print(f"  Secondary: [dim]{', '.join(secondary)}[/dim]")
        
        hashtags = seo_data.get('hashtags', [])[:8]
        if hashtags:
            console.print(f"  Hashtags: [magenta]{' '.join(hashtags)}[/magenta]")
        
        console.print("")
    
    def format_for_writer(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Format keyword data for the Writer Agent with all SEO data"""
        
        seo_data = result.get("seo_data", {})
        google_keywords = result.get("google_keywords", {})
        
        # Combine all keywords for maximum SEO
        all_secondary = seo_data.get("secondary_keywords", [])
        google_suggestions = google_keywords.get("all_suggestions", [])
        
        # Merge and dedupe
        combined_keywords = list(dict.fromkeys(all_secondary + google_suggestions))[:15]
        
        return {
            "topic": result.get("topic", ""),
            "title": seo_data.get("meta_title", result.get("topic", "")),
            "primary_keyword": seo_data.get("primary_keyword", ""),
            "secondary_keywords": combined_keywords,
            "long_tail_keywords": seo_data.get("long_tail_keywords", []),
            "suggested_headings": seo_data.get("suggested_headings", []),
            "hashtags": seo_data.get("hashtags", []),
            "meta_description": seo_data.get("meta_description", ""),
            "slug": seo_data.get("slug", ""),
            "schema_type": seo_data.get("schema_type", "NewsArticle"),
            "viral_hooks": seo_data.get("viral_hooks", []),
            "click_triggers": seo_data.get("click_triggers", []),
            "google_suggestions": google_suggestions,
            "keyword_patterns": google_keywords.get("keyword_patterns", [])
        }
