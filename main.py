"""
Agentic AI Blog System
Main entry point for running the automated blog posting system
"""
import asyncio
import argparse
from rich.console import Console

from agents.orchestrator import run_orchestrator
from config.settings import BLOG_NICHE

console = Console()


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Agentic AI Blog System - Automated blog posting with AI agents"
    )
    
    parser.add_argument(
        "--topic",
        "-t",
        type=str,
        default=None,
        help="Specific topic to write about (optional, auto-detected from trends if not provided)"
    )
    
    parser.add_argument(
        "--niche",
        "-n",
        type=str,
        default=None,
        help=f"Blog niche (default: {BLOG_NICHE})"
    )
    
    parser.add_argument(
        "--trending",
        action="store_true",
        help="Write about ANY trending topic (ignores niche filter)"
    )
    
    parser.add_argument(
        "--publish",
        "-p",
        action="store_true",
        help="Automatically publish the post (default: save as draft)"
    )
    
    parser.add_argument(
        "--dry-run",
        "-d",
        action="store_true",
        help="Run without saving or publishing (for testing)"
    )
    
    return parser.parse_args()


async def main():
    """Main entry point"""
    args = parse_args()
    
    try:
        if args.dry_run:
            console.print("[yellow]🧪 Dry run mode - no files will be saved[/yellow]\n")
        
        if args.trending:
            console.print("[bold magenta]🔥 TRENDING MODE: Writing about ANY trending topic (no niche filter)[/bold magenta]\n")
        
        # If --trending flag is used, set niche to None to skip filtering
        niche = None if args.trending else args.niche
        
        result = await run_orchestrator(
            topic=args.topic,
            niche=niche,
            auto_publish=args.publish,
            use_any_trending=args.trending
        )
        
        console.print("\n[green]✅ Blog generation completed successfully![/green]")
        return result
        
    except ValueError as e:
        console.print(f"\n[red]❌ Configuration error: {e}[/red]")
        console.print("[yellow]Please check your .env file and ensure all required API keys are set.[/yellow]")
        return None
        
    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/red]")
        raise


if __name__ == "__main__":
    asyncio.run(main())
