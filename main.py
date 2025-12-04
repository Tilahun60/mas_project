"""Main entry point for the Multi-Agent System.

This script demonstrates how to use the MAS for data processing,
feature engineering, prediction, and visualization.
"""
import os
import sys
from orchestrator import Orchestrator


def main():
    """Run the Multi-Agent System pipeline."""
    print("=" * 60)
    print("Multi-Agent System (MAS) for Data Processing and ML")
    print("=" * 60)
    
    # Initialize the orchestrator
    orchestrator = Orchestrator()
    
    # Example usage with a sample dataset
    # You can replace this with your own data path
    data_path = "data/sample_data.csv"
    
    # Check if sample data exists
    if not os.path.exists(data_path):
        print(f"\n[Main] Sample data not found at {data_path}")
        print("[Main] Please place your CSV data file in the 'data/' directory")
        print("[Main] and update the data_path variable in main.py")
        print("\n[Main] Example usage:")
        print("  1. Place your CSV file in data/ directory")
        print("  2. Update data_path in main.py")
        print("  3. Optionally set target_column for supervised learning")
        print("  4. Run: python main.py")
        return 1
    
    # Define the target column (for supervised learning)
    # Set to None for unsupervised tasks
    target_column = "target"  # e.g., "target" or "label"
    
    try:
        # Run the complete pipeline
        results = orchestrator.run_pipeline(
            data_path=data_path,
            target_column=target_column,
            train_model=True if target_column else False,
            visualize=True,
            save_visualization="visualization.png"
        )
        
        # Display results
        print("[Main] Pipeline Results:")
        print(f"  - Data shape: {results['data_shape']}")
        print(f"  - Features shape: {results['features_shape']}")
        print(f"  - Predictions generated: {results['has_predictions']}")
        if results['has_predictions']:
            print(f"  - Number of predictions: {results['num_predictions']}")
        
        # Optionally save the trained model
        if results['has_predictions']:
            model_path = "models/trained_model.pkl"
            os.makedirs("models", exist_ok=True)
            orchestrator.save_model(model_path)
            print(f"\n[Main] Model saved to {model_path}")
        
        print("\n" + "=" * 60)
        print("Pipeline execution completed successfully!")
        print("=" * 60)
        
        return 0
        
    except Exception as e:
        print(f"\n[Main] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
