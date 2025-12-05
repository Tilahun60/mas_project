"""Prediction agent for machine learning model integration."""
import numpy as np
import pandas as pd
from typing import Any, Optional
from .base_agent import BaseAgent


class PredictionAgent(BaseAgent):
    """Agent responsible for making predictions using ML/transformer models.
    
    This agent is prepared for integration with scikit-learn and PyTorch models.
    """
    
    def __init__(self, name: str = "PredictionAgent"):
        """Initialize the PredictionAgent.
        
        Args:
            name: The name identifier for this agent.
        """
        super().__init__(name)
        self.model: Optional[Any] = None
        self.model_type: Optional[str] = None
    
    def run(self, features: pd.DataFrame, train: bool = False, 
            target: Optional[pd.Series] = None) -> np.ndarray:
        """Make predictions or train a model.
        
        Args:
            features: The feature DataFrame for prediction or training.
            train: Whether to train the model (requires target).
            target: The target values for training.
            
        Returns:
            Predictions as a numpy array.
        """
        if train:
            if target is None:
                raise ValueError("Target is required for training")
            return self._train_model(features, target)
        else:
            return self._predict(features)
    
    def _train_model(self, features: pd.DataFrame, target: pd.Series) -> np.ndarray:
        """Train a machine learning model.
        
        This is a placeholder that can be extended with actual model training.
        
        Args:
            features: Training features.
            target: Training targets.
            
        Returns:
            Training predictions.
        """
        self.log("Training model...")
        
        try:
            from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
            from sklearn.model_selection import train_test_split
            
            # Determine if this is a classification or regression task
            unique_targets = target.nunique()
            is_classification = unique_targets < 20  # Simple heuristic
            
            if is_classification:
                self.model = RandomForestClassifier(n_estimators=100, random_state=42)
                self.model_type = "classification"
                self.log(f"Using RandomForestClassifier ({unique_targets} classes)")
            else:
                self.model = RandomForestRegressor(n_estimators=100, random_state=42)
                self.model_type = "regression"
                self.log("Using RandomForestRegressor")
            
            # Train the model
            self.model.fit(features, target)
            self.log("Model training completed")
            
            # Return training predictions
            predictions = self.model.predict(features)
            return predictions
            
        except ImportError:
            self.log("scikit-learn not available, using dummy predictions")
            return np.zeros(len(features))
    
    def _predict(self, features: pd.DataFrame) -> np.ndarray:
        """Make predictions using the trained model.
        
        Args:
            features: Features for prediction.
            
        Returns:
            Model predictions.
        """
        if self.model is None:
            self.log("No trained model available, returning dummy predictions")
            return np.zeros(len(features))
        
        self.log("Making predictions...")
        predictions = self.model.predict(features)
        self.log(f"Generated {len(predictions)} predictions")
        
        return predictions
    
    def save_model(self, file_path: str) -> None:
        """Save the trained model to disk.
        
        Args:
            file_path: Path where to save the model.
        """
        if self.model is None:
            self.log("No model to save")
            return
        
        try:
            import joblib
            joblib.dump(self.model, file_path)
            self.log(f"Model saved to {file_path}")
        except ImportError:
            self.log("joblib not available, cannot save model")
    
    def load_model(self, file_path: str) -> None:
        """Load a trained model from disk.
        
        Args:
            file_path: Path to the saved model.
        """
        try:
            import joblib
            self.model = joblib.load(file_path)
            self.log(f"Model loaded from {file_path}")
        except ImportError:
            self.log("joblib not available, cannot load model")
        except Exception as e:
            self.log(f"Error loading model: {str(e)}")
