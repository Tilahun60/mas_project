"""Data collection agent for loading and cleaning CSV data."""
import pandas as pd
from typing import Optional
from .base_agent import BaseAgent


class DataCollectorAgent(BaseAgent):
    """Agent responsible for loading and cleaning CSV data.
    
    This agent handles data ingestion and basic preprocessing tasks.
    """
    
    def __init__(self, name: str = "DataCollector"):
        """Initialize the DataCollectorAgent.
        
        Args:
            name: The name identifier for this agent.
        """
        super().__init__(name)
    
    def run(self, file_path: str) -> pd.DataFrame:
        """Load and clean CSV data.
        
        Args:
            file_path: Path to the CSV file to load.
            
        Returns:
            A cleaned pandas DataFrame.
        """
        self.log(f"Loading data from {file_path}")
        
        try:
            # Load the CSV file
            df = pd.read_csv(file_path)
            self.log(f"Loaded {len(df)} rows and {len(df.columns)} columns")
            
            # Basic cleaning
            df = self._clean_data(df)
            
            self.log("Data cleaning completed")
            return df
            
        except Exception as e:
            self.log(f"Error loading data: {str(e)}")
            raise
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Perform basic data cleaning operations.
        
        Args:
            df: The DataFrame to clean.
            
        Returns:
            The cleaned DataFrame.
        """
        # Remove duplicate rows
        initial_rows = len(df)
        df = df.drop_duplicates()
        if len(df) < initial_rows:
            self.log(f"Removed {initial_rows - len(df)} duplicate rows")
        
        # Handle missing values - drop rows with any missing values
        if df.isnull().any().any():
            missing_count = df.isnull().sum().sum()
            self.log(f"Found {missing_count} missing values")
            df = df.dropna()
            self.log(f"Dropped rows with missing values, {len(df)} rows remaining")
        
        return df
