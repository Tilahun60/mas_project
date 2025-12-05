"""Feature processing agent for feature engineering."""
import pandas as pd
import numpy as np
from typing import List, Optional, Union
from .base_agent import BaseAgent


class FeatureProcessorAgent(BaseAgent):
    """Agent responsible for feature engineering and transformation.
    
    This agent provides hooks for creating and processing features
    from the cleaned data.
    """
    
    def __init__(self, name: str = "FeatureProcessor"):
        """Initialize the FeatureProcessorAgent.
        
        Args:
            name: The name identifier for this agent.
        """
        super().__init__(name)
    
    def run(self, df: pd.DataFrame, target_column: Optional[str] = None) -> Union[pd.DataFrame, tuple]:
        """Process and engineer features from the data.
        
        Args:
            df: The input DataFrame to process.
            target_column: Optional name of the target column for supervised learning.
            
        Returns:
            A tuple of (features_df, target_series) if target_column is provided,
            otherwise just features_df.
        """
        self.log("Starting feature processing")
        
        # Store original columns
        original_columns = df.columns.tolist()
        self.log(f"Original features: {len(original_columns)} columns")
        
        # Separate features and target
        if target_column and target_column in df.columns:
            target = df[target_column]
            features = df.drop(columns=[target_column])
            self.log(f"Target column '{target_column}' separated")
        else:
            features = df.copy()
            target = None
        
        # Apply feature engineering
        features = self._engineer_features(features)
        
        self.log(f"Feature processing completed: {len(features.columns)} features")
        
        if target is not None:
            return features, target
        return features
    
    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply feature engineering transformations.
        
        This is a hook method that can be extended with custom
        feature engineering logic.
        
        Args:
            df: The DataFrame containing features.
            
        Returns:
            The DataFrame with engineered features.
        """
        processed_df = df.copy()
        
        # Identify numeric and categorical columns
        numeric_cols = processed_df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = processed_df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        self.log(f"Found {len(numeric_cols)} numeric and {len(categorical_cols)} categorical features")
        
        # Normalize numeric features (simple standardization)
        if numeric_cols:
            for col in numeric_cols:
                mean = processed_df[col].mean()
                std = processed_df[col].std()
                if std != 0:
                    processed_df[col] = (processed_df[col] - mean) / std
            self.log("Normalized numeric features")
        
        # Encode categorical features (using sklearn LabelEncoder for robustness)
        if categorical_cols:
            try:
                from sklearn.preprocessing import LabelEncoder
                for col in categorical_cols:
                    le = LabelEncoder()
                    processed_df[col] = le.fit_transform(processed_df[col].astype(str))
                self.log("Encoded categorical features using LabelEncoder")
            except ImportError:
                # Fallback to simple categorical codes if sklearn not available
                for col in categorical_cols:
                    processed_df[col] = pd.Categorical(processed_df[col]).codes
                self.log("Encoded categorical features using categorical codes")
        
        return processed_df
