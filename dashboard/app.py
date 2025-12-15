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
    /* Main title styling */
    .main-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(120deg, #2193b0, #6dd5ed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
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
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
        color: white;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    section[data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 600;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3.5rem;
        background-color: white;
        border-radius: 8px;
        padding: 0 1.5rem;
        font-weight: 600;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f1f5f9;
        border-color: #cbd5e1;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border-color: transparent;
    }
    
    /* Cards for content sections */
    .content-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid #3b82f6;
    }
    
    /* Dataframes */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
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
    
    /* Headers */
    h1, h2, h3 {
        color: #1e293b;
    }
    
    h2 {
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 8px;
    }
    
    /* Multiselect */
    .stMultiSelect > div > div {
        border-radius: 8px;
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
st.markdown('<h1 class="main-title">🌍 Climate & Health Analytics Platform</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Comprehensive analysis of climate-mortality relationships across 49 countries (1990-2019)</p>', unsafe_allow_html=True)

st.markdown("---")

st.sidebar.header("Filters")

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=sorted(df['Country/Territory'].unique()),
    default=['Germany', 'United States', 'China', 'Brazil']
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
    
    fig = px.line(
        filtered_df,
        x='Year',
        y=climate_var,
        color='Country/Territory',
        title=f'{climate_var} Evolution Over Time'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Temperature Distribution by Country")
    fig2 = px.box(
        filtered_df,
        x='Country/Territory',
        y='Temperature_C',
        title='Temperature Distribution'
    )
    fig2.update_xaxes(tickangle=45)
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.header("Mortality Analysis")
    
    rate_cols = [col for col in df.columns if col.endswith('_Rate_per_100k')]
    
    selected_cause = st.selectbox(
        "Select Cause of Death",
        [col.replace('_Rate_per_100k', '') for col in rate_cols]
    )
    
    rate_col = f'{selected_cause}_Rate_per_100k'
    
    fig = px.line(
        filtered_df,
        x='Year',
        y=rate_col,
        color='Country/Territory',
        title=f'{selected_cause} - Death Rate per 100k'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader(f"Average {selected_cause} Rate by Country")
    avg_by_country = filtered_df.groupby('Country/Territory')[rate_col].mean().sort_values(ascending=False)
    
    fig2 = px.bar(
        x=avg_by_country.index,
        y=avg_by_country.values,
        labels={'x': 'Country', 'y': 'Average Rate per 100k'},
        title=f'Average {selected_cause} Rate by Country'
    )
    fig2.update_xaxes(tickangle=45)
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
    
    fig = px.bar(
        top_corr,
        x='Correlation',
        y=[f"{row['Cause'][:25]} vs {row['Climate_Variable']}" for _, row in top_corr.iterrows()],
        orientation='h',
        title=f'Top {top_n} Climate-Mortality Correlations ({corr_type})',
        color='Correlation',
        color_continuous_scale='RdBu_r'
    )
    fig.update_layout(height=600)
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
        aspect="auto"
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.info("Dashboard created with Streamlit")