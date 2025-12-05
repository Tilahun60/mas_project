"""
Streamlit Web Frontend for Multi-Agent System
A simple interactive web interface to demonstrate the MAS pipeline.
"""
import streamlit as st
import pandas as pd
import os
import sys
from io import StringIO
import base64

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orchestrator import Orchestrator


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Multi-Agent System Dashboard",
        page_icon="🤖",
        layout="wide"
    )
    
    # Title and description
    st.title("🤖 Multi-Agent System Dashboard")
    st.markdown("""
    This interactive dashboard demonstrates the Multi-Agent System for data processing, 
    feature engineering, ML prediction, and visualization.
    """)
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    
    # Data source selection
    data_source = st.sidebar.radio(
        "Select Data Source:",
        ["Use Sample Data", "Upload CSV File"]
    )
    
    df = None
    
    if data_source == "Upload CSV File":
        uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.sidebar.success(f"✅ Uploaded: {uploaded_file.name}")
    else:
        # Use sample data
        sample_path = "data/sample_data.csv"
        if os.path.exists(sample_path):
            df = pd.read_csv(sample_path)
            st.sidebar.info("📊 Using sample_data.csv")
        else:
            st.sidebar.error("❌ Sample data not found!")
    
    # Target column selection
    target_column = None
    if df is not None:
        columns = df.columns.tolist()
        target_column = st.sidebar.selectbox(
            "Select Target Column (optional):",
            ["None"] + columns
        )
        if target_column == "None":
            target_column = None
    
    # Pipeline options
    st.sidebar.subheader("Pipeline Options")
    train_model = st.sidebar.checkbox("Train ML Model", value=True if target_column else False)
    create_viz = st.sidebar.checkbox("Create Visualizations", value=True)
    
    # Main content area
    if df is not None:
        # Create tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Data Preview", "🚀 Run Pipeline", "📈 Results", "ℹ️ About"])
        
        with tab1:
            st.subheader("Data Preview")
            st.write(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
            st.dataframe(df.head(20), use_container_width=True)
            
            # Basic statistics
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Numeric Columns:**")
                numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                st.write(numeric_cols if numeric_cols else "None")
            with col2:
                st.write("**Categorical Columns:**")
                cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
                st.write(cat_cols if cat_cols else "None")
        
        with tab2:
            st.subheader("🚀 Run Multi-Agent System Pipeline")
            
            if st.button("▶️ Execute Pipeline", type="primary", use_container_width=True):
                with st.spinner("Running Multi-Agent System pipeline..."):
                    try:
                        # Save uploaded data to temp file if needed
                        if data_source == "Upload CSV File":
                            temp_path = "data/temp_upload.csv"
                            df.to_csv(temp_path, index=False)
                            data_path = temp_path
                        else:
                            data_path = "data/sample_data.csv"
                        
                        # Initialize orchestrator
                        orchestrator = Orchestrator()
                        
                        # Create a container for logs
                        log_container = st.expander("📋 Pipeline Logs", expanded=True)
                        
                        # Capture output
                        import io
                        from contextlib import redirect_stdout
                        
                        f = io.StringIO()
                        with redirect_stdout(f):
                            # Run pipeline
                            results = orchestrator.run_pipeline(
                                data_path=data_path,
                                target_column=target_column,
                                train_model=train_model and target_column is not None,
                                visualize=create_viz,
                                save_visualization="webapp_visualization.png"
                            )
                        
                        # Show logs
                        logs = f.getvalue()
                        log_container.code(logs)
                        
                        # Store results in session state
                        st.session_state['results'] = results
                        st.session_state['orchestrator'] = orchestrator
                        
                        st.success("✅ Pipeline completed successfully!")
                        st.info("👉 Check the 'Results' tab to see the output")
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        import traceback
                        st.code(traceback.format_exc())
        
        with tab3:
            st.subheader("📈 Pipeline Results")
            
            if 'results' in st.session_state:
                results = st.session_state['results']
                orchestrator = st.session_state['orchestrator']
                
                # Display metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Data Rows", results['data_shape'][0])
                with col2:
                    st.metric("Features", results['features_shape'][1])
                with col3:
                    if results['has_predictions']:
                        st.metric("Predictions", results['num_predictions'])
                    else:
                        st.metric("Predictions", "N/A")
                
                # Show processed data
                st.subheader("Processed Data")
                if orchestrator.data is not None:
                    st.dataframe(orchestrator.data.head(10), use_container_width=True)
                
                # Show features
                st.subheader("Engineered Features")
                if orchestrator.features is not None:
                    st.dataframe(orchestrator.features.head(10), use_container_width=True)
                
                # Show predictions
                if results['has_predictions'] and orchestrator.predictions is not None:
                    st.subheader("Predictions")
                    pred_df = pd.DataFrame({
                        'Index': range(len(orchestrator.predictions)),
                        'Prediction': orchestrator.predictions
                    })
                    st.dataframe(pred_df.head(20), use_container_width=True)
                    
                    # Download predictions
                    csv = pred_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Predictions",
                        data=csv,
                        file_name="predictions.csv",
                        mime="text/csv"
                    )
                
                # Show visualization
                if create_viz and os.path.exists("webapp_visualization.png"):
                    st.subheader("Visualization")
                    st.image("webapp_visualization.png", use_column_width=True)
                
            else:
                st.info("👈 Run the pipeline from the 'Run Pipeline' tab to see results here")
        
        with tab4:
            st.subheader("ℹ️ About Multi-Agent System")
            st.markdown("""
            ### System Architecture
            
            The Multi-Agent System consists of specialized agents that work together:
            
            1. **DataCollectorAgent** 🗂️
               - Loads CSV data
               - Removes duplicates
               - Handles missing values
            
            2. **FeatureProcessorAgent** 🔧
               - Normalizes numeric features
               - Encodes categorical features
               - Performs feature engineering
            
            3. **PredictionAgent** 🎯
               - Trains ML models (Random Forest)
               - Makes predictions
               - Supports classification & regression
            
            4. **VisualizationAgent** 📊
               - Creates data visualizations
               - Plots predictions vs actual
               - Generates insight graphs
            
            5. **Orchestrator** 🎭
               - Coordinates all agents
               - Manages data flow
               - Handles pipeline execution
            
            ### Usage Tips
            
            - Upload your own CSV data or use the sample dataset
            - Select a target column for supervised learning
            - Enable model training to get predictions
            - View detailed logs in the Pipeline tab
            - Download results for further analysis
            """)
    
    else:
        st.info("👈 Please select a data source from the sidebar to get started")
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Multi-Agent System v1.0**")
    st.sidebar.markdown("Built with ❤️ using Streamlit")


if __name__ == "__main__":
    main()
