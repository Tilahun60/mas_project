#!/usr/bin/env python
"""
Test script to verify the Multi-Agent System works correctly.
This script runs a basic end-to-end test of the MAS pipeline.
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orchestrator import Orchestrator


def test_basic_pipeline():
    """Test the basic pipeline with sample data."""
    print("Testing Multi-Agent System Pipeline")
    print("=" * 60)
    
    # Initialize orchestrator
    orchestrator = Orchestrator()
    
    # Run pipeline with sample data
    data_path = "data/sample_data.csv"
    
    if not os.path.exists(data_path):
        print(f"ERROR: Sample data not found at {data_path}")
        return False
    
    try:
        results = orchestrator.run_pipeline(
            data_path=data_path,
            target_column="target",
            train_model=True,
            visualize=True,
            save_visualization="test_visualization.png"
        )
        
        # Verify results
        assert results['data_shape'][0] > 0, "No data loaded"
        assert results['features_shape'][1] > 0, "No features processed"
        assert results['has_predictions'], "No predictions generated"
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        print(f"  - Loaded {results['data_shape'][0]} rows of data")
        print(f"  - Processed {results['features_shape'][1]} features")
        print(f"  - Generated {results['num_predictions']} predictions")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_basic_pipeline()
    sys.exit(0 if success else 1)
