"""
Airbnb Pricing Analysis Dashboard - Streamlit Version
=====================================================
Interactive visualization of pricing patterns across European cities
"""

import pandas as pd
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
        Analysis of 51,707 Listings Across 10 Major European Destinations
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
st.subheader("Tourism Pressure Ratio vs Average Nightly Price")

if len(city_summary_filtered) > 1:
    corr = city_summary_filtered['tourism_pressure_ratio'].corr(city_summary_filtered['avg_price'])
    st.info(f"📊 **Pearson Correlation: {corr:.3f}**")

# Create scatter chart data
scatter_data = city_summary_filtered[['city', 'tourism_pressure_ratio', 'avg_price', 'total_listings']].copy()
scatter_data = scatter_data.sort_values('tourism_pressure_ratio')

st.scatter_chart(
    scatter_data,
    x='tourism_pressure_ratio',
    y='avg_price',
    size='total_listings',
    color='city',
    height=500
)

# Display data table
st.write("**City Details:**")
display_df = city_summary_filtered[['city', 'tourism_pressure_ratio', 'avg_price', 'total_listings']].copy()
display_df.columns = ['City', 'Tourism Pressure Ratio', 'Avg Price (€)', 'Total Listings']
display_df['Avg Price (€)'] = display_df['Avg Price (€)'].round(0)
display_df['Tourism Pressure Ratio'] = display_df['Tourism Pressure Ratio'].round(2)
st.dataframe(display_df, use_container_width=True, hide_index=True)

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
    st.subheader("Price by Distance from City Center")
    
    dist_stats = df_filtered.groupby('distance_bin', observed=True).agg({
        'realSum': ['mean', 'count']
    }).reset_index()
    
    dist_stats.columns = ['distance_bin', 'avg_price', 'count']
    dist_stats = dist_stats.dropna()
    
    # Create chart data
    chart_data = dist_stats.set_index('distance_bin')['avg_price']
    st.bar_chart(chart_data, height=400)
    
    # Show statistics
    st.write("**Statistics:**")
    for _, row in dist_stats.iterrows():
        st.write(f"**{row['distance_bin']}**: €{row['avg_price']:.0f} ({int(row['count'])} listings)")

with col2:
    # Metro accessibility
    st.subheader("Price by Metro Station Proximity")
    
    metro_data = df_filtered.groupby('metro_accessibility', observed=True)['realSum'].mean().reset_index()
    metro_data.columns = ['metro_accessibility', 'avg_price']
    metro_data = metro_data.dropna()
    
    metro_data = df_filtered.groupby('metro_accessibility', observed=True)['realSum'].mean().reset_index()
    metro_data.columns = ['metro_accessibility', 'avg_price']
    metro_data = metro_data.dropna()
    
    # Create chart
    chart_data = metro_data.set_index('metro_accessibility')['avg_price']
    st.bar_chart(chart_data, height=400)
    
    # Show statistics
    st.write("**Statistics:**")
    for _, row in metro_data.iterrows():
        st.write(f"**{row['metro_accessibility']}**: €{row['avg_price']:.0f}")

# Airport distance analysis
st.subheader("Price and Satisfaction by Distance to Airport")

airport_stats = df_filtered.groupby('airport_distance_bin', observed=True).agg({
    'realSum': 'mean',
    'guest_satisfaction_overall': 'mean'
}).reset_index()

airport_stats.columns = ['distance_bin', 'avg_price', 'satisfaction']
airport_stats = airport_stats.dropna()

# Create two columns for dual axis effect
col_a, col_b = st.columns(2)

with col_a:
    st.write("**Average Price (€)**")
    chart_data = airport_stats.set_index('distance_bin')['avg_price']
    st.bar_chart(chart_data, height=350)

with col_b:
    st.write("**Guest Satisfaction Score**")
    chart_data = airport_stats.set_index('distance_bin')['satisfaction']
    st.line_chart(chart_data, height=350, color="#e74c3c")

# Show combined statistics
st.write("**Combined Statistics:**")
display_airport = airport_stats.copy()
display_airport['avg_price'] = display_airport['avg_price'].round(0)
display_airport['satisfaction'] = display_airport['satisfaction'].round(2)
display_airport.columns = ['Distance to Airport', 'Avg Price (€)', 'Satisfaction Score']
st.dataframe(display_airport, use_container_width=True, hide_index=True)

st.markdown("---")

# ============================================================================
# PRICE ANALYSIS
# ============================================================================

st.header("💰 Price Distribution and Comparison")

# City comparison
st.subheader("Average Nightly Price by City")

city_sorted = city_summary_filtered.sort_values('avg_price', ascending=False)

# Create horizontal bar chart
chart_data = city_sorted.set_index('city')['avg_price']
st.bar_chart(chart_data, height=500, horizontal=True)

# Show detailed city data
st.write("**City Comparison Details:**")
display_city = city_sorted[['city', 'avg_price', 'total_listings', 'tourism_pressure_ratio']].copy()
display_city['avg_price'] = display_city['avg_price'].round(0)
display_city['tourism_pressure_ratio'] = display_city['tourism_pressure_ratio'].round(2)
display_city.columns = ['City', 'Avg Price (€)', 'Total Listings', 'Tourism Ratio']
st.dataframe(display_city, use_container_width=True, hide_index=True)

# Price distribution
st.subheader("Price Distribution by City")

# Calculate statistics for each city
price_stats = []
for city in sorted(df_filtered['city'].unique()):
    city_df = df_filtered[df_filtered['city'] == city]
    price_stats.append({
        'City': city.capitalize(),
        'Mean': city_df['realSum'].mean(),
        'Median': city_df['realSum'].median(),
        'Std Dev': city_df['realSum'].std(),
        'Min': city_df['realSum'].min(),
        'Max': city_df['realSum'].max()
    })

stats_df = pd.DataFrame(price_stats)

# Create area chart for price ranges
chart_data = stats_df.set_index('City')[['Min', 'Mean', 'Max']]
st.area_chart(chart_data, height=400)

# Display statistics table
st.write("**Price Statistics by City:**")
display_stats = stats_df.copy()
for col in ['Mean', 'Median', 'Std Dev', 'Min', 'Max']:
    display_stats[col] = display_stats[col].round(0)
st.dataframe(display_stats, use_container_width=True, hide_index=True)

# Price per person
st.subheader("Average Price per Person by Room Type")

room_analysis = df_filtered.groupby('room_type').agg({
    'price_per_person': 'mean',
    'realSum': 'mean',
    'person_capacity': 'mean'
}).round(2).reset_index()

# Create bar chart
chart_data = room_analysis.set_index('room_type')['price_per_person']
st.bar_chart(chart_data, height=400)

# Show detailed room type data
st.write("**Room Type Analysis:**")
display_room = room_analysis.copy()
display_room.columns = ['Room Type', 'Price per Person (€)', 'Avg Total Price (€)', 'Avg Capacity']
display_room['Price per Person (€)'] = display_room['Price per Person (€)'].round(0)
display_room['Avg Total Price (€)'] = display_room['Avg Total Price (€)'].round(0)
display_room['Avg Capacity'] = display_room['Avg Capacity'].round(1)
st.dataframe(display_room, use_container_width=True, hide_index=True)

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

# Display correlation matrix as dataframe
st.write("**Correlation Matrix of Key Features**")
st.write("Values range from -1 (negative correlation) to +1 (positive correlation)")

# Format the dataframe
corr_display = corr_matrix.round(2)
st.dataframe(corr_display, use_container_width=True)

# Show top correlations
st.write("**Top Positive Correlations:**")
# Get upper triangle of correlation matrix
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
corr_matrix_masked = corr_matrix.mask(mask)

# Find top correlations
correlations = []
for i in range(len(corr_matrix_masked.columns)):
    for j in range(len(corr_matrix_masked.columns)):
        if not pd.isna(corr_matrix_masked.iloc[i, j]):
            correlations.append({
                'Feature 1': corr_matrix_masked.columns[i],
                'Feature 2': corr_matrix_masked.index[j],
                'Correlation': corr_matrix_masked.iloc[i, j]
            })

corr_df = pd.DataFrame(correlations).sort_values('Correlation', ascending=False)
st.dataframe(corr_df.head(10), use_container_width=True, hide_index=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 20px;'>
    <p>📊 Data Analysis | 51,707 listings | 10 European cities | Real-time airport data from OpenFlights.org</p>
</div>
""", unsafe_allow_html=True)