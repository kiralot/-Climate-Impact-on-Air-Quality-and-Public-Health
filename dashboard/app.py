import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os

st.set_page_config(
    page_title="Climate & Health Analytics",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* Dark theme base - Complete Streamlit override */
    .stApp {
        background-color: #0f1419;
    }
    
    .main {
        background-color: #0f1419;
    }
    
    /* Override Streamlit default backgrounds */
    .block-container {
        background-color: #0f1419;
        padding-top: 2rem;
    }
    
    /* Hero section container with animation */
    .hero-section {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
        animation: fadeInUp 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Main title styling with animation */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(120deg, #667eea, #764ba2, #f093fb, #667eea);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 0.5rem 0;
        margin-bottom: 1rem;
        animation: gradientShift 4s ease infinite;
        position: relative;
        z-index: 1;
        letter-spacing: -0.5px;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% center; }
        50% { background-position: 100% center; }
    }
    
    .subtitle {
        text-align: center;
        color: #e2e8f0;
        font-size: 1.2rem;
        margin-bottom: 0;
        font-weight: 500;
        position: relative;
        z-index: 1;
        line-height: 1.6;
        animation: fadeIn 1s ease-out 0.3s both;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Metric cards */
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: white;
    }
    
    .stMetric label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 600;
    }
    
    .stMetric .metric-value {
        color: white !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar styling - Professional purple theme */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #ffffff !important;
    }
    
    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    section[data-testid="stSidebar"] h2 {
        color: #ffffff !important;
    }
    
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: #ffffff !important;
    }
    
    /* Sidebar widgets styling */
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stSlider label {
        color: #ffffff !important;
    }
    
    /* Slider styling - Remove blue box and apply dark theme */
    section[data-testid="stSidebar"] .stSlider {
        background-color: transparent !important;
    }
    
    section[data-testid="stSidebar"] .stSlider > div {
        background-color: transparent !important;
    }
    
    section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] {
        background-color: transparent !important;
    }
    
    /* Slider track - inactive (gray) */
    section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] > div {
        background-color: #334155 !important;
    }
    
    /* Slider track - active (blue/purple) */
    section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] [data-baseweb="slider-track"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    /* Slider thumb */
    section[data-testid="stSidebar"] .stSlider [role="slider"] {
        background-color: #667eea !important;
        border: 2px solid #764ba2 !important;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Slider values (min/max numbers) */
    section[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMin"],
    section[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMax"],
    section[data-testid="stSidebar"] .stSlider div[data-baseweb="slider"] span {
        color: #ffffff !important;
    }
    
    /* Tabs styling - Dark theme */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: #1e293b;
        padding: 1rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3.5rem;
        background-color: #0f172a;
        border-radius: 8px;
        padding: 0 1.5rem;
        font-weight: 600;
        border: 2px solid #334155;
        color: #cbd5e1;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #1e293b;
        border-color: #475569;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border-color: transparent;
    }
    
    /* Cards for content sections - Dark theme */
    .content-card {
        background: #1e293b;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        margin-bottom: 1.5rem;
        border: 1px solid #334155;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid #667eea;
        background-color: #1e293b;
    }
    
    /* Dataframes */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        background-color: #1e293b;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Plotly charts */
    .js-plotly-plot {
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    /* Headers - Dark theme with white text */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    h2 {
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    
    /* All text elements white */
    p, label, span, div {
        color: #ffffff !important;
    }
    
    /* Radio buttons and slider labels - white text */
    .stRadio label, .stSlider label {
        color: #ffffff !important;
        font-weight: 500;
    }
    
    /* Radio button options */
    .stRadio > label > div[role="radiogroup"] > label {
        color: #ffffff !important;
    }
    
    .stRadio > label > div[role="radiogroup"] > label > div {
        color: #ffffff !important;
    }
    
    /* Slider values and all numbers */
    .stSlider [data-testid="stTickBarMin"],
    .stSlider [data-testid="stTickBarMax"],
    .stSlider span {
        color: #ffffff !important;
    }
    
    /* Selectbox styling - Dark theme with white text */
    .stSelectbox > div > div {
        border-radius: 8px;
        background-color: #1e293b;
        border-color: #334155;
    }
    
    .stSelectbox label {
        color: #ffffff !important;
        font-weight: 500;
    }
    
    /* Multiselect - Dark theme with white text */
    .stMultiSelect > div > div {
        border-radius: 8px;
        background-color: #1e293b !important;
        border-color: #334155 !important;
    }
    
    .stMultiSelect label {
        color: #ffffff !important;
        font-weight: 500;
    }
    
    /* Multiselect input container */
    .stMultiSelect [data-baseweb="select"] > div {
        background-color: #1e293b !important;
        border-color: #334155 !important;
    }
    
    /* Selected country tags - purple gradient like buttons */
    .stMultiSelect [data-baseweb="tag"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        border: none !important;
    }
    
    /* Tag close button (X) */
    .stMultiSelect [data-baseweb="tag"] svg {
        fill: #ffffff !important;
    }
    
    /* Input text color */
    input, select, textarea {
        color: #ffffff !important;
        background-color: #1e293b !important;
    }
    
    /* Dropdown options - Dark background with visible text */
    [role="listbox"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
    }
    
    [role="option"] {
        color: #ffffff !important;
        background-color: #1e293b !important;
    }
    
    [role="option"]:hover {
        background-color: #334155 !important;
        color: #ffffff !important;
    }
    
    /* Selectbox dropdown when open */
    [data-baseweb="popover"] {
        background-color: #1e293b !important;
    }
    
    [data-baseweb="menu"] {
        background-color: #1e293b !important;
    }
    
    [data-baseweb="menu"] li {
        background-color: #1e293b !important;
        color: #ffffff !important;
    }
    
    [data-baseweb="menu"] li:hover {
        background-color: #334155 !important;
    }
    
    /* Multiselect dropdown options */
    [data-baseweb="select"] [role="option"] {
        background-color: #1e293b !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'integrated_data_1990_2019.csv'))
    corr_df = pd.read_csv(os.path.join(RESULTS_DIR, 'climate_mortality_correlations.csv'))
    
    continent_mapping = {
        'Germany': 'Europe', 'United Kingdom': 'Europe', 'France': 'Europe', 'Italy': 'Europe',
        'Spain': 'Europe', 'Poland': 'Europe', 'Netherlands': 'Europe', 'Belgium': 'Europe',
        'Greece': 'Europe', 'Portugal': 'Europe',
        'China': 'Asia', 'India': 'Asia', 'Japan': 'Asia', 'Indonesia': 'Asia',
        'Pakistan': 'Asia', 'Bangladesh': 'Asia', 'Russia': 'Asia', 'Turkey': 'Asia',
        'Iran': 'Asia', 'Thailand': 'Asia',
        'United States': 'Americas', 'Brazil': 'Americas', 'Mexico': 'Americas', 'Canada': 'Americas',
        'Argentina': 'Americas', 'Colombia': 'Americas', 'Peru': 'Americas', 'Venezuela': 'Americas',
        'Chile': 'Americas', 'Ecuador': 'Americas',
        'Nigeria': 'Africa', 'Ethiopia': 'Africa', 'Egypt': 'Africa', 'South Africa': 'Africa',
        'Tanzania': 'Africa', 'Kenya': 'Africa', 'Algeria': 'Africa', 'Sudan': 'Africa',
        'Uganda': 'Africa',
        'Australia': 'Oceania', 'Papua New Guinea': 'Oceania', 'New Zealand': 'Oceania',
        'Fiji': 'Oceania', 'Solomon Islands': 'Oceania', 'Samoa': 'Oceania',
        'Vanuatu': 'Oceania', 'Kiribati': 'Oceania', 'Tonga': 'Oceania', 'Micronesia': 'Oceania'
    }
    df['Continent'] = df['Country/Territory'].map(continent_mapping)
    
    return df, corr_df

df, corr_df = load_data()

# Hero Section
st.markdown('''
<div class="hero-section">
    <h1 class="main-title">Climate & Health Analytics Platform</h1>
    <p class="subtitle">Comprehensive analysis of climate-mortality relationships across 49 countries (1990-2019)</p>
</div>
''', unsafe_allow_html=True)

st.markdown("---")

st.sidebar.header("Filters")

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=sorted(df['Country/Territory'].unique()),
    default=['United States', 'Germany', 'Italy', 'Japan', 'United Kingdom']
)

year_range = st.sidebar.slider(
    "Year Range",
    min_value=int(df['Year'].min()),
    max_value=int(df['Year'].max()),
    value=(1990, 2019)
)

filtered_df = df[
    (df['Country/Territory'].isin(selected_countries)) &
    (df['Year'] >= year_range[0]) &
    (df['Year'] <= year_range[1])
]

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Overview", "Climate Trends", "Mortality Analysis", "Correlations", "Predictions 2020-2030", "ML Model Analysis"])

with tab1:
    st.header("Dataset Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Countries", df['Country/Territory'].nunique())
    with col2:
        st.metric("Years", f"{df['Year'].min()}-{df['Year'].max()}")
    with col3:
        st.metric("Total Records", len(df))
    with col4:
        st.metric("Variables", len(df.columns))
    
    st.subheader("Sample Data")
    st.dataframe(filtered_df.head(10))

with tab2:
    st.header("Climate Trends")
    
    climate_var = st.selectbox(
        "Select Climate Variable",
        ['Temperature_C', 'Precipitation_mm', 'Surface_Pressure_Pa', 'Wind_Speed_ms']
    )
    
    # Aggregate data to ensure one value per country-year
    climate_plot_data = filtered_df.groupby(['Country/Territory', 'Year'])[climate_var].mean().reset_index()
    
    fig = px.line(
        climate_plot_data,
        x='Year',
        y=climate_var,
        color='Country/Territory',
        title=f'{climate_var} Evolution Over Time'
    )
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#0e1117',
        plot_bgcolor='#1e293b',
        font=dict(color='#ffffff', size=12),
        title_font=dict(color='#ffffff', size=16),
        height=500,
        xaxis=dict(gridcolor='#334155', color='#ffffff'),
        yaxis=dict(gridcolor='#334155', color='#ffffff'),
        legend=dict(font=dict(color='#ffffff'))
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Temperature Distribution by Country")
    fig2 = px.violin(
        filtered_df,
        x='Country/Territory',
        y='Temperature_C',
        title='Temperature Distribution',
        box=True,
        points='outliers',
        color='Country/Territory'
    )
    fig2.update_layout(
        template='plotly_dark',
        paper_bgcolor='#0e1117',
        plot_bgcolor='#1e293b',
        font=dict(color='#ffffff', size=12),
        title_font=dict(color='#ffffff', size=16),
        showlegend=False,
        height=600,
        xaxis=dict(tickangle=45, gridcolor='#334155', color='#ffffff'),
        yaxis=dict(gridcolor='#334155', color='#ffffff')
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.header("Mortality Analysis")
    
    rate_cols = [col for col in df.columns if col.endswith('_Rate_per_100k')]
    
    selected_cause = st.selectbox(
        "Select Cause of Death",
        [col.replace('_Rate_per_100k', '') for col in rate_cols]
    )
    
    rate_col = f'{selected_cause}_Rate_per_100k'
    
    # Aggregate data to ensure one value per country-year
    mortality_plot_data = filtered_df.groupby(['Country/Territory', 'Year'])[rate_col].mean().reset_index()
    
    fig = px.line(
        mortality_plot_data,
        x='Year',
        y=rate_col,
        color='Country/Territory',
        title=f'{selected_cause} - Death Rate per 100k'
    )
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#0e1117',
        plot_bgcolor='#1e293b',
        font=dict(color='#ffffff', size=12),
        title_font=dict(color='#ffffff', size=16),
        height=500,
        xaxis=dict(gridcolor='#334155', color='#ffffff'),
        yaxis=dict(gridcolor='#334155', color='#ffffff'),
        legend=dict(font=dict(color='#ffffff'))
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader(f"Average {selected_cause} Rate by Country")
    avg_by_country = filtered_df.groupby('Country/Territory')[rate_col].mean().sort_values(ascending=False)
    
    fig2 = px.bar(
        x=avg_by_country.index,
        y=avg_by_country.values,
        labels={'x': 'Country', 'y': 'Average Rate per 100k'},
        title=f'Average {selected_cause} Rate by Country',
        color=avg_by_country.values,
        color_continuous_scale='Viridis'
    )
    fig2.update_layout(
        template='plotly_dark',
        paper_bgcolor='#0e1117',
        plot_bgcolor='#1e293b',
        font=dict(color='#ffffff', size=12),
        title_font=dict(color='#ffffff', size=16),
        xaxis=dict(tickangle=45, gridcolor='#334155', color='#ffffff'),
        yaxis=dict(gridcolor='#334155', color='#ffffff'),
        height=600
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab4:
    st.header("Climate-Mortality Correlations")
    
    top_n = st.slider("Number of top correlations to display", 10, 50, 20)
    
    corr_type = st.radio("Correlation Type", ["Strongest (Absolute)", "Positive", "Negative"])
    
    if corr_type == "Strongest (Absolute)":
        top_corr = corr_df.nlargest(top_n, 'Correlation', keep='all')
    elif corr_type == "Positive":
        top_corr = corr_df.nlargest(top_n, 'Correlation')
    else:
        top_corr = corr_df.nsmallest(top_n, 'Correlation')
        
        # La figura se ve rara porque los valores son negativos 
    
    labels = [f"{row['Cause'][:30]} vs {row['Climate_Variable']}" for _, row in top_corr.iterrows()]
    
    fig = px.bar(
        top_corr,
        x='Correlation',
        y=labels,
        orientation='h',
        title=f'Top {top_n} Climate-Mortality Correlations ({corr_type})',
        color='Correlation',
        color_continuous_scale='RdBu_r',
        text='Correlation'
    )
    fig.update_traces(
        texttemplate='%{text:.3f}',
        textposition='outside'
    )
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#0e1117',
        plot_bgcolor='#1e293b',
        font=dict(color='#ffffff', size=11),
        title_font=dict(color='#ffffff', size=16),
        height=max(600, top_n * 25),
        yaxis=dict(tickfont=dict(size=10, color='#ffffff'), color='#ffffff'),
        xaxis=dict(gridcolor='#334155', color='#ffffff'),
        margin=dict(l=300, r=50, t=80, b=50)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Correlation Heatmap - Top Causes")
    top_causes = corr_df.groupby('Cause')['Correlation'].apply(lambda x: x.abs().max()).nlargest(10).index
    
    heatmap_data = corr_df[corr_df['Cause'].isin(top_causes)].pivot(
        index='Cause',
        columns='Climate_Variable',
        values='Correlation'
    )
    # Tengo que Fixear el heatmap porque no se ve bien
    
    fig_heatmap = px.imshow(
        heatmap_data,
        labels=dict(x="Climate Variable", y="Cause of Death", color="Correlation"),
        color_continuous_scale='RdBu_r',
        aspect="auto",
        text_auto='.2f'
    )
    fig_heatmap.update_layout(
        template='plotly_dark',
        paper_bgcolor='#0e1117',
        plot_bgcolor='#1e293b',
        font=dict(color='#ffffff', size=12),
        title_font=dict(color='#ffffff', size=16),
        height=600,
        xaxis=dict(side='bottom', color='#ffffff'),
        yaxis=dict(tickfont=dict(size=11, color='#ffffff'), color='#ffffff')
    )
    fig_heatmap.update_traces(
        text=heatmap_data.values,
        texttemplate='%{text:.2f}',
        textfont=dict(size=10)
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

with tab5:
    st.header("Future Mortality Predictions (2020-2030)")
    
    # Load predictions
    try:
        pred_df = pd.read_csv(os.path.join(RESULTS_DIR, 'temporal_predictions.csv'))
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                    padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; border: 1px solid rgba(102, 126, 234, 0.3);">
            <p style="color: #e2e8f0; margin: 0;">
                 <strong>Prophet Time Series Model</strong> trained on 30 years (1990-2019) of historical data<br>
                 Incorporates <strong>5 climate variables</strong> as predictors: Temperature, Precipitation, Pressure, Dewpoint, Wind Speed<br>
                 Forecasts for <strong>8 countries</strong> across different continents<br>
                 Predictions for <strong>top 10 mortality causes</strong> including cardiovascular diseases, neoplasms, and respiratory conditions
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            pred_country = st.selectbox(
                "Select Country for Prediction",
                options=sorted(pred_df['Country'].unique()),
                key='pred_country'
            )
        
        with col2:
            pred_cause = st.selectbox(
                "Select Cause of Death",
                options=sorted(pred_df['Cause'].unique()),
                key='pred_cause'
            )
        
        # Filter prediction data
        pred_filtered = pred_df[
            (pred_df['Country'] == pred_country) &
            (pred_df['Cause'] == pred_cause)
        ]
        
        # Get historical data for comparison
        hist_data = df[df['Country/Territory'] == pred_country].copy()
        hist_data = hist_data[['Year', pred_cause]].groupby('Year')[pred_cause].mean().reset_index()
        
        # Create combined historical + prediction plot
        st.subheader(f"{pred_cause} - Historical vs Predicted Trend")
        
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=hist_data['Year'],
            y=hist_data[pred_cause],
            name='Historical (1990-2019)',
            mode='lines+markers',
            line=dict(color='#667eea', width=3),
            marker=dict(size=6)
        ))
        
        # Predicted data
        fig.add_trace(go.Scatter(
            x=pred_filtered['Year'],
            y=pred_filtered['Predicted_Rate'],
            name='Predicted (2020-2030)',
            mode='lines+markers',
            line=dict(color='#f093fb', width=3, dash='dash'),
            marker=dict(size=6, symbol='diamond')
        ))
        
        # Confidence interval
        fig.add_trace(go.Scatter(
            x=pred_filtered['Year'],
            y=pred_filtered['Upper_Bound'],
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig.add_trace(go.Scatter(
            x=pred_filtered['Year'],
            y=pred_filtered['Lower_Bound'],
            mode='lines',
            line=dict(width=0),
            fillcolor='rgba(240, 147, 251, 0.2)',
            fill='tonexty',
            name='Confidence Interval',
            hoverinfo='skip'
        ))
        
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='#0e1117',
            plot_bgcolor='#1e293b',
            font=dict(color='#ffffff', size=12),
            title_font=dict(color='#ffffff', size=16),
            height=600,
            xaxis=dict(
                title='Year',
                gridcolor='#334155',
                color='#ffffff',
                range=[1990, 2030]
            ),
            yaxis=dict(
                title='Absolute Deaths',
                gridcolor='#334155',
                color='#ffffff'
            ),
            legend=dict(
                font=dict(color='#ffffff'),
                bgcolor='rgba(30, 41, 59, 0.8)',
                bordercolor='#667eea',
                borderwidth=1
            ),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Prediction statistics
        st.subheader("Prediction Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        last_historical = hist_data.iloc[-1][pred_cause]
        first_prediction = pred_filtered.iloc[0]['Predicted_Rate']
        last_prediction = pred_filtered.iloc[-1]['Predicted_Rate']
        change_percent = ((last_prediction - last_historical) / last_historical) * 100
        
        with col1:
            st.metric(
                "2019 (Last Historical)",
                f"{last_historical:,.0f}",
                help="Last year of historical data"
            )
        
        with col2:
            st.metric(
                "2020 (First Prediction)",
                f"{first_prediction:,.0f}",
                f"{((first_prediction - last_historical) / last_historical * 100):+.1f}%"
            )
        
        with col3:
            st.metric(
                "2030 (Final Prediction)",
                f"{last_prediction:,.0f}",
                f"{change_percent:+.1f}%"
            )
        
        with col4:
            avg_annual_change = (last_prediction - last_historical) / 11
            st.metric(
                "Avg Annual Change",
                f"{avg_annual_change:+,.0f}",
                help="Average annual change from 2020-2030"
            )
        
        # Detailed predictions table
        with st.expander("📋 View Detailed Predictions Table"):
            display_df = pred_filtered[['Year', 'Predicted_Rate', 'Lower_Bound', 'Upper_Bound']].copy()
            display_df.columns = ['Year', 'Predicted Deaths', 'Lower Bound (95%)', 'Upper Bound (95%)']
            display_df['Predicted Deaths'] = display_df['Predicted Deaths'].apply(lambda x: f"{x:,.0f}")
            display_df['Lower Bound (95%)'] = display_df['Lower Bound (95%)'].apply(lambda x: f"{x:,.0f}")
            display_df['Upper Bound (95%)'] = display_df['Upper Bound (95%)'].apply(lambda x: f"{x:,.0f}")
            st.dataframe(display_df, use_container_width=True)
        
        # Key insights
        st.subheader("🔍 Key Insights")
        
        if change_percent > 0:
            trend_emoji = "📈"
            trend_text = "increasing"
            trend_color = "#ff6b6b"
        else:
            trend_emoji = "📉"
            trend_text = "decreasing"
            trend_color = "#51cf66"
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%); 
                    padding: 1.5rem; border-radius: 12px; border: 1px solid #334155;">
            <p style="color: #e2e8f0; font-size: 1.1rem; margin-bottom: 1rem;">
                {trend_emoji} <strong>Projected Trend:</strong> 
                <span style="color: {trend_color}; font-weight: bold;">{trend_text.upper()}</span>
            </p>
            <ul style="color: #cbd5e1; margin: 0; padding-left: 1.5rem;">
                <li>Deaths from <strong>{pred_cause}</strong> in <strong>{pred_country}</strong> are projected to 
                    <strong>{trend_text}</strong> by <strong>{abs(change_percent):.1f}%</strong> from 2019 to 2030</li>
                <li>This represents an average annual change of <strong>{avg_annual_change:+,.0f}</strong> deaths per year</li>
                <li>Predictions incorporate climate trends: temperature, precipitation, pressure, and wind patterns</li>
                <li>Confidence intervals show 95% probability range for actual outcomes</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.error("⚠️ Prediction data not found. Please run `python scripts/09_temporal_prediction_model.py` first.")
    except Exception as e:
        st.error(f"Error loading predictions: {str(e)}")

with tab6:
    st.header("Random Forest Model - Climate Impact Prediction")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.6) 100%); 
                padding: 1.5rem; border-radius: 12px; border: 1px solid #334155; margin-bottom: 2rem;">
        <h3 style="color: #a78bfa; margin-top: 0;">About this Model</h3>
        <p style="color: #e2e8f0; font-size: 1rem; line-height: 1.6;">
            This Random Forest regressor predicts <strong>Neoplasms (Cancer) mortality rates</strong> based on 
            5 climate variables. The model learns non-linear relationships between environmental conditions 
            and health outcomes across 49 countries.
        </p>
        <p style="color: #cbd5e1; margin-bottom: 0;">
            <strong>Target:</strong> Neoplasms_Rate_per_100k | 
            <strong>Algorithm:</strong> Random Forest (100 trees, max_depth=10) |
            <strong>Data Split:</strong> 80% training, 20% testing
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Train model on-the-fly with caching to avoid compatibility issues
    @st.cache_resource
    def train_rf_model():
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.model_selection import train_test_split
        
        climate_features = ['Temperature_C', 'Precipitation_mm', 'Surface_Pressure_Pa', 'Dewpoint_K', 'Wind_Speed_ms']
        target = 'Neoplasms_Rate_per_100k'
        
        X = df[climate_features]
        y = df[target]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        
        predictions_df = pd.DataFrame({
            'Actual': y_test,
            'Predicted': y_pred,
            'Error': y_test - y_pred
        })
        
        return model, predictions_df
    
    try:
        model, predictions_df = train_rf_model()
        
        # Model Performance Metrics
        st.subheader("Model Performance Metrics")
        
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
        mae = mean_absolute_error(predictions_df['Actual'], predictions_df['Predicted'])
        rmse = np.sqrt(mean_squared_error(predictions_df['Actual'], predictions_df['Predicted']))
        r2 = r2_score(predictions_df['Actual'], predictions_df['Predicted'])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1.5rem; border-radius: 12px; text-align: center;">
                <p style="color: #e2e8f0; font-size: 0.9rem; margin: 0;">Mean Absolute Error</p>
                <h2 style="color: #ffffff; margin: 0.5rem 0;">{mae:.2f}</h2>
                <p style="color: #cbd5e1; font-size: 0.85rem; margin: 0;">deaths per 100k</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 1.5rem; border-radius: 12px; text-align: center;">
                <p style="color: #e2e8f0; font-size: 0.9rem; margin: 0;">Root Mean Squared Error</p>
                <h2 style="color: #ffffff; margin: 0.5rem 0;">{rmse:.2f}</h2>
                <p style="color: #cbd5e1; font-size: 0.85rem; margin: 0;">deaths per 100k</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            r2_color = "#51cf66" if r2 > 0.7 else "#ffd93d" if r2 > 0.5 else "#ff6b6b"
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                        padding: 1.5rem; border-radius: 12px; text-align: center;">
                <p style="color: #e2e8f0; font-size: 0.9rem; margin: 0;">R² Score</p>
                <h2 style="color: {r2_color}; margin: 0.5rem 0;">{r2:.3f}</h2>
                <p style="color: #cbd5e1; font-size: 0.85rem; margin: 0;">variance explained</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Feature Importance
        st.subheader("Climate Variable Importance")
        
        climate_features = ['Temperature_C', 'Precipitation_mm', 'Surface_Pressure_Pa', 'Dewpoint_K', 'Wind_Speed_ms']
        feature_importance_df = pd.DataFrame({
            'Feature': climate_features,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=True)
        
        fig_importance = go.Figure()
        fig_importance.add_trace(go.Bar(
            y=feature_importance_df['Feature'],
            x=feature_importance_df['Importance'],
            orientation='h',
            marker=dict(
                color=feature_importance_df['Importance'],
                colorscale=[[0, '#667eea'], [0.5, '#764ba2'], [1, '#f093fb']],
                showscale=True,
                colorbar=dict(title="Importance", titlefont=dict(color='#ffffff'), tickfont=dict(color='#ffffff'))
            ),
            text=[f"{x:.3f}" for x in feature_importance_df['Importance']],
            textposition='outside',
            textfont=dict(color='#ffffff')
        ))
        
        fig_importance.update_layout(
            template='plotly_dark',
            paper_bgcolor='#0f1419',
            plot_bgcolor='#1e293b',
            font=dict(color='#ffffff', size=14),
            xaxis_title="Importance Score",
            yaxis_title="",
            height=400,
            margin=dict(l=150, r=50, t=50, b=50)
        )
        
        st.plotly_chart(fig_importance, use_container_width=True)
        
        st.markdown("""
        <div style="background: rgba(102, 126, 234, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #667eea; margin-top: 1rem;">
            <p style="color: #e2e8f0; margin: 0; font-size: 0.95rem;">
                <strong>Interpretation:</strong> Higher importance values indicate which climate variables have 
                the strongest predictive power for cancer mortality rates. The model uses these features to 
                make predictions about health outcomes based on environmental conditions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Predictions vs Actual
        st.subheader("Model Predictions vs Actual Values")
        
        fig_scatter = go.Figure()
        
        # Perfect prediction line
        min_val = min(predictions_df['Actual'].min(), predictions_df['Predicted'].min())
        max_val = max(predictions_df['Actual'].max(), predictions_df['Predicted'].max())
        fig_scatter.add_trace(go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode='lines',
            name='Perfect Prediction',
            line=dict(color='#51cf66', width=2, dash='dash'),
            showlegend=True
        ))
        
        # Actual predictions
        fig_scatter.add_trace(go.Scatter(
            x=predictions_df['Actual'],
            y=predictions_df['Predicted'],
            mode='markers',
            name='Predictions',
            marker=dict(
                size=8,
                color=predictions_df['Error'].abs(),
                colorscale=[[0, '#667eea'], [0.5, '#764ba2'], [1, '#f5576c']],
                showscale=True,
                colorbar=dict(title="Absolute Error", titlefont=dict(color='#ffffff'), tickfont=dict(color='#ffffff')),
                line=dict(color='#ffffff', width=0.5)
            ),
            text=[f"Actual: {a:.1f}<br>Predicted: {p:.1f}<br>Error: {e:.1f}" 
                  for a, p, e in zip(predictions_df['Actual'], predictions_df['Predicted'], predictions_df['Error'])],
            hovertemplate='%{text}<extra></extra>'
        ))
        
        fig_scatter.update_layout(
            template='plotly_dark',
            paper_bgcolor='#0f1419',
            plot_bgcolor='#1e293b',
            font=dict(color='#ffffff', size=14),
            xaxis_title="Actual Mortality Rate (per 100k)",
            yaxis_title="Predicted Mortality Rate (per 100k)",
            height=500,
            showlegend=True,
            legend=dict(font=dict(color='#ffffff'))
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Error Distribution
        st.subheader("Prediction Error Distribution")
        
        fig_error = go.Figure()
        fig_error.add_trace(go.Histogram(
            x=predictions_df['Error'],
            nbinsx=30,
            marker=dict(
                color='#667eea',
                line=dict(color='#ffffff', width=1)
            ),
            name='Error Distribution'
        ))
        
        fig_error.update_layout(
            template='plotly_dark',
            paper_bgcolor='#0f1419',
            plot_bgcolor='#1e293b',
            font=dict(color='#ffffff', size=14),
            xaxis_title="Prediction Error (Actual - Predicted)",
            yaxis_title="Frequency",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig_error, use_container_width=True)
        
        # Interactive Predictor
        st.subheader("Interactive Climate-Based Predictor")
        
        st.markdown("""
        <div style="background: rgba(167, 139, 250, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #a78bfa; margin-bottom: 1.5rem;">
            <p style="color: #e2e8f0; margin: 0; font-size: 0.95rem;">
                Adjust the climate variables below to see how they impact predicted cancer mortality rates. 
                This demonstrates the model's learned relationships between environmental conditions and health outcomes.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            temp_input = st.slider(
                "Temperature (°C)",
                min_value=-10.0,
                max_value=35.0,
                value=15.0,
                step=0.5
            )
            
            precip_input = st.slider(
                "Precipitation (mm)",
                min_value=0.0,
                max_value=200.0,
                value=60.0,
                step=5.0
            )
            
            pressure_input = st.slider(
                "Surface Pressure (Pa)",
                min_value=95000.0,
                max_value=105000.0,
                value=101325.0,
                step=100.0
            )
        
        with col2:
            dewpoint_input = st.slider(
                "Dewpoint (K)",
                min_value=250.0,
                max_value=300.0,
                value=280.0,
                step=1.0
            )
            
            wind_input = st.slider(
                "Wind Speed (m/s)",
                min_value=0.0,
                max_value=15.0,
                value=4.0,
                step=0.5
            )
        
        # Make prediction
        input_data = pd.DataFrame({
            'Temperature_C': [temp_input],
            'Precipitation_mm': [precip_input],
            'Surface_Pressure_Pa': [pressure_input],
            'Dewpoint_K': [dewpoint_input],
            'Wind_Speed_ms': [wind_input]
        })
        
        prediction = model.predict(input_data)[0]
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 16px; text-align: center; margin-top: 2rem;">
            <p style="color: #e2e8f0; font-size: 1.2rem; margin: 0 0 1rem 0;">Predicted Neoplasms Mortality Rate</p>
            <h1 style="color: #ffffff; margin: 0; font-size: 3rem;">{prediction:.2f}</h1>
            <p style="color: #cbd5e1; font-size: 1rem; margin: 1rem 0 0 0;">deaths per 100,000 population</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Detailed predictions table
        with st.expander("View Detailed Predictions Data"):
            st.dataframe(
                predictions_df.style.format({
                    'Actual': '{:.2f}',
                    'Predicted': '{:.2f}',
                    'Error': '{:.2f}'
                }),
                use_container_width=True
            )
        
    except FileNotFoundError as e:
        st.error(f"Model files not found. Please run `python scripts/08_predictive_modeling.py` first.")
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")

st.sidebar.markdown("---")