"""Visualization agent for plotting data and predictions."""
import numpy as np
import pandas as pd
from typing import Optional
from .base_agent import BaseAgent


class VisualizationAgent(BaseAgent):
    """Agent responsible for creating visualizations using matplotlib.
    
    This agent plots data distributions, predictions, and model results.
    """
    
    def __init__(self, name: str = "VisualizationAgent"):
        """Initialize the VisualizationAgent.
        
        Args:
            name: The name identifier for this agent.
        """
        super().__init__(name)
    
    def run(self, data: pd.DataFrame, predictions: Optional[np.ndarray] = None,
            target: Optional[pd.Series] = None, save_path: Optional[str] = None) -> None:
        """Create visualizations for data and predictions.
        
        Args:
            data: The DataFrame to visualize.
            predictions: Optional model predictions to plot.
            target: Optional target values to plot.
            save_path: Optional path to save the plot.
        """
        self.log("Creating visualizations...")
        
        try:
            import matplotlib.pyplot as plt
            
            # Determine the number of subplots needed
            num_plots = 1
            if predictions is not None:
                num_plots += 1
            if target is not None and predictions is not None:
                num_plots += 1
            
            fig, axes = plt.subplots(1, num_plots, figsize=(6 * num_plots, 5))
            if num_plots == 1:
                axes = [axes]
            
            plot_idx = 0
            
            # Plot 1: Data distribution
            self._plot_data_distribution(data, axes[plot_idx])
            plot_idx += 1
            
            # Plot 2: Predictions distribution (if available)
            if predictions is not None:
                self._plot_predictions(predictions, axes[plot_idx])
                plot_idx += 1
            
            # Plot 3: Predictions vs Actual (if both available)
            if predictions is not None and target is not None:
                self._plot_predictions_vs_actual(predictions, target, axes[plot_idx])
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                self.log(f"Visualization saved to {save_path}")
            else:
                plt.savefig('visualization.png', dpi=300, bbox_inches='tight')
                self.log("Visualization saved to visualization.png")
            
            plt.close()
            
        except ImportError:
            self.log("matplotlib not available, skipping visualization")
        except Exception as e:
            self.log(f"Error creating visualization: {str(e)}")
    
    def _plot_data_distribution(self, data: pd.DataFrame, ax) -> None:
        """Plot the distribution of numeric features in the data.
        
        Args:
            data: The DataFrame to visualize.
            ax: The matplotlib axis to plot on.
        """
        import matplotlib.pyplot as plt
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            # Plot the first numeric column as a histogram
            first_col = numeric_cols[0]
            ax.hist(data[first_col].dropna(), bins=30, edgecolor='black', alpha=0.7)
            ax.set_title(f'Distribution of {first_col}')
            ax.set_xlabel(first_col)
            ax.set_ylabel('Frequency')
            ax.grid(True, alpha=0.3)
        else:
            ax.text(0.5, 0.5, 'No numeric features', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Data Distribution')
    
    def _plot_predictions(self, predictions: np.ndarray, ax) -> None:
        """Plot the distribution of predictions.
        
        Args:
            predictions: The predictions array.
            ax: The matplotlib axis to plot on.
        """
        ax.hist(predictions, bins=30, edgecolor='black', alpha=0.7, color='orange')
        ax.set_title('Predictions Distribution')
        ax.set_xlabel('Predicted Value')
        ax.set_ylabel('Frequency')
        ax.grid(True, alpha=0.3)
    
    def _plot_predictions_vs_actual(self, predictions: np.ndarray, 
                                    target: pd.Series, ax) -> None:
        """Plot predictions versus actual values.
        
        Args:
            predictions: The predictions array.
            target: The actual target values.
            ax: The matplotlib axis to plot on.
        """
        ax.scatter(target, predictions, alpha=0.5, edgecolor='black')
        
        # Plot diagonal line (perfect predictions)
        min_val = min(target.min(), predictions.min())
        max_val = max(target.max(), predictions.max())
        ax.plot([min_val, max_val], [min_val, max_val], 
               'r--', linewidth=2, label='Perfect Prediction')
        
        ax.set_title('Predictions vs Actual')
        ax.set_xlabel('Actual Value')
        ax.set_ylabel('Predicted Value')
        ax.legend()
        ax.grid(True, alpha=0.3)
