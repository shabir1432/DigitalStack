"""
Google Trends Service
Fetches trending topics and related keywords for SEO optimization
"""
import time
import random
import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from config.settings import TREND_REGION

console = Console()

# Countries with RSS feed support
RSS_COUNTRIES = {
    'united_states': 'US',
    'united_kingdom': 'GB',
    'india': 'IN',
    'canada': 'CA',
    'australia': 'AU',
    'germany': 'DE',
    'france': 'FR',
    'brazil': 'BR',
    'japan': 'JP',
    'mexico': 'MX',
    'indonesia': 'ID',
    'italy': 'IT',
    'spain': 'ES',
    'south_korea': 'KR',
    'netherlands': 'NL',
    'argentina': 'AR',
    'russia': 'RU',
    'turkey': 'TR',
}

GLOBAL_REGIONS = list(RSS_COUNTRIES.keys())


class GoogleTrendsService:
    """Service for fetching Google Trends data and related keywords globally"""
    
    def __init__(self, region: str = TREND_REGION):
        self.region = region
        self.request_delay = 0.5
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        })
    
    def get_global_trends(self, regions: Optional[List[str]] = None, max_per_region: int = 20) -> List[Dict[str, Any]]:
        """Fetch trends from multiple countries using RSS feeds"""
        regions = regions or GLOBAL_REGIONS
        all_trends: Dict[str, Dict[str, Any]] = {}
        
        console.print(f"\n[bold blue]🌍 Scanning trends from {len(regions)} countries...[/bold blue]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Fetching trends...", total=len(regions))
            
            for region in regions:
                progress.update(task, description=f"Scanning {region.replace('_', ' ').title()}...")
                
                try:
                    regional_trends = self._fetch_rss_trends(region)
                    
                    for trend in regional_trends[:max_per_region]:
                        trend_lower = trend.lower().strip()
                        
                        if trend_lower in all_trends:
                            all_trends[trend_lower]['regions'].append(region)
                            all_trends[trend_lower]['score'] += 1
                        else:
                            all_trends[trend_lower] = {
                                'topic': trend,
                                'topic_normalized': trend_lower,
                                'regions': [region],
                                'score': 1,
                                'is_rising': True,
                            }
                    
                    time.sleep(self.request_delay)
                    
                except Exception as e:
                    console.print(f"[yellow]⚠ {region}: {e}[/yellow]")
                
                progress.advance(task)
        
        trends_list = list(all_trends.values())
        trends_list.sort(key=lambda x: x['score'], reverse=True)
        
        console.print(f"\n[green]✓ Found {len(trends_list)} unique trending topics[/green]")
        
        multi_region = [t for t in trends_list if t['score'] > 1]
        if multi_region:
            console.print(f"[green]  → {len(multi_region)} topics trending in multiple countries[/green]")
        
        return trends_list
    
    def _fetch_rss_trends(self, region: str) -> List[str]:
        """Fetch trends from Google Trends RSS feed"""
        country_code = RSS_COUNTRIES.get(region.lower(), 'US')
        rss_url = f"https://trends.google.com/trending/rss?geo={country_code}"
        
        try:
            response = self.session.get(rss_url, timeout=10)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            
            trends = []
            for item in root.findall('.//item/title'):
                if item.text:
                    trends.append(item.text.strip())
            
            return trends[:20]
            
        except Exception as e:
            return self._fetch_realtime_fallback(country_code)
    
    def _fetch_realtime_fallback(self, country_code: str) -> List[str]:
        """Fallback method using realtime trends"""
        try:
            url = f"https://trends.google.com/trends/trendingsearches/daily?geo={country_code}&hl=en"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    trends = []
                    for item in data.get('default', {}).get('trendingSearchesDays', []):
                        for search in item.get('trendingSearches', []):
                            title = search.get('title', {}).get('query', '')
                            if title:
                                trends.append(title)
                    return trends[:20]
                except:
                    pass
            return []
        except Exception:
            return []
    
    def get_trending_searches(self, region: Optional[str] = None) -> List[str]:
        """Get daily trending searches for a region"""
        region = region or self.region
        return self._fetch_rss_trends(region)
    
    def get_related_queries(self, keyword: str, geo: str = 'US') -> Dict[str, List[Dict[str, Any]]]:
        """
        Get related queries and trending keywords for a topic using Google Trends suggestions
        This helps with SEO by finding what people are also searching for
        """
        related_data = {
            'rising': [],
            'top': [],
            'suggestions': [],
            'trending_keywords': []
        }
        
        try:
            # Method 1: Google Trends Autocomplete API
            suggestions = self._get_trends_suggestions(keyword)
            related_data['suggestions'] = suggestions
            
            # Method 2: Generate related keywords based on common patterns
            patterns = self._generate_keyword_patterns(keyword)
            related_data['trending_keywords'] = patterns
            
            # Combine into rising/top format for compatibility
            for i, sugg in enumerate(suggestions[:10]):
                related_data['rising'].append({
                    'query': sugg,
                    'value': 100 - (i * 10)  # Simulated rising value
                })
            
            for pattern in patterns[:10]:
                related_data['top'].append({
                    'query': pattern,
                    'value': random.randint(50, 100)
                })
            
            console.print(f"[green]✓ Found {len(suggestions)} suggestions and {len(patterns)} keyword patterns[/green]")
            
        except Exception as e:
            console.print(f"[yellow]⚠ Could not fetch related queries: {e}[/yellow]")
        
        return related_data
    
    def _get_trends_suggestions(self, keyword: str) -> List[str]:
        """Get autocomplete suggestions from Google Trends"""
        suggestions = []
        
        try:
            # Google Trends autocomplete endpoint
            url = f"https://trends.google.com/trends/api/autocomplete/{requests.utils.quote(keyword)}"
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                # Response starts with ")]}'" which needs to be stripped
                text = response.text
                if text.startswith(")]}'"):
                    text = text[5:]
                
                import json
                data = json.loads(text)
                
                if 'default' in data and 'topics' in data['default']:
                    for topic in data['default']['topics']:
                        if 'title' in topic:
                            suggestions.append(topic['title'])
        except:
            pass
        
        # Fallback: Use Google Search suggestions
        if not suggestions:
            suggestions = self._get_google_suggestions(keyword)
        
        return suggestions
    
    def _get_google_suggestions(self, keyword: str) -> List[str]:
        """Get autocomplete suggestions from Google Search"""
        suggestions = []
        
        try:
            url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={requests.utils.quote(keyword)}"
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                import json
                data = json.loads(response.text)
                if len(data) > 1 and isinstance(data[1], list):
                    suggestions = data[1][:15]
        except:
            pass
        
        return suggestions
    
    def _generate_keyword_patterns(self, keyword: str) -> List[str]:
        """Generate SEO-friendly keyword variations"""
        patterns = []
        keyword_lower = keyword.lower()
        
        # Question patterns
        question_starters = ['what is', 'how to', 'why is', 'when is', 'where is', 'who is', 'best', 'top', 'latest']
        for starter in question_starters:
            patterns.append(f"{starter} {keyword_lower}")
        
        # Intent patterns
        intent_suffixes = ['news', 'update', 'today', '2026', 'live', 'highlights', 'results', 'latest news', 'breaking']
        for suffix in intent_suffixes:
            patterns.append(f"{keyword_lower} {suffix}")
        
        # Long-tail patterns
        long_tail = [
            f"{keyword_lower} explained",
            f"{keyword_lower} guide",
            f"{keyword_lower} everything you need to know",
            f"complete guide to {keyword_lower}",
            f"{keyword_lower} for beginners",
        ]
        patterns.extend(long_tail)
        
        return patterns[:20]
    
    def get_trending_hashtags(self, keyword: str) -> List[str]:
        """Generate trending hashtags for a topic"""
        hashtags = []
        
        # Clean keyword for hashtag
        clean_keyword = ''.join(word.capitalize() for word in keyword.split())
        
        # Direct hashtag
        hashtags.append(f"#{clean_keyword}")
        
        # Variations
        words = keyword.split()
        if len(words) > 1:
            for word in words:
                if len(word) > 3:
                    hashtags.append(f"#{word.capitalize()}")
        
        # Common trending hashtags
        common_tags = [
            "#Trending", "#Viral", "#News", "#Breaking", "#MustRead",
            "#Today", "#Latest", "#Update", "#Live", "#TopStory"
        ]
        hashtags.extend(common_tags[:5])
        
        # Category-specific
        keyword_lower = keyword.lower()
        if any(word in keyword_lower for word in ['game', 'match', 'score', 'vs', 'team']):
            hashtags.extend(["#Sports", "#Match", "#Live", "#Score"])
        elif any(word in keyword_lower for word in ['stock', 'market', 'crypto', 'price']):
            hashtags.extend(["#Finance", "#Investing", "#Markets"])
        elif any(word in keyword_lower for word in ['movie', 'film', 'actor', 'actress', 'show']):
            hashtags.extend(["#Entertainment", "#Movies", "#Celebrity"])
        elif any(word in keyword_lower for word in ['tech', 'ai', 'app', 'software']):
            hashtags.extend(["#Tech", "#Innovation", "#Digital"])
        
        return list(dict.fromkeys(hashtags))[:15]  # Remove duplicates, limit to 15
    
    def get_seo_keywords(self, keyword: str) -> Dict[str, Any]:
        """
        Get comprehensive SEO keywords for a topic
        Returns primary, secondary, and long-tail keywords
        """
        console.print(f"[cyan]🔍 Fetching SEO keywords for: {keyword}[/cyan]")
        
        # Get suggestions
        suggestions = self._get_google_suggestions(keyword)
        
        # Get related patterns
        patterns = self._generate_keyword_patterns(keyword)
        
        # Get hashtags
        hashtags = self.get_trending_hashtags(keyword)
        
        # Categorize keywords
        primary = keyword
        secondary = suggestions[:5] if suggestions else patterns[:5]
        long_tail = [s for s in suggestions if len(s.split()) >= 4][:10]
        
        if not long_tail:
            long_tail = [p for p in patterns if len(p.split()) >= 4][:10]
        
        result = {
            'primary_keyword': primary,
            'secondary_keywords': secondary,
            'long_tail_keywords': long_tail,
            'hashtags': hashtags,
            'all_suggestions': suggestions,
            'keyword_patterns': patterns,
            'seo_title_suggestions': [
                f"{keyword}: Everything You Need to Know",
                f"The Complete Guide to {keyword}",
                f"{keyword} - Latest News and Updates",
                f"Why {keyword} Is Trending Right Now",
                f"{keyword} Explained: What You Should Know",
            ]
        }
        
        console.print(f"[green]✓ Generated {len(secondary)} secondary keywords, {len(long_tail)} long-tail, {len(hashtags)} hashtags[/green]")
        
        return result
    
    def filter_by_niche(self, trends: List[Dict[str, Any]], niche_keywords: List[str]) -> List[Dict[str, Any]]:
        """Filter trends to only include those relevant to a niche"""
        niche_keywords_lower = [kw.lower() for kw in niche_keywords]
        
        filtered = []
        for trend in trends:
            topic_lower = trend['topic'].lower()
            if any(niche_kw in topic_lower for niche_kw in niche_keywords_lower):
                filtered.append(trend)
        
        console.print(f"[blue]Filtered to {len(filtered)} niche-relevant topics[/blue]")
        return filtered


# Singleton instance
_trends_instance = None

def get_trends_service() -> GoogleTrendsService:
    """Get or create the trends service instance"""
    global _trends_instance
    if _trends_instance is None:
        _trends_instance = GoogleTrendsService()
    return _trends_instance
