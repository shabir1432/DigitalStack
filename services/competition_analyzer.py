"""
Competition Analyzer Service
Estimates keyword competition using FREE methods
"""
import re
import time
import random
from typing import Dict, Any, Optional
from urllib.parse import quote_plus
import requests
from rich.console import Console

console = Console()


class CompetitionAnalyzer:
    """
    Estimates keyword competition using free methods:
    1. Google Search Results count approximation
    2. Trend direction analysis
    3. Query complexity scoring
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def analyze_competition(self, keyword: str, trend_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Analyze competition for a keyword
        
        Args:
            keyword: The keyword to analyze
            trend_data: Optional trend data from Google Trends
            
        Returns:
            Competition analysis with score
        """
        console.print(f"[blue]Analyzing competition for: {keyword}[/blue]")
        
        # Get various competition signals
        word_count = len(keyword.split())
        char_count = len(keyword)
        
        # Estimate based on query characteristics
        complexity_score = self._calculate_complexity_score(keyword)
        
        # Get trend direction if available
        trend_score = self._analyze_trend_direction(trend_data) if trend_data else 50
        
        # Calculate final competition score (0-100, lower = less competition)
        competition_score = self._calculate_final_score(
            complexity_score=complexity_score,
            trend_score=trend_score,
            word_count=word_count
        )
        
        # Determine competition level
        if competition_score < 30:
            level = "low"
            difficulty = "Easy to rank"
        elif competition_score < 60:
            level = "medium"
            difficulty = "Moderate effort needed"
        else:
            level = "high"
            difficulty = "Competitive - needs strong content"
        
        result = {
            'keyword': keyword,
            'competition_score': round(competition_score, 2),
            'competition_level': level,
            'difficulty': difficulty,
            'word_count': word_count,
            'is_long_tail': word_count >= 3,
            'trend_score': trend_score,
            'recommendation': self._get_recommendation(competition_score, trend_score)
        }
        
        console.print(f"[green]Competition: {level} (score: {competition_score:.0f}/100)[/green]")
        
        return result
    
    def _calculate_complexity_score(self, keyword: str) -> float:
        """
        Calculate complexity based on keyword characteristics
        Long-tail keywords (3+ words) typically have lower competition
        """
        words = keyword.lower().split()
        word_count = len(words)
        
        # Base score - more words = likely less competition
        if word_count >= 5:
            base_score = 20
        elif word_count >= 4:
            base_score = 30
        elif word_count >= 3:
            base_score = 40
        elif word_count >= 2:
            base_score = 60
        else:
            base_score = 80  # Single words are very competitive
        
        # Adjust for specific patterns
        adjustments = 0
        
        # Questions are often less competitive
        question_words = ['how', 'what', 'why', 'when', 'where', 'which', 'who']
        if words[0] in question_words:
            adjustments -= 10
        
        # Year in query often indicates freshness opportunity
        if any(str(year) in keyword for year in range(2024, 2030)):
            adjustments -= 15
        
        # "vs" comparisons are often good opportunities
        if ' vs ' in keyword.lower() or ' versus ' in keyword.lower():
            adjustments -= 10
        
        # "best", "top", "review" are competitive
        competitive_words = ['best', 'top', 'review', 'buy', 'cheap', 'free']
        if any(word in words for word in competitive_words):
            adjustments += 15
        
        return max(10, min(95, base_score + adjustments))
    
    def _analyze_trend_direction(self, trend_data: Dict) -> float:
        """
        Analyze if the trend is rising, stable, or falling
        Rising trends = better opportunity
        
        Returns score 0-100 (higher = better opportunity)
        """
        if not trend_data:
            return 50  # Neutral
        
        regions_count = len(trend_data.get('regions', []))
        base_score = trend_data.get('score', 1)
        
        # More regions = more global interest
        regional_bonus = min(regions_count * 5, 30)
        
        # Rising trends get bonus
        is_rising = trend_data.get('is_rising', False)
        rising_bonus = 20 if is_rising else 0
        
        return min(100, 40 + regional_bonus + rising_bonus)
    
    def _calculate_final_score(self, complexity_score: float, trend_score: float, word_count: int) -> float:
        """
        Calculate final competition score
        
        Lower score = Less competition = Better opportunity
        """
        # Weight the factors
        # Complexity (query characteristics): 60%
        # Trend opportunity (inverse): 40%
        
        # Invert trend score for competition (high trend opp = low competition value)
        trend_competition = 100 - trend_score
        
        weighted_score = (complexity_score * 0.6) + (trend_competition * 0.4)
        
        return weighted_score
    
    def _get_recommendation(self, competition_score: float, trend_score: float) -> str:
        """Get actionable recommendation based on scores"""
        
        if competition_score < 30 and trend_score > 60:
            return "🎯 EXCELLENT - Low competition + Rising trend. High priority!"
        elif competition_score < 30:
            return "✅ GOOD - Low competition. Worth pursuing."
        elif competition_score < 50 and trend_score > 50:
            return "👍 DECENT - Medium competition but trending. Consider it."
        elif competition_score < 60:
            return "⚠️ MODERATE - Some competition. Need quality content."
        else:
            return "❌ SKIP - High competition. Look for alternatives."
    
    def batch_analyze(self, keywords: list, trend_data: Optional[Dict[str, Dict]] = None) -> list:
        """
        Analyze multiple keywords
        
        Args:
            keywords: List of keywords to analyze
            trend_data: Optional dict mapping keywords to their trend data
            
        Returns:
            List of competition analyses sorted by opportunity (best first)
        """
        results = []
        trend_data = trend_data or {}
        
        for keyword in keywords:
            kw_trend = trend_data.get(keyword, None)
            analysis = self.analyze_competition(keyword, kw_trend)
            results.append(analysis)
            
            # Small delay to be respectful
            time.sleep(0.1)
        
        # Sort by competition score (lower = better opportunity)
        results.sort(key=lambda x: x['competition_score'])
        
        return results


# Singleton instance
_analyzer_instance = None

def get_competition_analyzer() -> CompetitionAnalyzer:
    """Get or create the competition analyzer instance"""
    global _analyzer_instance
    if _analyzer_instance is None:
        _analyzer_instance = CompetitionAnalyzer()
    return _analyzer_instance
