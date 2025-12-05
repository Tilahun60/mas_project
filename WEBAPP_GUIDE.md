# Web Interface Quick Start Guide

## Running the Web Dashboard

The Multi-Agent System includes an interactive web interface built with Streamlit.

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Launch the Web App

```bash
streamlit run webapp.py
```

The app will automatically open in your default web browser at `http://localhost:8501`

### 3. Using the Dashboard

#### Data Source
- **Use Sample Data**: Automatically loads the included `sample_data.csv`
- **Upload CSV File**: Upload your own CSV file for analysis

#### Configuration (Sidebar)
1. Select your data source
2. Choose a target column (for supervised learning)
3. Enable/disable options:
   - Train ML Model
   - Create Visualizations

#### Tabs

**📊 Data Preview**
- View your dataset
- See column types and statistics
- Preview first 20 rows

**🚀 Run Pipeline**
- Click "Execute Pipeline" button
- Watch real-time logs
- See execution status

**📈 Results**
- View pipeline metrics
- Examine processed data and features
- Download predictions as CSV
- View generated visualizations

**ℹ️ About**
- Learn about the MAS architecture
- Understand each agent's role
- Get usage tips

### Features

✅ **No Coding Required** - Point and click interface  
✅ **Real-time Logs** - See what each agent is doing  
✅ **Interactive** - Upload data, configure, and run instantly  
✅ **Visual Results** - Charts and graphs automatically generated  
✅ **Export Data** - Download predictions and processed data  

### Tips

- Start with the sample data to understand the workflow
- The target column should be what you want to predict
- Training requires a target column to be selected
- Visualizations show data distribution and prediction quality
- Check the logs to understand what each agent is doing

### Troubleshooting

**Port Already in Use**
```bash
streamlit run webapp.py --server.port 8502
```

**Module Not Found**
Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

**Upload Failed**
Ensure your CSV file:
- Has a header row
- Is properly formatted
- Contains numeric or categorical data

### Screenshots

After launching, you'll see:
1. A sidebar for configuration
2. Tabs for different views
3. Data preview with statistics
4. Interactive buttons to run the pipeline
5. Real-time results and visualizations

Enjoy exploring the Multi-Agent System! 🚀
