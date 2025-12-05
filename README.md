# Multi-Agent System (MAS) Project

A flexible and extensible Multi-Agent System for data processing, feature engineering, machine learning predictions, and visualization.

## Architecture

This MAS follows a modular architecture where specialized agents collaborate to process data through a complete machine learning pipeline. The system is coordinated by an orchestrator that manages the workflow and data flow between agents.

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                       Orchestrator                          │
│              (Workflow Coordination & Management)           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ├─────────────────┐
                              ▼                 ▼
                    ┌─────────────────┐  ┌─────────────────┐
                    │ DataCollector   │  │FeatureProcessor │
                    │    Agent        │  │     Agent       │
                    └─────────────────┘  └─────────────────┘
                              │                 │
                              ├─────────────────┘
                              ▼
                    ┌─────────────────┐
                    │  Prediction     │
                    │     Agent       │
                    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Visualization   │
                    │     Agent       │
                    └─────────────────┘
```

## Agent Roles

### 1. BaseAgent (Abstract Base Class)
- **Purpose**: Defines the interface that all agents must implement
- **Key Features**:
  - Abstract `run()` method that all agents must implement
  - State management for each agent
  - Logging functionality with agent identification

### 2. DataCollectorAgent
- **Purpose**: Handles data ingestion and basic preprocessing
- **Responsibilities**:
  - Load CSV data files
  - Remove duplicate rows
  - Handle missing values
  - Basic data cleaning operations
- **Input**: File path to CSV data
- **Output**: Cleaned pandas DataFrame

### 3. FeatureProcessorAgent
- **Purpose**: Performs feature engineering and transformation
- **Responsibilities**:
  - Separate features from target variable
  - Normalize numeric features (standardization)
  - Encode categorical features (label encoding)
  - Extensible feature engineering hooks
- **Input**: Cleaned DataFrame
- **Output**: Processed features DataFrame and optional target Series

### 4. PredictionAgent
- **Purpose**: Handles machine learning model training and inference
- **Responsibilities**:
  - Train models (Random Forest by default)
  - Make predictions
  - Save and load trained models
  - Support for both classification and regression
- **Input**: Feature DataFrame and optional target for training
- **Output**: Predictions as numpy array
- **Models Supported**: 
  - Scikit-learn (Random Forest, extensible to others)
  - PyTorch (prepared for integration)

### 5. VisualizationAgent
- **Purpose**: Creates visual representations of data and results
- **Responsibilities**:
  - Plot data distributions
  - Visualize prediction distributions
  - Compare predictions vs actual values
  - Save plots to disk
- **Input**: Data, predictions, and target values
- **Output**: Visualization plots (saved as PNG)

### 6. Orchestrator
- **Purpose**: Coordinates the entire MAS workflow
- **Responsibilities**:
  - Initialize all agents
  - Manage data flow between agents
  - Execute the complete pipeline
  - Provide access to intermediate results
  - Handle model persistence

## Project Structure

```
mas_project/
│
├── agents/                      # Agent implementations
│   ├── __init__.py             # Package initialization
│   ├── base_agent.py           # Abstract base class
│   ├── data_collector.py       # Data loading and cleaning
│   ├── feature_processor.py    # Feature engineering
│   ├── prediction_agent.py     # ML model training and prediction
│   └── visualization_agent.py  # Data and result visualization
│
├── data/                        # Dataset storage
│   └── sample_data.csv         # Example dataset for testing
│
├── models/                      # Trained model storage
│
├── orchestrator.py             # System coordination and workflow
├── main.py                     # CLI entry point for running the pipeline
├── webapp.py                   # Web interface (Streamlit dashboard)
├── test_pipeline.py            # Test script to verify the system works
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mas_project
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

The repository includes a sample dataset to help you get started immediately:

```bash
# Run with the included sample data
python main.py
```

This will:
- Load the sample dataset (`data/sample_data.csv`)
- Train a Random Forest classifier
- Generate predictions
- Create visualizations
- Save the trained model

You can also run the test script to verify everything works:

```bash
python test_pipeline.py
```

### Web Interface (Recommended for Beginners)

Launch the interactive web dashboard to explore the MAS visually:

```bash
streamlit run webapp.py
```

This will open a web browser with an interactive dashboard where you can:
- 📊 Upload your own CSV files or use sample data
- ⚙️ Configure pipeline parameters through the UI
- 🚀 Run the complete MAS pipeline with one click
- 📈 View real-time results, predictions, and visualizations
- 📥 Download predictions and processed data

**Features:**
- No coding required - point and click interface
- Real-time pipeline execution logs
- Interactive data preview and statistics
- Automatic visualization generation
- Download results in CSV format

### Basic Usage

1. **Prepare your data**:
   - Place your CSV data file in the `data/` directory
   - Example: `data/sample_data.csv`

2. **Update configuration** (in `main.py`):
   ```python
   data_path = "data/your_data.csv"
   target_column = "your_target_column"  # or None for unsupervised
   ```

3. **Run the pipeline**:
   ```bash
   python main.py
   ```

### Advanced Usage

#### Using the Orchestrator Directly

```python
from orchestrator import Orchestrator

# Initialize
orchestrator = Orchestrator()

# Run pipeline with custom settings
results = orchestrator.run_pipeline(
    data_path="data/my_data.csv",
    target_column="target",
    train_model=True,
    visualize=True,
    save_visualization="results/my_plot.png"
)

# Save the trained model
orchestrator.save_model("models/my_model.pkl")

# Load a previously trained model
orchestrator.load_model("models/my_model.pkl")
```

#### Using Individual Agents

```python
from agents import DataCollectorAgent, FeatureProcessorAgent

# Use agents independently
data_agent = DataCollectorAgent()
df = data_agent.run("data/sample.csv")

feature_agent = FeatureProcessorAgent()
features, target = feature_agent.run(df, target_column="label")
```

### Pipeline Output

The pipeline generates:
- **Console logs**: Detailed progress information from each agent
- **Visualization**: PNG file showing data distribution, predictions, and comparisons
- **Trained model**: Saved in the `models/` directory (if training is enabled)
- **Results dictionary**: Contains pipeline execution summary

## Customization

### Extending the System

1. **Create custom agents**: Inherit from `BaseAgent` and implement the `run()` method
2. **Custom feature engineering**: Override `_engineer_features()` in `FeatureProcessorAgent`
3. **Different ML models**: Modify `_train_model()` in `PredictionAgent`
4. **Additional visualizations**: Add methods to `VisualizationAgent`

### Example: Custom Agent

```python
from agents.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self, name="CustomAgent"):
        super().__init__(name)
    
    def run(self, data):
        self.log("Processing data...")
        # Your custom logic here
        return processed_data
```

## Dependencies

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **matplotlib**: Data visualization
- **scikit-learn**: Machine learning models and tools
- **torch**: Deep learning framework (prepared for future integration)

## Future Enhancements

- [ ] Support for more data formats (JSON, Parquet, databases)
- [ ] Advanced feature engineering techniques
- [ ] Deep learning model integration with PyTorch
- [ ] Hyperparameter optimization
- [ ] Cross-validation and model evaluation metrics
- [ ] Agent communication protocols
- [ ] Distributed processing capabilities
- [ ] REST API for remote agent invocation

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available under the MIT License.

## Contact

For questions or support, please open an issue on the repository. 
