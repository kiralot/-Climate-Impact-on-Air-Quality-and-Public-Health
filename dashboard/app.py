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
    default=['United States', 'Germany', 'India', 'Italy', 'Japan', 'United Kingdom']
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

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Climate Trends", "Mortality Analysis", "Correlations"])

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

st.sidebar.markdown("---")