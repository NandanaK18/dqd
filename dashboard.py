import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page config
st.set_page_config(
    page_title="Data Quality Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Override Streamlit's default background and text colors */
    .stApp {
        background-color: white !important;
    }
    
    .main .block-container {
        background-color: white !important;
    }
    
    /* Allow status indicators to keep their colors */
    .status-indicator {
        color: inherit !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg, .css-1lcbmhc {
        background-color: white !important;
        color: black !important;
    }
    
    /* Metric containers */
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #007770;
    }
    .metric-title {
        font-size: 14px;
        color: black !important;
        margin-bottom: 0.2rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: black !important;
        margin: 0;
    }
    .metric-delta {
        font-size: 12px;
        color: black !important;
        margin-top: 0.2rem;
    }
    
    /* Chart containers */
    .chart-container {
        background-color: #007770;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    /* Override Streamlit selectbox and multiselect */
    .stSelectbox > div > div, .stMultiSelect > div > div {
        background-color: white !important;
        color: black !important;
    }
    
    /* Enhanced filter widget styling */
    .stSelectbox, .stMultiSelect {
        background-color: white !important;
    }
    
    .stSelectbox > div > div > div, .stMultiSelect > div > div > div {
        background-color: white !important;
        color: black !important;
    }
    
    /* Filter dropdown styling */
    .stSelectbox > div > div > div > div, .stMultiSelect > div > div > div > div {
        background-color: white !important;
        color: black !important;
    }
    
    /* Multiselect selected items (tags) styling */
    .stMultiSelect span[data-baseweb="tag"] {
        background-color: #007770 !important;
        color: white !important;
        border: 1px solid #007770 !important;
    }
    
    /* Multiselect tag close button */
    .stMultiSelect span[data-baseweb="tag"] span[data-baseweb="icon"] {
        color: white !important;
    }
    
    /* Dropdown arrow styling */
    .stSelectbox svg, .stMultiSelect svg {
        color: black !important;
        fill: black !important;
    }
    
    /* Enhanced dropdown arrow visibility */
    .stSelectbox > div > div > div > svg, .stMultiSelect > div > div > div > svg {
        color: black !important;
        fill: black !important;
        stroke: black !important;
    }
    
    /* Override data editor */
    .stDataFrame, .stDataEditor {
        background-color: white !important;
        color: black !important;
    }
    
    /* Enhanced table styling - More aggressive selectors */
    .stDataFrame table, .stDataEditor table, 
    .stDataFrame tbody, .stDataEditor tbody,
    .stDataFrame thead, .stDataEditor thead {
        background-color: white !important;
        color: black !important;
        border: 1px solid black !important;
    }
    
    /* Table headers - Multiple selectors */
    .stDataFrame th, .stDataEditor th,
    .stDataFrame thead th, .stDataEditor thead th {
        background-color: white !important;
        color: black !important;
        border: 1px solid black !important;
        border-color: black !important;
    }
    
    /* Table cells - Multiple selectors */
    .stDataFrame td, .stDataEditor td,
    .stDataFrame tbody td, .stDataEditor tbody td {
        background-color: white !important;
        color: black !important;
        border: 1px solid black !important;
        border-color: black !important;
    }
    
    /* Table container - Remove conflicting background settings */
    .stDataFrame > div, .stDataEditor > div {
        color: black !important;
    }
    
    /* Data editor specific styling - Remove universal background override */
    div[data-testid="stDataFrame"], div[data-testid="stDataEditor"] {
        color: black !important;
        border: 1px solid black !important;
    }
    
    /* Only target text elements, not all elements */
    div[data-testid="stDataFrame"] span, div[data-testid="stDataEditor"] span,
    div[data-testid="stDataFrame"] p, div[data-testid="stDataEditor"] p,
    div[data-testid="stDataFrame"] div, div[data-testid="stDataEditor"] div {
        color: black !important;
    }
    
    /* Additional table text styling */
    .stDataFrame span, .stDataEditor span,
    .stDataFrame p, .stDataEditor p {
        color: black !important;
    }
    
    /* Table input fields styling */
    .stDataFrame input, .stDataEditor input {
        color: black !important;
        background-color: white !important;
        border: 1px solid black !important;
    }
    
    /* Override metric widgets and summary statistics */
    .css-1xarl3l, .css-1wivap2 {
        background-color: white !important;
        color: black !important;
    }
    
    /* Metric value styling */
    .css-1wivap2 > div, .css-1xarl3l > div {
        color: black !important;
    }
    
    /* Summary statistics specific styling */
    .metric-container div, .css-metric div {
        color: black !important;
    }
    
    /* Override all Streamlit text elements */
    .css-10trblm, .css-16idsys, .css-1dp5vir {
        color: black !important;
    }
    
    /* Override markdown text */
    .stMarkdown {
        color: black !important;
    }
    
    /* Override title and headers */
    .css-18e3th9, .css-1629p8f {
        color: black !important;
    }
    
    /* Comprehensive metric widget styling - More aggressive */
    [data-testid="metric-container"], 
    [data-testid="metric-container"] *,
    .css-1xarl3l, .css-1wivap2,
    .css-1xarl3l *, .css-1wivap2 * {
        background-color: white !important;
        color: black !important;
    }
    
    [data-testid="metric-container"] > div {
        color: black !important;
    }
    
    [data-testid="metric-container"] div[data-testid="metric-value"] {
        color: black !important;
    }
    
    [data-testid="metric-container"] div[data-testid="metric-label"] {
        color: black !important;
    }
    
    /* Force all metric text to be black */
    .css-metric, .css-metric div, .css-metric span,
    .css-metric *, .metric * {
        color: black !important;
    }
    
    /* Summary statistics text - Multiple selectors */
    .css-1kyxreq, .css-1dp5vir, .css-10trblm,
    .css-1kyxreq *, .css-1dp5vir *, .css-10trblm *,
    div[data-testid="metric-container"] div,
    div[data-testid="metric-container"] span {
        color: black !important;
    }
    
    /* Universal metric override */
    [class*="metric"] {
        color: black !important;
    }
    
    [class*="metric"] * {
        color: black !important;
    }
    
    /* Aggressive metric value targeting */
    .css-1wivap2, .css-1xarl3l, .css-metric-container {
        color: black !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    .css-1wivap2 *, .css-1xarl3l *, .css-metric-container * {
        color: black !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    /* Target the specific metric value elements */
    div[data-testid="metric-container"] > div:first-child {
        color: black !important;
        font-weight: bold !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    /* Ensure metric labels are visible */
    div[data-testid="metric-container"] > div:last-child {
        color: black !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
</style>
""", unsafe_allow_html=True)

# Sample data (replace this with your ChatGPT generated data)
@st.cache_data
def load_data():
    data = {
        'Country': ['USA', 'China', 'India', 'Germany', 'Japan', 'Brazil', 'Australia', 'UK', 'France', 'Canada'],
        'GDP_Trillions_USD': [15.3, 12.7, 3.7, 4.3, 4.9, 2.1, 1.6, 3.1, 2.9, 2.0],
        'Population_Millions': [331, 440, 380, 83, 125, 213, 26, 67, 68, 38],
        'Military_Spending_Billions': [478, 252, 72, 52, 49, 19, 31, 59, 50, 22],
        'Internet_Users_Millions': [298, 989, 658, 79, 118, 149, 22, 63, 60, 34],
        'CO2_Emissions_Million_Tons': [5007, 1065, 2654, 729, 1107, 469, 415, 351, 315, 572],
        'Renewable_Energy_TWh': [792, 2355, 158, 244, 199, 385, 32, 124, 119, 385],
        'Tourist_Arrivals_Millions': [79, 65, 17, 39, 32, 6, 9, 40, 90, 22],
        'Steel_Production_Million_Tons': [87, 1053, 118, 40, 83, 31, 6, 7, 14, 13],
        'Mobile_Subscribers_Millions': [442, 1732, 1198, 107, 186, 244, 28, 79, 71, 35],
        'University_Students_Millions': [20, 47, 37, 3, 4, 8, 1, 2, 3, 2],
        'Healthcare_Spending_Billions': [4224, 730, 75, 643, 461, 124, 240, 280, 323, 308]
    }
    return pd.DataFrame(data)

# Load data
df = load_data()

# Title with UST Global logo
title_col1, title_col2 = st.columns([1, 10])

with title_col1:
    # UST Global company logo from local file
    st.image("ust_logo.png", width=90)

with title_col2:
    st.markdown("""
    <div style="background-color: #007770; padding: 15px 20px; border-radius: 8px; margin: 10px 0;">
        <div style="color: white; margin: 0; font-size: 2.5rem; font-weight: bold; font-family: sans-serif;">Data Quality Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

# Top section with metrics and filters
col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 3, 3])

# Metrics in the left columns
with col1:
    st.markdown("""
    <div class="metric-container">
        <div class="metric-title">Total Countries</div>
        <div class="metric-value">10</div>
        <div class="metric-delta">Active Dataset</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_population = df['Population_Millions'].sum()
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-title">Total Population</div>
        <div class="metric-value">{total_population:,.0f}M</div>
        <div class="metric-delta">Global Coverage</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    avg_gdp_growth = 2.4  # Sample growth rate
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-title">Avg GDP Growth</div>
        <div class="metric-value">{avg_gdp_growth}%</div>
        <div class="metric-delta">Annual Rate</div>
    </div>
    """, unsafe_allow_html=True)

# Filters in the right columns
with col4:
    st.markdown('<h3 style="margin-bottom: 0px; margin-top: 0px;">Country Filter</h3>', unsafe_allow_html=True)
    st.markdown("""
    <style>
    .stMultiSelect > label {
        color: black !important;
        font-weight: bold !important;
    }
    .stMultiSelect {
        margin-top: -15px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    selected_countries = st.multiselect(
        "Select Countries",
        options=df['Country'].tolist(),
        default=['USA', 'India', 'China'],
        key="country_filter"
    )

with col5:
    st.markdown('<h3 style="margin-bottom: 0px; margin-top: 0px;">Metric Filter</h3>', unsafe_allow_html=True)
    st.markdown("""
    <style>
    .stSelectbox > label {
        color: black !important;
        font-weight: bold !important;
        margin-top: -15px !important;
    }
    .stSelectbox {
        margin-top: -10px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    metrics = [
        'GDP_Trillions_USD', 'Population_Millions', 'Military_Spending_Billions',
        'Internet_Users_Millions', 'CO2_Emissions_Million_Tons', 'Renewable_Energy_TWh',
        'Tourist_Arrivals_Millions', 'Steel_Production_Million_Tons', 
        'Mobile_Subscribers_Millions', 'University_Students_Millions', 'Healthcare_Spending_Billions'
    ]
    selected_metric = st.selectbox(
        "Select Primary Metric",
        options=metrics,
        index=0,
        key="metric_filter"
    )

st.markdown("---")

# Filter data based on selections
filtered_df = df[df['Country'].isin(selected_countries)]

# Charts section with horizontal scrolling
st.markdown("<h3 style='text-align: center;'>Missing Mandatory Data</h3>", unsafe_allow_html=True)

# Initialize session state for chart scrolling
if 'chart_start_index' not in st.session_state:
    st.session_state.chart_start_index = 0

# Define all available charts
chart_configs = [
    {
        'title': f"{selected_metric.replace('_', ' ').title()}",
        'metric': selected_metric,
        'color_scale': 'Blues'
    },
    {
        'title': "Population",
        'metric': 'Population_Millions',
        'color_scale': 'Greens'
    },
    {
        'title': "CO2 Emissions",
        'metric': 'CO2_Emissions_Million_Tons',
        'color_scale': 'Reds'
    },
    {
        'title': "Military Spending",
        'metric': 'Military_Spending_Billions',
        'color_scale': 'Oranges'
    },
    {
        'title': "Internet Users",
        'metric': 'Internet_Users_Millions',
        'color_scale': 'Purples'
    }
]

# Create columns for charts and navigation
chart_cols = st.columns([1, 1, 1, 1, 0.2])

# Display 4 charts starting from current index
for i in range(4):
    chart_index = st.session_state.chart_start_index + i
    if chart_index < len(chart_configs):
        chart_config = chart_configs[chart_index]
        
        with chart_cols[i]:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            
            # Status indicator instead of title
            metric_sum = filtered_df[chart_config['metric']].sum()
            
            if chart_config['metric'] == selected_metric:
                status_value = round(metric_sum, 1)
                if metric_sum >= 50:
                    status_color = "#007770"
                    status_text = "Excellent Performance"
                elif metric_sum >= 20:
                    status_color = "#ffc107"
                    status_text = "Good Progress"
                else:
                    status_color = "#dc3545"
                    status_text = "Action Required"
            elif chart_config['metric'] == 'Population_Millions':
                status_value = int(metric_sum)
                if metric_sum >= 1000:
                    status_color = "#007770"
                    status_text = "High Population"
                elif metric_sum >= 500:
                    status_color = "#ffc107"
                    status_text = "Moderate Population"
                else:
                    status_color = "#dc3545"
                    status_text = "Low Population"
            elif chart_config['metric'] == 'CO2_Emissions_Million_Tons':
                status_value = int(metric_sum)
                if metric_sum >= 8000:
                    status_color = "#dc3545"
                    status_text = "Critical Levels"
                elif metric_sum >= 4000:
                    status_color = "#ffc107"
                    status_text = "High Emissions"
                else:
                    status_color = "#007770"
                    status_text = "Within Limits"
            elif chart_config['metric'] == 'Military_Spending_Billions':
                status_value = int(metric_sum)
                if metric_sum >= 800:
                    status_color = "#dc3545"
                    status_text = "Very High Spending"
                elif metric_sum >= 400:
                    status_color = "#ffc107"
                    status_text = "High Spending"
                else:
                    status_color = "#007770"
                    status_text = "Normal Range"
            else:  # Internet Users
                status_value = int(metric_sum)
                if metric_sum >= 1000:
                    status_color = "#007770"
                    status_text = "Excellent Coverage"
                elif metric_sum >= 500:
                    status_color = "#ffc107"
                    status_text = "Good Coverage"
                else:
                    status_color = "#dc3545"
                    status_text = "Action Required"
            
            # Display status indicator
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 10px;" class="status-indicator">
                <div style="font-size: 24px; font-weight: bold; color: {status_color};">{status_value}</div>
                <div style="font-size: 12px; color: {status_color}; font-weight: bold;">▶ {status_text}</div>
            </div>
            """, unsafe_allow_html=True)
            
            fig = px.bar(
                filtered_df, 
                x='Country', 
                y=chart_config['metric'],
                title=f"{chart_config['metric'].replace('_', ' ').title()}"
            )
            fig.update_layout(
                height=350,
                showlegend=False,
                xaxis_title="Country",
                yaxis_title=chart_config['metric'].replace('_', ' ').title(),
                font=dict(size=10, color='black'),
                margin=dict(l=40, r=40, t=50, b=40),
                plot_bgcolor='white',
                paper_bgcolor='white',
                title_font_color='black',
                xaxis=dict(color='black', gridcolor='black', tickfont=dict(color='black')),
                yaxis=dict(color='black', gridcolor='black', tickfont=dict(color='black'))
            )
            # Set a single color for all bars to avoid color scale
            fig.update_traces(marker_color='#1f77b4')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Empty column if no chart to display
        with chart_cols[i]:
            st.empty()

# Navigation arrow in the 5th column
with chart_cols[4]:
    st.markdown("<br><br><br><br><br><br><br><br>", unsafe_allow_html=True)  # Add spacing to center the button
    
    # Right arrow - only show if we can scroll forward
    max_start_index = len(chart_configs) - 4  # Maximum starting index to show 4 charts
    if st.session_state.chart_start_index < max_start_index:
        if st.button("→", key="scroll_right", help="Scroll to next chart"):
            st.session_state.chart_start_index += 1
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Left arrow - only show if we can scroll backward
    if st.session_state.chart_start_index > 0:
        if st.button("←", key="scroll_left", help="Scroll to previous chart"):
            st.session_state.chart_start_index -= 1
            st.rerun()

# Solid line separator
st.markdown("<hr style='border: 2px solid #333; margin: 2rem 0;'>", unsafe_allow_html=True)

# Second row of charts
st.markdown("<h3 style='text-align: center;'>Unusual Transaction/Outliers</h3>", unsafe_allow_html=True)

# Define additional charts
additional_chart_configs = [
    {
        'title': "Renewable Energy",
        'metric': 'Renewable_Energy_TWh',
        'color_scale': 'Greens'
    },
    {
        'title': "Tourist Arrivals",
        'metric': 'Tourist_Arrivals_Millions',
        'color_scale': 'Blues'
    },
    {
        'title': "Steel Production",
        'metric': 'Steel_Production_Million_Tons',
        'color_scale': 'Greys'
    },
    {
        'title': "Healthcare Spending",
        'metric': 'Healthcare_Spending_Billions',
        'color_scale': 'Reds'
    }
]

# Create columns for additional charts
additional_chart_cols = st.columns(4)

# Display additional charts
for i in range(4):
    chart_config = additional_chart_configs[i]
    
    with additional_chart_cols[i]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        # Status indicator for additional charts
        metric_sum = filtered_df[chart_config['metric']].sum()
        
        if chart_config['metric'] == 'Renewable_Energy_TWh':
            status_value = int(metric_sum)
            if metric_sum >= 1000:
                status_color = "#007770"
                status_text = "Excellent Progress"
            elif metric_sum >= 500:
                status_color = "#ffc107"
                status_text = "Good Progress"
            else:
                status_color = "#dc3545"
                status_text = "Action Required"
        elif chart_config['metric'] == 'Tourist_Arrivals_Millions':
            status_value = int(metric_sum)
            if metric_sum >= 150:
                status_color = "#007770"
                status_text = "Thriving Tourism"
            elif metric_sum >= 75:
                status_color = "#ffc107"
                status_text = "Moderate Tourism"
            else:
                status_color = "#dc3545"
                status_text = "Needs Growth"
        elif chart_config['metric'] == 'Steel_Production_Million_Tons':
            status_value = int(metric_sum)
            if metric_sum >= 500:
                status_color = "#007770"
                status_text = "Strong Industry"
            elif metric_sum >= 200:
                status_color = "#ffc107"
                status_text = "Moderate Output"
            else:
                status_color = "#dc3545"
                status_text = "Low Production"
        else:  # Healthcare Spending
            status_value = int(metric_sum)
            if metric_sum >= 3000:
                status_color = "#007770"
                status_text = "Well Funded"
            elif metric_sum >= 1500:
                status_color = "#ffc107"
                status_text = "Adequate Funding"
            else:
                status_color = "#dc3545"
                status_text = "Action Required"
        
        # Display status indicator
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 10px;" class="status-indicator">
            <div style="font-size: 24px; font-weight: bold; color: {status_color};">{status_value}</div>
            <div style="font-size: 12px; color: {status_color}; font-weight: bold;">▶ {status_text}</div>
        </div>
        """, unsafe_allow_html=True)
        
        fig = px.bar(
            filtered_df, 
            x='Country', 
            y=chart_config['metric'],
            title=f"{chart_config['metric'].replace('_', ' ').title()}"
        )
        fig.update_layout(
            height=350,
            showlegend=False,
            xaxis_title="Country",
            yaxis_title=chart_config['metric'].replace('_', ' ').title(),
            font=dict(size=10, color='black'),
            margin=dict(l=40, r=40, t=50, b=40),
            plot_bgcolor='white',
            paper_bgcolor='white',
            title_font_color='black',
            xaxis=dict(color='black', gridcolor='black', tickfont=dict(color='black')),
            yaxis=dict(color='black', gridcolor='black', tickfont=dict(color='black'))
        )
        # Set a single color for all bars to avoid color scale
        fig.update_traces(marker_color='#2ca02c')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Solid line separator for third row
st.markdown("<hr style='border: 2px solid #333; margin: 2rem 0;'>", unsafe_allow_html=True)

# Third row of charts - remaining 2 graphs centered
st.markdown("<h3 style='text-align: center;'>Data Inconsistencies</h3>", unsafe_allow_html=True)

# Define remaining charts
remaining_chart_configs = [
    {
        'title': "Mobile Subscribers",
        'metric': 'Mobile_Subscribers_Millions',
        'color_scale': 'Purples'
    },
    {
        'title': "University Students",
        'metric': 'University_Students_Millions',
        'color_scale': 'Oranges'
    }
]

# Create columns to match the layout above (same as second row)
remaining_chart_cols = st.columns(4)

# Display remaining charts in center positions (columns 1 and 2, same as center of second row)
for i in range(2):
    chart_config = remaining_chart_configs[i]
    
    with remaining_chart_cols[i + 1]:  # Use columns 1 and 2 (positions 2 and 3 of 4)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        # Status indicator for remaining charts
        metric_sum = filtered_df[chart_config['metric']].sum()
        
        if chart_config['metric'] == 'Mobile_Subscribers_Millions':
            status_value = int(metric_sum)
            if metric_sum >= 1500:
                status_color = "#007770"
                status_text = "High Adoption"
            elif metric_sum >= 800:
                status_color = "#ffc107"
                status_text = "Good Adoption"
            else:
                status_color = "#dc3545"
                status_text = "Action Required"
        else:  # University Students
            status_value = int(metric_sum)
            if metric_sum >= 80:
                status_color = "#007770"
                status_text = "Excellent Education"
            elif metric_sum >= 40:
                status_color = "#ffc107"
                status_text = "Good Education"
            else:
                status_color = "#dc3545"
                status_text = "Needs Growth"
        
        # Display status indicator
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 10px;" class="status-indicator">
            <div style="font-size: 24px; font-weight: bold; color: {status_color};">{status_value}</div>
            <div style="font-size: 12px; color: {status_color}; font-weight: bold;">▶ {status_text}</div>
        </div>
        """, unsafe_allow_html=True)
        
        fig = px.bar(
            filtered_df, 
            x='Country', 
            y=chart_config['metric'],
            title=f"{chart_config['metric'].replace('_', ' ').title()}"
        )
        fig.update_layout(
            height=350,
            showlegend=False,
            xaxis_title="Country",
            yaxis_title=chart_config['metric'].replace('_', ' ').title(),
            font=dict(size=10, color='black'),
            margin=dict(l=40, r=40, t=50, b=40),
            plot_bgcolor='white',
            paper_bgcolor='white',
            title_font_color='black',
            xaxis=dict(color='black', gridcolor='black', tickfont=dict(color='black')),
            yaxis=dict(color='black', gridcolor='black', tickfont=dict(color='black'))
        )
        # Set a single color for all bars to avoid color scale
        fig.update_traces(marker_color='#ff7f0e')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Solid line separator for data table
st.markdown("<hr style='border: 2px solid #333; margin: 2rem 0;'>", unsafe_allow_html=True)

# Data table section
st.markdown("<h3 style='text-align: center;'>Selected Countries Data</h3>", unsafe_allow_html=True)

# Display data table for selected countries
if selected_countries:
    # Filter the dataframe for selected countries
    table_df = df[df['Country'].isin(selected_countries)].copy()
    
    # Select only the required columns
    display_cols = ['Country', 'GDP_Trillions_USD', 'Population_Millions', 'Military_Spending_Billions', 'Healthcare_Spending_Billions']
    table_df = table_df[display_cols].copy()
    
    # Round numerical columns for better display
    numerical_cols = ['GDP_Trillions_USD', 'Population_Millions', 'Military_Spending_Billions', 'Healthcare_Spending_Billions']
    for col in numerical_cols:
        table_df[col] = table_df[col].round(2)
    
    # Initialize session state for comments if not exists
    if 'country_comments' not in st.session_state:
        st.session_state.country_comments = {}
    
    # Add comments column
    table_df['Comments'] = ''
    for idx, country in enumerate(table_df['Country']):
        if country in st.session_state.country_comments:
            table_df.loc[table_df['Country'] == country, 'Comments'] = st.session_state.country_comments[country]
    
    # Display the editable table
    edited_df = st.data_editor(
        table_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Country": st.column_config.TextColumn("Country", width="medium", disabled=True),
            "GDP_Trillions_USD": st.column_config.NumberColumn("GDP (Trillions $)", format="%.2f", disabled=True),
            "Population_Millions": st.column_config.NumberColumn("Population (M)", format="%.0f", disabled=True),
            "Military_Spending_Billions": st.column_config.NumberColumn("Military Spending (B$)", format="%.0f", disabled=True),
            "Healthcare_Spending_Billions": st.column_config.NumberColumn("Healthcare Spending (B$)", format="%.0f", disabled=True),
            "Comments": st.column_config.TextColumn("Comments", width="large")
        },
        key="country_data_table"
    )
    
    # Update session state with comments
    for idx, row in edited_df.iterrows():
        country = row['Country']
        comment = row['Comments']
        if comment:  # Only store non-empty comments
            st.session_state.country_comments[country] = comment
        elif country in st.session_state.country_comments and not comment:
            # Remove comment if user cleared it
            del st.session_state.country_comments[country]
    
    # Summary statistics for the 4 displayed metrics only
    st.markdown("#### Summary Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_countries = len(selected_countries)
        st.markdown(f"""
        <div style="text-align: center; padding: 10px; background-color: white; border-radius: 5px;">
            <div style="font-size: 14px; color: black; margin-bottom: 5px;">Countries Selected</div>
            <div style="font-size: 24px; font-weight: bold; color: black;">{total_countries}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_pop = table_df['Population_Millions'].sum()
        st.markdown(f"""
        <div style="text-align: center; padding: 10px; background-color: white; border-radius: 5px;">
            <div style="font-size: 14px; color: black; margin-bottom: 5px;">Total Population (M)</div>
            <div style="font-size: 24px; font-weight: bold; color: black;">{total_pop:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_military = table_df['Military_Spending_Billions'].sum()
        st.markdown(f"""
        <div style="text-align: center; padding: 10px; background-color: white; border-radius: 5px;">
            <div style="font-size: 14px; color: black; margin-bottom: 5px;">Total Military Spending (B$)</div>
            <div style="font-size: 24px; font-weight: bold; color: black;">{total_military:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_healthcare = table_df['Healthcare_Spending_Billions'].sum()
        st.markdown(f"""
        <div style="text-align: center; padding: 10px; background-color: white; border-radius: 5px;">
            <div style="font-size: 14px; color: black; margin-bottom: 5px;">Total Healthcare Spending (B$)</div>
            <div style="font-size: 24px; font-weight: bold; color: black;">{total_healthcare:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

else:
    st.info("Please select countries from the filter above to view their data.")

# Footer
st.markdown("---")
st.markdown("**Data Analytics Dashboard** | Built with Streamlit")
