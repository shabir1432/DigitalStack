"""
Topic Scorer Service
Ranks topics based on volume, competition, and trend signals
"""
from typing import Dict, Any, List, Optional
from rich.console import Console
from rich.table import Table

console = Console()


class TopicScorer:
    """
    Scores and ranks topics to find the best content opportunities.
    
    Formula: Score = (Volume Proxy × Trend Multiplier) / Competition Factor
    
    Higher score = Better opportunity
    """
    
    def __init__(self):
        self.min_score_threshold = 20  # Minimum score to consider
    
    def score_topic(
        self,
        topic: str,
        regions: List[str],
        competition_data: Dict[str, Any],
        trend_data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Calculate a comprehensive score for a topic
        
        Args:
            topic: The topic keyword
            regions: List of regions where this topic is trending
            competition_data: Competition analysis from CompetitionAnalyzer
            trend_data: Additional trend data
            
        Returns:
            Scored topic with all metrics
        """
        # Volume Proxy: Based on number of regions trending + trend intensity
        volume_proxy = self._estimate_volume(regions, trend_data)
        
        # Trend Multiplier: Rising trends get bonus
        trend_multiplier = self._calculate_trend_multiplier(trend_data, regions)
        
        # Competition Factor: Lower competition = higher factor
        competition_score = competition_data.get('competition_score', 50)
        competition_factor = max(1, competition_score / 10)  # 1-10 range
        
        # Calculate final score
        raw_score = (volume_proxy * trend_multiplier) / competition_factor
        
        # Normalize to 0-100 scale
        final_score = min(100, raw_score)
        
        # Determine priority
        if final_score >= 70:
            priority = "🔥 HIGH"
            action = "Write immediately"
        elif final_score >= 50:
            priority = "⚡ MEDIUM"
            action = "Add to content queue"
        elif final_score >= 30:
            priority = "📝 LOW"
            action = "Consider if relevant"
        else:
            priority = "⏭️ SKIP"
            action = "Not recommended"
        
        return {
            'topic': topic,
            'final_score': round(final_score, 2),
            'priority': priority,
            'action': action,
            'metrics': {
                'volume_proxy': round(volume_proxy, 2),
                'trend_multiplier': round(trend_multiplier, 2),
                'competition_factor': round(competition_factor, 2),
                'competition_level': competition_data.get('competition_level', 'unknown'),
                'regions_count': len(regions),
                'regions': regions[:5],  # Top 5 regions
            },
            'is_long_tail': competition_data.get('is_long_tail', False),
            'recommendation': competition_data.get('recommendation', '')
        }
    
    def _estimate_volume(self, regions: List[str], trend_data: Optional[Dict]) -> float:
        """
        Estimate relative search volume based on:
        - Number of regions where topic is trending
        - Base score from trend data
        """
        # Base volume from region count (more regions = more global interest)
        region_volume = len(regions) * 10
        
        # Bonus for major markets
        major_markets = ['united_states', 'united_kingdom', 'india', 'germany', 'japan']
        major_market_bonus = sum(5 for r in regions if r in major_markets)
        
        # Base score from trend data
        base_score = 20
        if trend_data:
            base_score = trend_data.get('score', 1) * 10
        
        return base_score + region_volume + major_market_bonus
    
    def _calculate_trend_multiplier(self, trend_data: Optional[Dict], regions: List[str]) -> float:
        """
        Calculate multiplier based on trend signals
        
        Returns: 0.5 - 2.0 multiplier
        """
        multiplier = 1.0
        
        # Rising trends get bonus
        if trend_data and trend_data.get('is_rising', False):
            multiplier += 0.5
        
        # Multi-region trends get bonus
        if len(regions) >= 5:
            multiplier += 0.3
        elif len(regions) >= 3:
            multiplier += 0.2
        
        # Cap the multiplier
        return min(2.0, max(0.5, multiplier))
    
    def rank_topics(self, scored_topics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Rank topics by their final score
        
        Args:
            scored_topics: List of scored topic dicts
            
        Returns:
            Sorted list (best opportunities first)
        """
        # Sort by final score descending
        ranked = sorted(scored_topics, key=lambda x: x['final_score'], reverse=True)
        
        # Add rank numbers
        for i, topic in enumerate(ranked, 1):
            topic['rank'] = i
        
        return ranked
    
    def get_best_topic(self, scored_topics: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Get the single best topic to write about
        
        Args:
            scored_topics: List of scored topic dicts
            
        Returns:
            Best topic or None if no suitable topics
        """
        if not scored_topics:
            return None
        
        ranked = self.rank_topics(scored_topics)
        
        # Return best topic that meets minimum threshold
        for topic in ranked:
            if topic['final_score'] >= self.min_score_threshold:
                return topic
        
        # If none meet threshold, return the best available
        return ranked[0] if ranked else None
    
    def display_rankings(self, scored_topics: List[Dict[str, Any]], top_n: int = 10):
        """
        Display a formatted table of topic rankings
        """
        ranked = self.rank_topics(scored_topics)[:top_n]
        
        table = Table(title="📊 Topic Rankings (Best Opportunities)")
        table.add_column("Rank", style="cyan", width=6)
        table.add_column("Topic", style="white", max_width=40)
        table.add_column("Score", style="green", width=8)
        table.add_column("Priority", width=12)
        table.add_column("Competition", width=12)
        table.add_column("Regions", width=8)
        
        for topic in ranked:
            table.add_row(
                f"#{topic['rank']}",
                topic['topic'][:40],
                f"{topic['final_score']:.1f}",
                topic['priority'],
                topic['metrics']['competition_level'],
                str(topic['metrics']['regions_count'])
            )
        
        console.print(table)


# Singleton instance
_scorer_instance = None

def get_topic_scorer() -> TopicScorer:
    """Get or create the topic scorer instance"""
    global _scorer_instance
    if _scorer_instance is None:
        _scorer_instance = TopicScorer()
    return _scorer_instance
