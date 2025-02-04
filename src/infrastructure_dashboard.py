import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Infrastructure Asset Management Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

def format_euro(value):
    """Format a number as Euro currency"""
    if pd.isna(value) or value == 0:
        return "€ 0"
    formatted = f"{float(value):,.2f}"
    formatted = formatted.replace(",", "@").replace(".", ",").replace("@", ".")
    return f"€ {formatted}"

@st.cache_data
def load_data():
    try:
        file_path = Path("../data/excel/cleaned_filtered_data.csv")
        if not file_path.exists():
            st.error(f"Data file not found at: {file_path}")
            return pd.DataFrame()
        
        df = pd.read_csv(file_path)
        # Clean column names
        df.columns = ['Asset', 'Total_Area', 'Unit_Price', 'Total_Value']
        
        # Remove rows with missing values in important columns
        df = df.dropna(subset=['Asset', 'Total_Value'])
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def main():
    st.title("Infrastructure Asset Management Dashboard")
    st.subheader("Gemeente Rotterdam Infrastructure Analysis")
    
    # Load data
    df = load_data()
    
    if df.empty:
        st.error("No data available to display")
        return

    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Filter by asset type
    asset_types = ['All'] + sorted(df['Asset'].unique().tolist())
    selected_asset = st.sidebar.selectbox("Select Asset Type", asset_types)
    
    # Apply filters
    if selected_asset != 'All':
        df_filtered = df[df['Asset'] == selected_asset]
    else:
        df_filtered = df.copy()

    # Top metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_value = df_filtered['Total_Value'].sum()
        st.metric("Total Asset Value", format_euro(total_value))
    
    with col2:
        avg_unit_price = df_filtered['Unit_Price'].mean()
        st.metric("Average Unit Price", format_euro(avg_unit_price))
    
    with col3:
        total_assets = len(df_filtered)
        st.metric("Number of Asset Types", str(total_assets))

    # Create two columns for charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Asset Value Distribution")
        # Sort by value for better visualization
        df_sorted = df_filtered.sort_values('Total_Value', ascending=True)
        fig = px.bar(df_sorted, 
                    x='Total_Value', 
                    y='Asset',
                    orientation='h',
                    title="Total Value per Asset Type")
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Asset Value Breakdown")
        fig = px.pie(df_filtered,
                    values='Total_Value',
                    names='Asset',
                    title="Distribution of Asset Values")
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)

    # Detailed data table
    st.subheader("Detailed Asset Information")
    
    # Format the dataframe for display
    df_display = df_filtered.copy()
    df_display['Unit_Price'] = df_display['Unit_Price'].apply(format_euro)
    df_display['Total_Value'] = df_display['Total_Value'].apply(format_euro)
    
    st.dataframe(
        df_display,
        column_config={
            "Asset": "Asset Type",
            "Total_Area": "Total Area (m²)",
            "Unit_Price": "Price per Unit",
            "Total_Value": "Total Value"
        },
        hide_index=True
    )

    # Add analysis section
    st.markdown("---")
    st.subheader("Asset Analysis Insights")
    
    # Calculate and display some insights
    top_assets = df.nlargest(5, 'Total_Value')
    st.write("Top 5 Assets by Value:")
    for _, row in top_assets.iterrows():
        st.write(f"- {row['Asset']}: {format_euro(row['Total_Value'])}")

if __name__ == "__main__":
    main()
