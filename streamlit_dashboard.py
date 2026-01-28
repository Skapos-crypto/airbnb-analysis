"""
Airbnb Pricing Analysis Dashboard - Streamlit Version
=====================================================
Interactive visualization of pricing patterns across European cities
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import streamlit as st
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Airbnb Pricing Analysis",
    page_icon="🏠",
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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    h1 {
        color: #2c3e50;
    }
    h2 {
        color: #2c3e50;
        border-bottom: 3px solid #3498db;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    df = pd.read_csv('dataset.csv')
    return df

# Load and process data
with st.spinner('Loading data...'):
    df = load_data()

# City aggregations
city_summary = df.groupby('city').agg({
    'realSum': ['mean', 'count'],
    'population': 'first',
    'tourist_arrivals': 'first',
    'tourism_pressure_ratio': 'first',
    'guest_satisfaction_overall': 'mean',
    'airport_distance_km': 'mean',
    'city_avg_price': 'first',
    'price_per_person': 'mean'
}).reset_index()

city_summary.columns = ['city', 'avg_price', 'total_listings', 'population', 
                        'tourist_arrivals', 'tourism_pressure_ratio',
                        'avg_satisfaction', 'avg_airport_dist', 'city_avg_price',
                        'avg_price_per_person']

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 30px; border-radius: 10px; margin-bottom: 30px;'>
    <h1 style='color: white; text-align: center; margin: 0;'>
        🏠 Airbnb Pricing Analysis: European Cities
    </h1>
    <p style='color: white; text-align: center; margin: 10px 0 0 0; font-size: 16px;'>
        Analysis of 52,810 Listings Across 10 Major European Destinations
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# KEY METRICS
# ============================================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📊 Total Listings",
        value=f"{len(df):,}"
    )

with col2:
    st.metric(
        label="🌍 European Cities",
        value=f"{df['city'].nunique()}"
    )

with col3:
    st.metric(
        label="💰 Avg Nightly Price",
        value=f"€{df['realSum'].mean():.0f}"
    )

with col4:
    st.metric(
        label="🔢 Total Features",
        value=f"{len(df.columns)}"
    )

st.markdown("---")

# ============================================================================
# SIDEBAR FILTERS
# ============================================================================

with st.sidebar:
    st.header("🎛️ Filters")
    
    selected_cities = st.multiselect(
        "Select Cities",
        options=sorted(df['city'].unique()),
        default=sorted(df['city'].unique())
    )
    
    price_range = st.slider(
        "Price Range (€)",
        min_value=int(df['realSum'].min()),
        max_value=int(df['realSum'].max()),
        value=(int(df['realSum'].min()), int(df['realSum'].max()))
    )
    
    st.markdown("---")
    st.markdown("### 📈 Dataset Statistics")
    st.write(f"**Listings shown:** {len(df[df['city'].isin(selected_cities)]):,}")
    st.write(f"**Cities:** {len(selected_cities)}")
    st.write(f"**Avg Price:** €{df[df['city'].isin(selected_cities)]['realSum'].mean():.0f}")

# Filter data based on selections
df_filtered = df[
    (df['city'].isin(selected_cities)) & 
    (df['realSum'] >= price_range[0]) & 
    (df['realSum'] <= price_range[1])
]

city_summary_filtered = city_summary[city_summary['city'].isin(selected_cities)]

# ============================================================================
# TOURISM ANALYSIS
# ============================================================================

st.header("🌍 Tourism Demand Analysis")

# Tourism intensity scatter
fig_tourism = px.scatter(
    city_summary_filtered,
    x='tourism_pressure_ratio',
    y='avg_price',
    size='total_listings',
    color='avg_price',
    text='city',
    title='Tourism Pressure Ratio vs Average Nightly Price',
    labels={'tourism_pressure_ratio': 'Tourism Pressure Ratio (Annual Tourists per Resident)',
            'avg_price': 'Average Nightly Price (€)'},
    color_continuous_scale='Viridis',
    size_max=50
)

fig_tourism.update_traces(textposition='top center', textfont=dict(size=11, color='black'))
fig_tourism.update_layout(height=500, showlegend=False, font=dict(size=12))

if len(city_summary_filtered) > 1:
    corr = city_summary_filtered['tourism_pressure_ratio'].corr(city_summary_filtered['avg_price'])
    fig_tourism.add_annotation(
        text=f"Pearson Correlation: {corr:.3f}",
        xref="paper", yref="paper",
        x=0.02, y=0.98,
        showarrow=False,
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="black",
        borderwidth=2,
        font=dict(size=14, color="black")
    )

st.plotly_chart(fig_tourism, use_container_width=True)

st.markdown("---")

# ============================================================================
# LOCATION AND ACCESSIBILITY
# ============================================================================

st.header("📍 Location and Accessibility Impact")

col1, col2 = st.columns(2)

with col1:
    # Distance from city center
    dist_stats = df_filtered.groupby('distance_bin', observed=True).agg({
        'realSum': ['mean', 'count']
    }).reset_index()
    
    dist_stats.columns = ['distance_bin', 'avg_price', 'count']
    dist_stats = dist_stats.dropna()
    
    fig_distance = go.Figure()
    
    fig_distance.add_trace(go.Bar(
        x=dist_stats['distance_bin'],
        y=dist_stats['avg_price'],
        marker_color='steelblue',
        text=dist_stats['avg_price'].round(0),
        texttemplate='€%{text}',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Avg Price: €%{y:.0f}<br>Listings: %{customdata}<extra></extra>',
        customdata=dist_stats['count']
    ))
    
    fig_distance.update_layout(
        title='Average Price by Distance from City Center',
        xaxis_title='Distance from City Center',
        yaxis_title='Average Nightly Price (€)',
        height=450,
        font=dict(size=12)
    )
    
    st.plotly_chart(fig_distance, use_container_width=True)

with col2:
    # Metro accessibility
    metro_data = df_filtered.groupby('metro_accessibility', observed=True)['realSum'].mean().reset_index()
    metro_data.columns = ['metro_accessibility', 'avg_price']
    metro_data = metro_data.dropna()
    
    fig_metro = go.Figure()
    
    colors = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c']
    
    fig_metro.add_trace(go.Bar(
        x=metro_data['metro_accessibility'],
        y=metro_data['avg_price'],
        marker_color=colors[:len(metro_data)],
        text=metro_data['avg_price'].round(0),
        texttemplate='€%{text}',
        textposition='outside'
    ))
    
    fig_metro.update_layout(
        title='Average Price by Metro Station Proximity',
        xaxis_title='Distance to Nearest Metro Station',
        yaxis_title='Average Nightly Price (€)',
        height=450,
        showlegend=False,
        font=dict(size=12)
    )
    
    st.plotly_chart(fig_metro, use_container_width=True)

# Airport distance analysis
airport_stats = df_filtered.groupby('airport_distance_bin', observed=True).agg({
    'realSum': 'mean',
    'guest_satisfaction_overall': 'mean'
}).reset_index()

airport_stats.columns = ['distance_bin', 'avg_price', 'satisfaction']
airport_stats = airport_stats.dropna()

fig_airport = make_subplots(specs=[[{"secondary_y": True}]])

fig_airport.add_trace(
    go.Bar(x=airport_stats['distance_bin'], y=airport_stats['avg_price'],
           name='Average Price', marker_color='#3498db'),
    secondary_y=False,
)

fig_airport.add_trace(
    go.Scatter(x=airport_stats['distance_bin'], y=airport_stats['satisfaction'],
               name='Guest Satisfaction', mode='lines+markers',
               line=dict(color='#e74c3c', width=3), marker=dict(size=10)),
    secondary_y=True,
)

fig_airport.update_layout(
    title='Price and Satisfaction by Distance to Airport',
    height=450,
    font=dict(size=12)
)

fig_airport.update_xaxes(title_text="Distance to Nearest Major Airport")
fig_airport.update_yaxes(title_text="Average Nightly Price (€)", secondary_y=False)
fig_airport.update_yaxes(title_text="Guest Satisfaction Score", secondary_y=True)

st.plotly_chart(fig_airport, use_container_width=True)

st.markdown("---")

# ============================================================================
# PRICE ANALYSIS
# ============================================================================

st.header("💰 Price Distribution and Comparison")

# City comparison
city_sorted = city_summary_filtered.sort_values('avg_price', ascending=True)

fig_city_comp = go.Figure()

fig_city_comp.add_trace(go.Bar(
    y=city_sorted['city'],
    x=city_sorted['avg_price'],
    orientation='h',
    marker_color=city_sorted['avg_price'],
    marker_colorscale='Viridis',
    text=city_sorted['avg_price'].round(0),
    texttemplate='€%{text}',
    textposition='outside',
    hovertemplate='<b>%{y}</b><br>Price: €%{x:.0f}<br>Listings: %{customdata[0]}<br>Tourism Ratio: %{customdata[1]:.2f}<extra></extra>',
    customdata=np.column_stack((city_sorted['total_listings'], city_sorted['tourism_pressure_ratio']))
))

fig_city_comp.update_layout(
    title='Average Nightly Price by City',
    xaxis_title='Average Nightly Price (€)',
    height=500,
    font=dict(size=12)
)

st.plotly_chart(fig_city_comp, use_container_width=True)

# Price distribution
fig_price_dist = go.Figure()

for city in sorted(df_filtered['city'].unique()):
    city_df = df_filtered[df_filtered['city'] == city]
    fig_price_dist.add_trace(go.Box(
        y=city_df['realSum'],
        name=city.capitalize(),
        boxmean='sd'
    ))

fig_price_dist.update_layout(
    title='Price Distribution by City (with Standard Deviation)',
    yaxis_title='Nightly Price (€)',
    height=500,
    showlegend=True,
    font=dict(size=12)
)

st.plotly_chart(fig_price_dist, use_container_width=True)

# Price per person
room_analysis = df_filtered.groupby('room_type').agg({
    'price_per_person': 'mean',
    'realSum': 'mean',
    'person_capacity': 'mean'
}).round(2).reset_index()

fig_price_per_person = go.Figure()

fig_price_per_person.add_trace(go.Bar(
    x=room_analysis['room_type'],
    y=room_analysis['price_per_person'],
    marker_color=['#3498db', '#2ecc71', '#f39c12'],
    text=room_analysis['price_per_person'].round(0),
    texttemplate='€%{text}/person',
    textposition='outside'
))

fig_price_per_person.update_layout(
    title='Average Price per Person by Room Type',
    xaxis_title='Room Type',
    yaxis_title='Price per Person (€)',
    height=450,
    font=dict(size=12)
)

st.plotly_chart(fig_price_per_person, use_container_width=True)

st.markdown("---")

# ============================================================================
# CORRELATION ANALYSIS
# ============================================================================

st.header("🔬 Feature Correlation Analysis")

key_features = [
    'realSum', 'tourism_pressure_ratio', 'airport_distance_km',
    'dist', 'metro_dist', 'guest_satisfaction_overall',
    'price_per_person', 'city_avg_price'
]

corr_matrix = df_filtered[key_features].corr()

fig_corr = go.Figure(data=go.Heatmap(
    z=corr_matrix.values,
    x=corr_matrix.columns,
    y=corr_matrix.columns,
    colorscale='RdBu',
    zmid=0,
    text=corr_matrix.values.round(2),
    texttemplate='%{text}',
    textfont={"size": 10},
    colorbar=dict(title="Correlation")
))

fig_corr.update_layout(
    title='Correlation Matrix of Key Features',
    height=600,
    font=dict(size=10)
)

st.plotly_chart(fig_corr, use_container_width=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 20px;'>
    <p>📊 Data Analysis | 52,810 listings | 10 European cities | Real-time airport data from OpenFlights.org</p>
</div>
""", unsafe_allow_html=True)
