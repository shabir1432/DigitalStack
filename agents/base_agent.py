"""
Base Agent Class
Provides common functionality for all agents
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from rich.console import Console
from rich.panel import Panel

from core.llm import get_llm, MultiProviderLLM

console = Console()


class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.llm: MultiProviderLLM = get_llm()
    
    def log(self, message: str, level: str = "info"):
        """Log a message with agent context"""
        color_map = {
            "info": "blue",
            "success": "green",
            "warning": "yellow",
            "error": "red"
        }
        color = color_map.get(level, "white")
        console.print(f"[{color}][{self.name}] {message}[/{color}]")
    
    def log_start(self):
        """Log agent start"""
        console.print(Panel(
            f"[bold]{self.description}[/bold]",
            title=f"🤖 {self.name}",
            border_style="cyan"
        ))
    
    def log_complete(self, result: Any = None):
        """Log agent completion"""
        self.log("Task completed successfully", "success")
    
    @abstractmethod
    async def run(self, *args, **kwargs) -> Dict[str, Any]:
        """Run the agent's main task"""
        pass
    
    def validate_input(self, **kwargs) -> bool:
        """Validate input parameters"""
        return True
