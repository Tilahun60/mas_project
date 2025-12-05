"""Base agent class for the Multi-Agent System."""
from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgent(ABC):
    """Abstract base class for all agents in the system.
    
    All agents must inherit from this class and implement the run method.
    """
    
    def __init__(self, name: str):
        """Initialize the agent with a name.
        
        Args:
            name: The name identifier for this agent.
        """
        self.name = name
        self.state: Dict[str, Any] = {}
    
    @abstractmethod
    def run(self, data: Any) -> Any:
        """Execute the agent's main logic.
        
        Args:
            data: Input data for the agent to process.
            
        Returns:
            The processed output from the agent.
        """
        pass
    
    def log(self, message: str) -> None:
        """Log a message with the agent's name.
        
        Args:
            message: The message to log.
        """
        print(f"[{self.name}] {message}")
