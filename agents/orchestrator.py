"""
Orchestrator
Coordinates all agents to produce a complete blog post
"""
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from agents.trend_agent import TrendAgent
from agents.keyword_agent import KeywordAgent
from agents.writer_agent import WriterAgent
from agents.publisher_agent import PublisherAgent
from config.settings import BLOG_NICHE, validate_config

console = Console()


class Orchestrator:
    """Main orchestrator that coordinates all agents"""
    
    def __init__(self):
        self.trend_agent = TrendAgent()
        self.keyword_agent = KeywordAgent()
        self.writer_agent = WriterAgent()
        self.publisher_agent = PublisherAgent()
    
    async def run(
        self,
        topic: Optional[str] = None,
        niche: Optional[str] = None,
        auto_publish: bool = False,
        use_any_trending: bool = False
    ) -> Dict[str, Any]:
        """
        Run the complete blog post generation pipeline
        
        Args:
            topic: Optional specific topic (otherwise fetched from trends)
            niche: Blog niche (uses config if not provided)
            auto_publish: Whether to publish automatically
            use_any_trending: If True, write about ANY trending topic (no niche filter)
            
        Returns:
            Complete result with all agent outputs
        """
        start_time = datetime.now()
        
        # If use_any_trending, don't filter by niche
        if use_any_trending:
            niche = None
            display_niche = "🔥 ANY TRENDING TOPIC"
        else:
            niche = niche or BLOG_NICHE
            display_niche = niche
        
        # Display header
        console.print(Panel(
            f"""[bold cyan]Agentic AI Blog System[/bold cyan]
            
[yellow]Mode:[/yellow] {'🔥 Trending Mode (Any Topic)' if use_any_trending else 'Niche Mode'}
[yellow]Niche:[/yellow] {display_niche}
[yellow]Topic:[/yellow] {topic or 'Auto-detect from global trends'}
[yellow]Auto-publish:[/yellow] {auto_publish}
[yellow]Started:[/yellow] {start_time.strftime('%Y-%m-%d %H:%M:%S')}""",
            title="🚀 Starting Blog Generation",
            border_style="green"
        ))
        
        try:
            # Validate configuration
            validate_config()
            
            result = {
                "started_at": start_time.isoformat(),
                "niche": niche or "any",
                "mode": "trending" if use_any_trending else "niche",
                "stages": {}
            }
            
            # Stage 1: Trend Research (skip if topic provided)
            if topic:
                console.print("\n[cyan]📌 Using provided topic, skipping trend research[/cyan]")
                trend_result = {
                    "selected_topic": topic,
                    "analysis": {"suggested_title": topic},
                    "niche": niche or "any"
                }
            else:
                console.print("\n[cyan]🔍 Stage 1: Global Trend Research[/cyan]")
                
                if use_any_trending:
                    # Get TOP trending topic globally - no niche filter
                    trend_result = await self._get_any_trending_topic()
                else:
                    trend_result = await self.trend_agent.run(niche=niche)
                
                topic = trend_result["selected_topic"]
            
            result["stages"]["trend_research"] = trend_result
            result["topic"] = topic
            console.print(f"[green]✓ Selected topic: {topic}[/green]\n")
            
            # Stage 2: Keyword Analysis
            console.print("[cyan]🏷️ Stage 2: Keyword Analysis[/cyan]")
            keyword_result = await self.keyword_agent.run(
                topic=topic,
                niche=niche or "general",
                analysis=trend_result.get("analysis")
            )
            
            # Format keywords for writer
            keywords_for_writer = self.keyword_agent.format_for_writer(keyword_result)
            result["stages"]["keyword_analysis"] = keyword_result
            console.print(f"[green]✓ Generated {len(keywords_for_writer.get('hashtags', []))} hashtags[/green]\n")
            
            # Stage 3: Content Writing
            console.print("[cyan]✍️ Stage 3: Content Writing[/cyan]")
            writer_result = await self.writer_agent.run(
                topic=topic,
                keywords=keywords_for_writer,
                niche=niche or "general"
            )
            result["stages"]["content_writing"] = {
                "title": writer_result.get("title"),
                "word_count": writer_result.get("word_count"),
                "images_count": len(writer_result.get("images", [])),
                "videos_count": len(writer_result.get("videos", []))
            }
            console.print(f"[green]✓ Written {writer_result.get('word_count', 0)} words[/green]\n")
            
            # Stage 4: Publishing
            console.print("[cyan]📤 Stage 4: Publishing[/cyan]")
            publish_result = await self.publisher_agent.run(
                blog_post=writer_result,
                auto_publish=auto_publish
            )
            result["stages"]["publishing"] = publish_result
            console.print(f"[green]✓ Post saved successfully[/green]\n")
            
            # Calculate duration
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            result["completed_at"] = end_time.isoformat()
            result["duration_seconds"] = duration
            
            # Display summary
            self._display_summary(result, writer_result, publish_result)
            
            return result
            
        except Exception as e:
            console.print(f"\n[red]❌ Error: {e}[/red]")
            raise
    
    async def _get_any_trending_topic(self) -> Dict[str, Any]:
        """
        Get the TOP trending topic globally without any niche filter.
        This picks the #1 most popular topic across all countries.
        """
        from services.google_trends import get_trends_service
        from services.competition_analyzer import get_competition_analyzer
        from services.topic_scorer import get_topic_scorer
        
        trends_service = get_trends_service()
        competition_analyzer = get_competition_analyzer()
        topic_scorer = get_topic_scorer()
        
        # Get global trends (no niche filter)
        console.print("[magenta]🔥 Fetching TOP trending topics globally (no niche filter)...[/magenta]")
        global_trends = trends_service.get_global_trends()
        
        if not global_trends:
            raise ValueError("No trending topics found")
        
        # Score top 10 trends
        scored_topics = []
        for trend in global_trends[:10]:
            competition = competition_analyzer.analyze_competition(
                trend['topic'],
                trend_data=trend
            )
            scored = topic_scorer.score_topic(
                topic=trend['topic'],
                regions=trend.get('regions', []),
                competition_data=competition,
                trend_data=trend
            )
            scored_topics.append(scored)
        
        # Display rankings
        topic_scorer.display_rankings(scored_topics)
        
        # Get best topic
        best = topic_scorer.get_best_topic(scored_topics)
        
        if not best:
            best = scored_topics[0]
        
        console.print(f"[bold green]🏆 Selected: {best['topic']} (Score: {best['final_score']:.1f})[/bold green]")
        
        return {
            "selected_topic": best['topic'],
            "original_trend": best['topic'],
            "score": best['final_score'],
            "priority": best['priority'],
            "competition_level": best['metrics']['competition_level'],
            "regions": best['metrics'].get('regions', []),
            "regions_count": best['metrics']['regions_count'],
            "analysis": {
                "suggested_title": best['topic'],
                "reason": f"Top trending topic in {best['metrics']['regions_count']} countries",
                "content_type": "news"
            },
            "niche": "trending"
        }
    
    def _display_summary(
        self,
        result: Dict[str, Any],
        writer_result: Dict[str, Any],
        publish_result: Dict[str, Any]
    ):
        """Display a summary of the completed pipeline"""
        
        duration = result.get("duration_seconds", 0)
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        
        mode_text = "🔥 Trending" if result.get("mode") == "trending" else f"📁 {result.get('niche', 'N/A')}"
        
        summary = f"""[bold green]✅ Blog Post Generated Successfully![/bold green]

[yellow]Mode:[/yellow] {mode_text}
[yellow]Topic:[/yellow] {result.get('topic', 'N/A')}
[yellow]Title:[/yellow] {writer_result.get('title', 'N/A')}
[yellow]Word Count:[/yellow] {writer_result.get('word_count', 0)}
[yellow]Images:[/yellow] {len(writer_result.get('images', []))}
[yellow]Videos:[/yellow] {len(writer_result.get('videos', []))}

[yellow]Draft Path:[/yellow] {publish_result.get('draft_path', 'N/A')}
[yellow]Published:[/yellow] {'Yes' if publish_result.get('auto_published') else 'No (saved as draft)'}
{f"[yellow]Post URL:[/yellow] {publish_result.get('post_url')}" if publish_result.get('post_url') else ''}

[yellow]Duration:[/yellow] {minutes}m {seconds}s"""

        console.print(Panel(
            summary,
            title="📊 Summary",
            border_style="green"
        ))


async def run_orchestrator(
    topic: Optional[str] = None,
    niche: Optional[str] = None,
    auto_publish: bool = False,
    use_any_trending: bool = False
) -> Dict[str, Any]:
    """Convenience function to run the orchestrator"""
    orchestrator = Orchestrator()
    return await orchestrator.run(
        topic=topic,
        niche=niche,
        auto_publish=auto_publish,
        use_any_trending=use_any_trending
    )
