"""
SEO Service
Handles SERP analysis, search intent detection, and competitor research.
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
import time
import random
from rich.console import Console
from urllib.parse import quote_plus
from core.llm import get_llm
from config.settings import SERP_MAX_RESULTS, ENABLE_SERP_ANALYSIS

console = Console()

class SEOService:
    """Service for SEO analysis and SERP scraping"""
    
    def __init__(self):
        self.llm = get_llm()
        # Rotation of User-Agents to avoid immediate blocking
        self.user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        ]
    
    def analyze_search_intent(self, keyword: str) -> Dict[str, Any]:
        """
        Analyze the search intent for a keyword by inspecting top results.
        Returns:
            Dict containing 'intent', 'difficulty', 'content_type_needed'
        """
        if not ENABLE_SERP_ANALYSIS:
            return {"intent": "informational", "difficulty": "medium", "content_type": "article"}
            
        console.print(f"[cyan]🔍 Analyzing SERP for: {keyword}[/cyan]")
        
        # 1. Fetch Top Results
        results = self._scrape_google_serp(keyword, limit=5)
        
        if not results:
            console.print("[yellow]⚠️ Could not scrape SERP. Defaulting to AI reasoning.[/yellow]")
            return self._analyze_intent_without_serp(keyword)
            
        # 2. Extract Snippets for AI Analysis
        serp_context = "\n".join([
            f"{i+1}. {r['title']} - {r['snippet']} ({r['domain']})"
            for i, r in enumerate(results)
        ])
        
        # 3. AI Analysis
        prompt = f"""
        Analyze these Google Search Results for the keyword: "{keyword}"
        
        Top Results:
        {serp_context}
        
        Determine:
        1. Search Intent (Informational, Transactional, Navigational, Commercial)
        2. Content Type Needed (Listicle, How-to Guide, Review, Comparison, Opinion)
        3. Ranking Difficulty (Easy, Medium, Hard - based on if top domains are huge like Wikipedia/Amazon or small blogs)
        
        Return JSON only: {{ "intent": "...", "content_type": "...", "difficulty": "..." }}
        """
        
        try:
            analysis = self.llm.generate(prompt, max_tokens=200)
            # Basic cleaning if LLM returns markdown code block
            analysis = analysis.replace("```json", "").replace("```", "").strip()
            import json
            return json.loads(analysis)
        except Exception as e:
            console.print(f"[red]Error analyzing intent: {e}[/red]")
            return {"intent": "informational", "content_type": "article", "difficulty": "unknown"}

    def extract_competitor_gaps(self, keyword: str, competitors: List[Dict]) -> Dict[str, Any]:
        """
        Analyze competitor content to find gaps.
        """
        # In a real heavy production env, we would scrape the full body text.
        # For now, we analyze title + snippets to find 'Topic Gaps'.
        
        context = "\n".join([f"- {c['title']}: {c['snippet']}" for c in competitors])
        
        prompt = f"""
        I want to write the best article on the internet for "{keyword}".
        Here are the current top competitors:
        {context}
        
        Identify:
        1. Three topics/questions they missed (Gaps).
        2. One angle that would make my article "10X" better.
        3. Scientific/Data-backed subsections I should add.
        
        Return JSON: {{ "gaps": [], "angle": "...", "data_points": [] }}
        """
        
        try:
            response = self.llm.generate(prompt)
            response = response.replace("```json", "").replace("```", "").strip()
            import json
            return json.loads(response)
        except:
            return {"gaps": ["Detailed FAQ", "Expert Real-world Examples"], "angle": "More depth", "data_points": []}

    def generate_ranking_blueprint(self, keyword: str) -> Dict[str, Any]:
        """
        Generate a comprehensive ranking blueprint (H1-H3 structure).
        """
        # 1. Get SERP data
        results = self._scrape_google_serp(keyword, limit=5)
        
        # 2. Analyze Gaps
        gaps = self.extract_competitor_gaps(keyword, results)
        
        # 3. Create Blueprint
        prompt = f"""
        Create a "Ranking Blueprint" for a blog post about: "{keyword}".
        Target Audience: Professionals/Enthusiasts (High Authority).
        
        Competitor Gaps to fill: {gaps.get('gaps')}
        Unique Angle: {gaps.get('angle')}
        
        Generate a structure:
        - H1 (Catchy, SEO optimized)
        - Target Word Count
        - Section-by-section Outline (H2s and H3s)
        - Key "Power Terms" to use (LSI keywords) 
        - Featured Snippet Target (Answer < 50 words)
        
        Format as JSON: 
        {{
            "h1": "...",
            "target_word_count": 3000,
            "outline": [
                {{ "heading": "...", "subsections": ["..."] }}
            ],
            "lsi_keywords": ["..."],
            "featured_snippet": "..."
        }}
        """
        
        try:
            response = self.llm.generate(prompt)
            response = response.replace("```json", "").replace("```", "").strip()
            import json
            return json.loads(response)
        except Exception as e:
            console.print(f"[red]Error generating blueprint: {e}[/red]")
            # Fallback simple structure
            return {
                "h1": f"Complete Guide to {keyword} (2025 Edition)",
                "target_word_count": 2500,
                "outline": [{"heading": "Introduction", "subsections": []}],
                "lsi_keywords": [],
                "featured_snippet": ""
            }

    def _scrape_google_serp(self, keyword: str, limit: int = 5) -> List[Dict[str, str]]:
        """
        Scrape Google SERP nicely using requests + BS4.
        Note: This is a fragile method. In production, use SerpApi.
        """
        try:
            url = f"https://www.google.com/search?q={quote_plus(keyword)}&num={limit+2}"
            headers = {
                "User-Agent": random.choice(self.user_agents)
            }
            
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code != 200:
                return []
                
            soup = BeautifulSoup(response.text, "html.parser")
            results = []
            
            # This selector often changes, but standard 'g' class is stable for div containers
            for g in soup.find_all("div", class_="g")[:limit]:
                title_elm = g.find("h3")
                link_elm = g.find("a")
                snippet_elm = g.find("div", {"style": "-webkit-line-clamp:2"}) or g.find("span", class_="aCOpRe") 
                
                # Fallback for snippet
                if not snippet_elm:
                     # iterate text to find something that looks like a description
                     pass

                if title_elm and link_elm:
                    results.append({
                        "title": title_elm.get_text(),
                        "url": link_elm["href"],
                        "domain": link_elm["href"].split("/")[2] if "//" in link_elm["href"] else "",
                        "snippet": snippet_elm.get_text() if snippet_elm else "No snippet available"
                    })
            
            return results
            
        except Exception as e:
            console.print(f"[yellow]SERP Scraping failed: {e}[/yellow]")
            return []

    def _analyze_intent_without_serp(self, keyword: str) -> Dict[str, Any]:
        """Fallback if scraping fails"""
        prompt = f"""
        Determine the search intent for "{keyword}".
        Return JSON: {{ "intent": "...", "content_type": "...", "difficulty": "medium" }}
        """
        try:
            response = self.llm.generate(prompt)
            response = response.replace("```json", "").replace("```", "").strip()
            import json
            return json.loads(response)
        except:
             return {"intent": "informational", "content_type": "article", "difficulty": "medium"}

def get_seo_service():
    return SEOService()
