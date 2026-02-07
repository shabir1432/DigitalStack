"""
Trend Research Agent
Responsible for finding trending topics globally and scoring them for best opportunities
"""
from typing import Dict, Any, List, Optional
import json

from agents.base_agent import BaseAgent
from services.google_trends import get_trends_service
from services.competition_analyzer import get_competition_analyzer
from services.topic_scorer import get_topic_scorer
from config.settings import BLOG_NICHE


# Niche keywords for filtering
NICHE_KEYWORDS = {
    'technology': ['ai', 'tech', 'software', 'app', 'digital', 'computer', 'code', 'programming', 'robot', 'machine learning', 'data', 'cyber', 'internet', 'startup', 'innovation'],
    'ai': ['ai', 'artificial intelligence', 'machine learning', 'chatgpt', 'gpt', 'llm', 'neural', 'deep learning', 'openai', 'gemini', 'claude', 'automation'],
    'health': ['health', 'fitness', 'wellness', 'diet', 'exercise', 'medical', 'mental health', 'nutrition'],
    'finance': ['crypto', 'bitcoin', 'stock', 'invest', 'money', 'finance', 'trading', 'bank', 'economy'],
    'entertainment': ['movie', 'film', 'tv', 'series', 'celebrity', 'music', 'game', 'gaming', 'streaming'],
}


class TrendAgent(BaseAgent):
    """Agent that researches trending topics globally with competition analysis"""
    
    def __init__(self):
        super().__init__(
            name="Trend Research Agent",
            description="Researching trending topics globally with competition scoring"
        )
        self.trends_service = get_trends_service()
        self.competition_analyzer = get_competition_analyzer()
        self.topic_scorer = get_topic_scorer()
    
    async def run(
        self,
        niche: Dict[str, Any],
        use_global: bool = True,
        count: int = 10
    ) -> Dict[str, Any]:
        """
        Research trending topics globally and select the best one based on
        volume/competition scoring.
        
        Args:
            niche: Niche configuration dictionary
            use_global: If True, fetch from multiple countries
            count: Number of trends to analyze
        """
        self.log_start()
        niche_name = niche.get("name", "Technology")

        
        try:
            # Step 1: Get global trends OR regional trends
            if use_global:
                self.log("🌍 Fetching GLOBAL trends from multiple countries...")
                all_trends = self.trends_service.get_global_trends()
            else:
                self.log("Fetching regional trends...")
                trends = self.trends_service.get_trending_searches()
                all_trends = [{'topic': t, 'regions': ['united_states'], 'score': 1, 'is_rising': True} for t in trends]
            
            if not all_trends:
                self.log("No trends found, using AI-generated topics", "warning")
                fallback = await self._get_fallback_topics(niche)
                all_trends = [{'topic': t, 'regions': [], 'score': 1, 'is_rising': True} for t in fallback]
            
            self.log(f"Found {len(all_trends)} unique trending topics")
            
            # Step 2: Filter by niche relevance
            self.log(f"Filtering for {niche_name} niche...")
            niche_keywords = NICHE_KEYWORDS.get(niche_name.lower(), NICHE_KEYWORDS['technology'])
            niche_trends = self.trends_service.filter_by_niche(all_trends, niche_keywords)
            
            # If no niche matches, use AI to find relevant ones from top global trends
            if not niche_trends:
                self.log("No direct niche matches, using AI to find relevant topics...")
                niche_trends = await self._ai_filter_trends(all_trends[:30], niche)
            
            # Step 3: Analyze competition for top candidates
            self.log("📊 Analyzing competition for top candidates...")
            scored_topics = []
            
            for trend in niche_trends[:count]:
                # Analyze competition
                competition = self.competition_analyzer.analyze_competition(
                    trend['topic'],
                    trend_data=trend
                )
                
                # Score the topic
                scored = self.topic_scorer.score_topic(
                    topic=trend['topic'],
                    regions=trend.get('regions', []),
                    competition_data=competition,
                    trend_data=trend
                )
                
                scored_topics.append(scored)
            
            # Step 4: Get best topic
            self.topic_scorer.display_rankings(scored_topics, top_n=count)
            
            best_topic = self.topic_scorer.get_best_topic(scored_topics)
            
            if not best_topic:
                self.log("No suitable topic found, using first available", "warning")
                best_topic = scored_topics[0] if scored_topics else None
            
            self.log(f"🏆 Selected: {best_topic['topic']} (Score: {best_topic['final_score']:.1f})")
            
            # Step 5: Get related queries for content ideas
            related_queries = self.trends_service.get_related_queries(best_topic['topic'])
            
            # Step 6: Use AI to refine the topic angle
            self.log("Refining topic angle with AI...")
            analysis = await self._analyze_topic(best_topic, niche)
            
            result = {
                "selected_topic": analysis.get("selected_topic", best_topic['topic']),
                "original_trend": best_topic['topic'],
                "score": best_topic['final_score'],
                "priority": best_topic['priority'],
                "competition_level": best_topic['metrics']['competition_level'],
                "regions": best_topic['metrics'].get('regions', []),
                "regions_count": best_topic['metrics']['regions_count'],
                "analysis": analysis,
                "all_scored_topics": scored_topics[:5],  # Top 5 for reference
                "related_queries": related_queries,
                "niche": niche,
                "recommendation": best_topic.get('recommendation', '')
            }
            
            self.log_complete()
            return result
            
        except Exception as e:
            self.log(f"Error: {e}", "error")
            raise
    
    async def _ai_filter_trends(self, trends: List[Dict], niche: str) -> List[Dict]:
        """Use AI to find niche-relevant trends from global trends"""
        
        topics = [t['topic'] for t in trends]
        
        prompt = f"""From these globally trending topics, select the ones that could be relevant 
to a {niche} blog or could be given a {niche} angle:

Topics:
{json.dumps(topics, indent=2)}

Return a JSON array of the relevant topics (exact match from list):
["topic1", "topic2", ...]

Select up to 10 most relevant topics. If a topic can be discussed from a {niche} perspective, include it."""

        relevant_topics = self.llm.generate_json(prompt)
        
        if isinstance(relevant_topics, list):
            # Filter original trends to keep metadata
            relevant_set = set(t.lower() for t in relevant_topics)
            return [t for t in trends if t['topic'].lower() in relevant_set]
        
        return trends[:10]  # Fallback to top global trends
    
    async def _analyze_topic(self, scored_topic: Dict, niche: str) -> Dict[str, Any]:
        """Use AI to refine the selected topic with a unique angle"""
        
        prompt = f"""This trending topic has been selected for a {niche} blog based on data analysis:

Topic: {scored_topic['topic']}
Score: {scored_topic['final_score']}/100
Competition: {scored_topic['metrics']['competition_level']}
Trending in: {scored_topic['metrics']['regions_count']} countries

Create an engaging blog post plan for this topic:

Return JSON:
{{
    "selected_topic": "refined topic title (can enhance the original)",
    "reason": "why this is a great topic to cover now",
    "angle": "unique angle for {niche} audience",
    "target_audience": "who would read this",
    "content_type": "listicle/how-to/news/analysis/guide/comparison",
    "estimated_interest": "high/medium/low",
    "suggested_title": "catchy, SEO-friendly blog post title",
    "key_points": ["point 1", "point 2", "point 3"]
}}"""

        return self.llm.generate_json(prompt)
    
    async def _get_fallback_topics(self, niche: str) -> List[str]:
        """Generate fallback topics if trends API fails"""
        
        prompt = f"""Generate 10 trending and engaging blog topics for the {niche} niche.
These should be topics that would be currently relevant and interesting.

Return a JSON array of topic strings:
["topic 1", "topic 2", ...]"""

        result = self.llm.generate_json(prompt)
        
        if isinstance(result, list):
            return result
        return result.get("topics", [f"Latest {niche} trends", f"Top {niche} tips"])
    
    def get_trending_hashtags(self, topic: str) -> List[str]:
        """Get trending hashtags related to a topic"""
        
        prompt = f"""Generate 10 trending hashtags for this topic: {topic}

These should be hashtags that are:
1. Currently popular on social media
2. Relevant to the topic
3. A mix of broad and specific hashtags

Return a JSON array:
["#Hashtag1", "#Hashtag2", ...]"""

        result = self.llm.generate_json(prompt)
        
        if isinstance(result, list):
            return result
        return result.get("hashtags", [f"#{topic.replace(' ', '')}"])
