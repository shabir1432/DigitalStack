"""
Authority Blog System
Main entry point for running the daily 3-niche cycle
"""
import asyncio
import argparse
from rich.console import Console
from agents.orchestrator import run_orchestrator

console = Console()

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Authority AI Blog System - runs the daily 3-niche cycle"
    )
    
    parser.add_argument(
        "--publish",
        "-p",
        action="store_true",
        help="Automatically publish the posts to the website (default: save as drafts)"
    )
    
    return parser.parse_args()

async def main():
    """Main entry point"""
    args = parse_args()
    
    try:
        console.print("[bold green]🚀 Authority Blog System Initialized[/bold green]")
        if args.publish:
            console.print("[red]⚠️ AUTO-PUBLISH ENABLED - Posts will go live immediately[/red]")
        else:
            console.print("[yellow]📝 DRAFT MODE - Posts will be saved to content/posts for review[/yellow]")
        
        await run_orchestrator(auto_publish=args.publish)
        
        console.print("\n[bold green]✅ Daily Cycle Completed Successfully![/bold green]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️ Operation cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Critical Error: {e}[/red]")
        # import traceback
        # traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
