"""
Orchestrator
Coordinates the Authority Blog System
"""
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from agents.trend_agent import TrendAgent
from agents.keyword_agent import KeywordAgent
from agents.writer_agent import WriterAgent
from agents.publisher_agent import PublisherAgent
from services.seo_service import get_seo_service
from config.settings import NICHES, validate_config

console = Console()

class Orchestrator:
    """Main orchestrator that coordinates all agents for Authority Blogging"""
    
    def __init__(self):
        self.trend_agent = TrendAgent()
        self.keyword_agent = KeywordAgent()
        self.writer_agent = WriterAgent()
        self.publisher_agent = PublisherAgent()
        self.seo_service = get_seo_service()
    
    async def run(
        self,
        auto_publish: bool = False
    ) -> Dict[str, Any]:
        """
        Run the daily authority blog cycle (3 posts: 1 per niche)
        """
        start_time = datetime.now()
        
        console.print(Panel(
            f"""[bold cyan]Authority Blog System (SEO Edition)[/bold cyan]
            
[yellow]Strategy:[/yellow] 3 High-Quality Posts/Day
[yellow]Niches:[/yellow] {", ".join([n['name'] for n in NICHES])}
[yellow]Auto-publish:[/yellow] {auto_publish}
[yellow]Started:[/yellow] {start_time.strftime('%Y-%m-%d %H:%M:%S')}""",
            title="🚀 Starting Daily Cycle",
            border_style="green"
        ))
        
        results = []
        
        try:
            validate_config()
            
            # Loop through each niche and generate a post
            for niche in NICHES:
                console.print(f"\n[magenta]==========================================[/magenta]")
                console.print(f"[bold magenta]🎲 Starting Niche: {niche['name']}[/bold magenta]")
                console.print(f"[magenta]==========================================[/magenta]\n")
                
                try:
                    result = await self._process_niche(niche, auto_publish)
                    results.append(result)
                    
                    # 6. Traffic Acceleration Tips (Post-Processing)
                    self._display_traffic_tips(result)
                    
                except Exception as e:
                    console.print(f"[red]❌ Error processing niche {niche['name']}: {e}[/red]")
            
            return {"results": results}
            
        except Exception as e:
            console.print(f"\n[red]❌ Critical Error: {e}[/red]")
            raise

    async def _process_niche(self, niche: Dict[str, Any], auto_publish: bool) -> Dict[str, Any]:
        """Process a single niche through the SEO workflow"""
        
        # 1. Trend Research & Selection
        console.print(f"[cyan]🔍 Stage 1: Trend Research ({niche['name']})[/cyan]")
        trend_result = await self.trend_agent.run(niche=niche, count=5)
        topic = trend_result["selected_topic"]
        
        # 2. SEO Analysis (Intent & Competitor Gaps)
        console.print(f"[cyan]🧠 Stage 2: SEO Analysis & Intent[/cyan]")
        intent_analysis = self.seo_service.analyze_search_intent(topic)
        console.print(f"   Intent: [yellow]{intent_analysis.get('intent', 'unknown')}[/yellow]")
        console.print(f"   Difficulty: [yellow]{intent_analysis.get('difficulty', 'medium')}[/yellow]")
        
        # 3. Ranking Blueprint Generation
        console.print(f"[cyan]📐 Stage 3: Generatin Ranking Blueprint[/cyan]")
        blueprint = self.seo_service.generate_ranking_blueprint(topic)
        console.print(f"   Target Word Count: [green]{blueprint.get('target_word_count')}[/green]")
        console.print(f"   H1: [green]{blueprint.get('h1')}[/green]")

        # 4. Keyword Enhancement
        console.print(f"[cyan]🏷️ Stage 4: Keyword Strategy[/cyan]")
        keyword_result = await self.keyword_agent.run(
            topic=topic,
            niche=niche['name'],
            analysis=trend_result.get("analysis")
        )
        # Merge Blueprint LSI keywords
        keyword_result['lsi'] = list(set(keyword_result.get('lsi', []) + blueprint.get('lsi_keywords', [])))
        
        # 5. Authority Writing
        console.print(f"[cyan]✍️ Stage 5: Authority Writing (E-E-A-T)[/cyan]")
        writer_result = await self.writer_agent.run(
            topic=topic,
            keywords=keyword_result,
            niche=niche['name'],
            blueprint=blueprint
        )
        
        # 6. Publishing
        console.print(f"[cyan]📤 Stage 6: Publishing[/cyan]")
        publish_result = await self.publisher_agent.run(
            blog_post=writer_result,
            auto_publish=auto_publish
        )
        
        return {
            "niche": niche['name'],
            "topic": topic,
            "blueprint": blueprint,
            "writer_result": writer_result,
            "publish_result": publish_result
        }

    def _display_traffic_tips(self, result: Dict[str, Any]):
        """Show manual tips for the user to boost this post"""
        topic = result['topic']
        tips = f"""
[bold green]🚀 Traffic Acceleration Tips for "{topic}"[/bold green]
1. [bold]Internal Linking:[/bold] Search your blog for "{result['blueprint'].get('lsi_keywords', ['tags'])[0]}" and link to this new post.
2. [bold]Social:[/bold] Tweet the "Key Takeaways" section as a thread.
3. [bold]Email:[/bold] Send the "Why this matters now" angle to your list.
"""
        console.print(Panel(tips, title="📢 Promote This Post", border_style="blue"))

async def run_orchestrator(auto_publish: bool = False) -> Dict[str, Any]:
    orchestrator = Orchestrator()
    return await orchestrator.run(auto_publish=auto_publish)
