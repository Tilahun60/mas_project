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
            
            # Add agent status visualization
            st.markdown("### 🤖 Multi-Agent System Workflow")
            st.markdown("""
            The pipeline coordinates **5 specialized agents** that work together:
            """)
            
            agent_col1, agent_col2 = st.columns(2)
            with agent_col1:
                st.info("🗂️ **DataCollectorAgent** - Loads & cleans data")
                st.info("🔧 **FeatureProcessorAgent** - Engineers features")
                st.info("🎯 **PredictionAgent** - Trains ML models")
            with agent_col2:
                st.info("📊 **VisualizationAgent** - Creates visualizations")
                st.info("🎭 **Orchestrator** - Coordinates all agents")
            
            st.markdown("---")
            
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
                        
                        # Create progress tracking
                        st.markdown("### 📊 Agent Activity Monitor")
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Agent status indicators
                        agent_status = {
                            'DataCollector': st.empty(),
                            'FeatureProcessor': st.empty(),
                            'PredictionAgent': st.empty(),
                            'VisualizationAgent': st.empty()
                        }
                        
                        # Show initial status
                        for agent_name, status_container in agent_status.items():
                            status_container.markdown(f"⏳ **{agent_name}**: Waiting...")
                        
                        # Create a container for logs
                        log_container = st.expander("📋 Detailed Pipeline Logs", expanded=False)
                        
                        # Capture output
                        import io
                        from contextlib import redirect_stdout
                        import time
                        
                        f = io.StringIO()
                        
                        # Update status as agents run
                        status_text.text("🎭 Orchestrator: Initializing Multi-Agent System...")
                        progress_bar.progress(10)
                        
                        with redirect_stdout(f):
                            # Run pipeline
                            results = orchestrator.run_pipeline(
                                data_path=data_path,
                                target_column=target_column,
                                train_model=train_model and target_column is not None,
                                visualize=create_viz,
                                save_visualization="webapp_visualization.png"
                            )
                        
                        # Parse logs to show agent activity
                        logs = f.getvalue()
                        log_lines = logs.split('\n')
                        
                        # Update agent statuses based on logs
                        agent_status['DataCollector'].markdown("✅ **DataCollectorAgent**: Completed - Loaded & cleaned data")
                        progress_bar.progress(30)
                        
                        agent_status['FeatureProcessor'].markdown("✅ **FeatureProcessorAgent**: Completed - Engineered features")
                        progress_bar.progress(60)
                        
                        if train_model and target_column:
                            agent_status['PredictionAgent'].markdown("✅ **PredictionAgent**: Completed - Trained model & made predictions")
                        else:
                            agent_status['PredictionAgent'].markdown("⏭️ **PredictionAgent**: Skipped (no target column)")
                        progress_bar.progress(80)
                        
                        if create_viz:
                            agent_status['VisualizationAgent'].markdown("✅ **VisualizationAgent**: Completed - Created visualizations")
                        else:
                            agent_status['VisualizationAgent'].markdown("⏭️ **VisualizationAgent**: Skipped")
                        progress_bar.progress(100)
                        
                        status_text.text("🎭 Orchestrator: All agents completed successfully!")
                        
                        # Show logs
                        log_container.code(logs)
                        
                        # Store results in session state
                        st.session_state['results'] = results
                        st.session_state['orchestrator'] = orchestrator
                        
                        st.success("✅ Multi-Agent System pipeline completed successfully!")
                        st.info("👉 Check the 'Results' tab to see what each agent produced")
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        import traceback
                        st.code(traceback.format_exc())
        
        with tab3:
            st.subheader("📈 Multi-Agent System Results")
            
            if 'results' in st.session_state:
                results = st.session_state['results']
                orchestrator = st.session_state['orchestrator']
                
                st.markdown("""
                ### 🎯 What Each Agent Produced
                Below you can see the output from each specialized agent in the Multi-Agent System.
                """)
                
                # Display overall metrics
                st.markdown("### 📊 Overall Pipeline Metrics")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Data Rows", results['data_shape'][0])
                with col2:
                    st.metric("Engineered Features", results['features_shape'][1])
                with col3:
                    if results['has_predictions']:
                        st.metric("Predictions Made", results['num_predictions'])
                    else:
                        st.metric("Predictions Made", "N/A")
                
                st.markdown("---")
                
                # Show processed data from DataCollectorAgent
                st.markdown("### 🗂️ DataCollectorAgent Output")
                st.markdown("**What this agent did:** Loaded CSV file, removed duplicates, handled missing values")
                if orchestrator.data is not None:
                    st.dataframe(orchestrator.data.head(10), use_container_width=True)
                    st.caption(f"Showing 10 of {len(orchestrator.data)} cleaned rows")
                
                st.markdown("---")
                
                # Show features from FeatureProcessorAgent
                st.markdown("### 🔧 FeatureProcessorAgent Output")
                st.markdown("**What this agent did:** Normalized numeric features, encoded categorical features, separated target variable")
                if orchestrator.features is not None:
                    st.dataframe(orchestrator.features.head(10), use_container_width=True)
                    st.caption(f"Showing 10 of {len(orchestrator.features)} feature rows")
                
                st.markdown("---")
                
                # Show predictions from PredictionAgent
                if results['has_predictions'] and orchestrator.predictions is not None:
                    st.markdown("### 🎯 PredictionAgent Output")
                    st.markdown("**What this agent did:** Trained Random Forest model, generated predictions")
                    pred_df = pd.DataFrame({
                        'Index': range(len(orchestrator.predictions)),
                        'Prediction': orchestrator.predictions
                    })
                    st.dataframe(pred_df.head(20), use_container_width=True)
                    st.caption(f"Showing 20 of {len(pred_df)} predictions")
                    
                    # Download predictions
                    csv = pred_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download All Predictions",
                        data=csv,
                        file_name="mas_predictions.csv",
                        mime="text/csv"
                    )
                else:
                    st.markdown("### 🎯 PredictionAgent Output")
                    st.info("⏭️ PredictionAgent was skipped (no target column selected)")
                
                st.markdown("---")
                
                # Show visualization from VisualizationAgent
                if create_viz and os.path.exists("webapp_visualization.png"):
                    st.markdown("### 📊 VisualizationAgent Output")
                    st.markdown("**What this agent did:** Created charts showing data distribution, predictions, and comparison plots")
                    st.image("webapp_visualization.png", use_column_width=True)
                else:
                    st.markdown("### 📊 VisualizationAgent Output")
                    st.info("⏭️ VisualizationAgent was skipped (visualization disabled)")
                
            else:
                st.info("👈 Run the Multi-Agent System pipeline from the 'Run Pipeline' tab to see what each agent produces!")
        
        with tab4:
            st.subheader("ℹ️ About Multi-Agent System")
            st.markdown("""
            ### What is a Multi-Agent System?
            
            A **Multi-Agent System (MAS)** is an approach where multiple specialized software agents 
            work together to accomplish a complex task. Each agent is responsible for a specific 
            function, and they collaborate through an orchestrator.
            
            ### Our MAS Architecture
            
            This system uses **5 specialized agents** that work in sequence:
            
            ```
            Data Input → DataCollector → FeatureProcessor → PredictionAgent → VisualizationAgent
                              ↓              ↓                    ↓                ↓
                         Orchestrator coordinates the entire workflow
            ```
            
            #### The Agents and Their Roles:
            
            **1. 🗂️ DataCollectorAgent**
            - **Role:** Data ingestion and cleaning
            - **Actions:** 
              - Loads CSV data files
              - Removes duplicate rows
              - Handles missing values
            - **Output:** Clean dataset ready for processing
            
            **2. 🔧 FeatureProcessorAgent**
            - **Role:** Feature engineering and transformation
            - **Actions:**
              - Separates features from target variable
              - Normalizes numeric features (standardization)
              - Encodes categorical features (label encoding)
            - **Output:** Processed feature matrix
            
            **3. 🎯 PredictionAgent**
            - **Role:** Machine learning model training and inference
            - **Actions:**
              - Trains Random Forest models
              - Detects classification vs regression tasks
              - Makes predictions
              - Saves/loads trained models
            - **Output:** Predictions and trained model
            
            **4. 📊 VisualizationAgent**
            - **Role:** Data and result visualization
            - **Actions:**
              - Creates distribution charts
              - Plots predictions vs actual values
              - Generates comparative visualizations
            - **Output:** Visual charts and graphs
            
            **5. 🎭 Orchestrator**
            - **Role:** System coordinator
            - **Actions:**
              - Initializes all agents
              - Manages data flow between agents
              - Handles pipeline execution
              - Provides results summary
            - **Output:** Coordinates the entire workflow
            
            ### How to See the Agents in Action
            
            1. **Run Pipeline Tab:** Watch the "Agent Activity Monitor" to see each agent activate
            2. **Results Tab:** See what each agent produced (clearly labeled by agent name)
            3. **Detailed Logs:** Expand the logs to see each agent's console output
            
            ### Why Use a Multi-Agent System?
            
            ✅ **Modularity:** Each agent can be updated independently  
            ✅ **Reusability:** Agents can be reused in different pipelines  
            ✅ **Maintainability:** Easier to debug and maintain  
            ✅ **Scalability:** New agents can be added without changing others  
            ✅ **Clarity:** Each agent has a clear, single responsibility
            """)
    
    else:
        st.info("👈 Please select a data source from the sidebar to get started")
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Multi-Agent System v1.0**")
    st.sidebar.markdown("Built with ❤️ using Streamlit")


if __name__ == "__main__":
    main()
