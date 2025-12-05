"""Orchestrator for coordinating the Multi-Agent System workflow."""
from typing import Any, Dict, Optional
import pandas as pd
import numpy as np

from agents import (
    DataCollectorAgent,
    FeatureProcessorAgent,
    PredictionAgent,
    VisualizationAgent
)


class Orchestrator:
    """Orchestrates the workflow between different agents in the system.
    
    The orchestrator manages the coordination and data flow between agents,
    ensuring they work together to complete the entire pipeline.
    """
    
    def __init__(self):
        """Initialize the orchestrator and all agents."""
        self.data_collector = DataCollectorAgent()
        self.feature_processor = FeatureProcessorAgent()
        self.prediction_agent = PredictionAgent()
        self.visualization_agent = VisualizationAgent()
        
        self.data: Optional[pd.DataFrame] = None
        self.features: Optional[pd.DataFrame] = None
        self.target: Optional[pd.Series] = None
        self.predictions: Optional[np.ndarray] = None
        
        print("[Orchestrator] Multi-Agent System initialized")
    
    def run_pipeline(self, data_path: str, target_column: Optional[str] = None,
                    train_model: bool = True, visualize: bool = True,
                    save_visualization: Optional[str] = None) -> Dict[str, Any]:
        """Run the complete MAS pipeline.
        
        Args:
            data_path: Path to the CSV data file.
            target_column: Name of the target column for supervised learning.
            train_model: Whether to train a prediction model.
            visualize: Whether to create visualizations.
            save_visualization: Optional path to save the visualization.
            
        Returns:
            A dictionary containing the results of the pipeline.
        """
        print("\n[Orchestrator] Starting MAS pipeline...\n")
        
        # Step 1: Data Collection
        print("[Orchestrator] Step 1: Data Collection")
        self.data = self.data_collector.run(data_path)
        
        # Step 2: Feature Processing
        print("\n[Orchestrator] Step 2: Feature Processing")
        result = self.feature_processor.run(self.data, target_column)
        if isinstance(result, tuple):
            self.features, self.target = result
        else:
            self.features = result
        
        # Step 3: Prediction (if enabled)
        if train_model and self.target is not None:
            print("\n[Orchestrator] Step 3: Model Training and Prediction")
            self.predictions = self.prediction_agent.run(
                self.features, train=True, target=self.target
            )
        elif not train_model and self.prediction_agent.model is not None:
            print("\n[Orchestrator] Step 3: Making Predictions")
            self.predictions = self.prediction_agent.run(self.features, train=False)
        else:
            print("\n[Orchestrator] Step 3: Skipping prediction (no target or model)")
        
        # Step 4: Visualization (if enabled)
        if visualize:
            print("\n[Orchestrator] Step 4: Creating Visualizations")
            self.visualization_agent.run(
                self.data,
                predictions=self.predictions,
                target=self.target,
                save_path=save_visualization
            )
        
        print("\n[Orchestrator] Pipeline completed successfully!\n")
        
        # Return results
        results = {
            'data_shape': self.data.shape,
            'features_shape': self.features.shape,
            'has_predictions': self.predictions is not None,
        }
        
        if self.predictions is not None:
            results['num_predictions'] = len(self.predictions)
        
        return results
    
    def get_agent_states(self) -> Dict[str, Dict]:
        """Get the state of all agents.
        
        Returns:
            A dictionary mapping agent names to their states.
        """
        return {
            'data_collector': self.data_collector.state,
            'feature_processor': self.feature_processor.state,
            'prediction_agent': self.prediction_agent.state,
            'visualization_agent': self.visualization_agent.state,
        }
    
    def save_model(self, file_path: str) -> None:
        """Save the trained prediction model.
        
        Args:
            file_path: Path where to save the model.
        """
        self.prediction_agent.save_model(file_path)
    
    def load_model(self, file_path: str) -> None:
        """Load a trained prediction model.
        
        Args:
            file_path: Path to the saved model.
        """
        self.prediction_agent.load_model(file_path)
