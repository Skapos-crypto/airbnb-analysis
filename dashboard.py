"""
Airbnb Pricing Analysis Dashboard
==================================
Interactive visualization of pricing patterns across European cities
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from dash import Dash, dcc, html
import warnings
warnings.filterwarnings('ignore')

# Load data
print("Loading data...")
df = pd.read_csv('dataset.csv')

print(f"✓ Loaded {len(df):,} listings across {df['city'].nunique()} cities")
print(f"✓ Total features: {len(df.columns)}")

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
# VISUALIZATIONS
# ============================================================================

def create_key_metrics():
    """Key metrics cards"""
    total_listings = len(df)
    total_cities = df['city'].nunique()
    avg_price = df['realSum'].mean()
    total_features = len(df.columns)
    
    return html.Div([
        html.Div([
            html.Div([
                html.H3(f"{total_listings:,}", style={'color': 'white', 'margin': '0'}),
                html.P("Total Listings", style={'color': 'white', 'margin': '5px 0', 'opacity': '0.9'})
            ], style={'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                     'padding': '20px', 'borderRadius': '10px', 'flex': '1', 'margin': '0 10px'}),
            
            html.Div([
                html.H3(f"{total_cities}", style={'color': 'white', 'margin': '0'}),
                html.P("European Cities", style={'color': 'white', 'margin': '5px 0', 'opacity': '0.9'})
            ], style={'background': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                     'padding': '20px', 'borderRadius': '10px', 'flex': '1', 'margin': '0 10px'}),
            
            html.Div([
                html.H3(f"€{avg_price:.0f}", style={'color': 'white', 'margin': '0'}),
                html.P("Average Nightly Price", style={'color': 'white', 'margin': '5px 0', 'opacity': '0.9'})
            ], style={'background': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                     'padding': '20px', 'borderRadius': '10px', 'flex': '1', 'margin': '0 10px'}),
            
            html.Div([
                html.H3(f"{total_features}", style={'color': 'white', 'margin': '0'}),
                html.P("Total Features", style={'color': 'white', 'margin': '5px 0', 'opacity': '0.9'})
            ], style={'background': 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
                     'padding': '20px', 'borderRadius': '10px', 'flex': '1', 'margin': '0 10px'}),
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '30px'})
    ])

def create_tourism_intensity_scatter():
    """Tourism intensity vs price correlation analysis"""
    fig = px.scatter(
        city_summary,
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
    
    fig.update_traces(textposition='top center', textfont=dict(size=11, color='black'))
    fig.update_layout(height=500, showlegend=False, font=dict(size=12))
    
    corr = city_summary['tourism_pressure_ratio'].corr(city_summary['avg_price'])
    fig.add_annotation(
        text=f"Pearson Correlation: {corr:.3f}",
        xref="paper", yref="paper",
        x=0.02, y=0.98,
        showarrow=False,
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="black",
        borderwidth=2,
        font=dict(size=14, color="black")
    )
    
    return fig

def create_airport_distance_analysis():
    """Airport proximity impact on pricing"""
    airport_stats = df.groupby('airport_distance_bin', observed=True).agg({
        'realSum': 'mean',
        'guest_satisfaction_overall': 'mean'
    }).reset_index()
    
    airport_stats.columns = ['distance_bin', 'avg_price', 'satisfaction']
    airport_stats = airport_stats.dropna()
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(x=airport_stats['distance_bin'], y=airport_stats['avg_price'],
               name='Average Price', marker_color='#3498db'),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(x=airport_stats['distance_bin'], y=airport_stats['satisfaction'],
                   name='Guest Satisfaction', mode='lines+markers',
                   line=dict(color='#e74c3c', width=3), marker=dict(size=10)),
        secondary_y=True,
    )
    
    fig.update_layout(
        title='Price and Satisfaction by Distance to Airport',
        height=450,
        font=dict(size=12)
    )
    
    fig.update_xaxes(title_text="Distance to Nearest Major Airport")
    fig.update_yaxes(title_text="Average Nightly Price (€)", secondary_y=False)
    fig.update_yaxes(title_text="Guest Satisfaction Score", secondary_y=True)
    
    return fig

def create_distance_decay():
    """Distance from city center pricing analysis"""
    dist_stats = df.groupby('distance_bin', observed=True).agg({
        'realSum': ['mean', 'count']
    }).reset_index()
    
    dist_stats.columns = ['distance_bin', 'avg_price', 'count']
    dist_stats = dist_stats.dropna()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=dist_stats['distance_bin'],
        y=dist_stats['avg_price'],
        marker_color='steelblue',
        text=dist_stats['avg_price'].round(0),
        texttemplate='€%{text}',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Avg Price: €%{y:.0f}<br>Listings: %{customdata}<extra></extra>',
        customdata=dist_stats['count']
    ))
    
    fig.update_layout(
        title='Average Price by Distance from City Center',
        xaxis_title='Distance from City Center',
        yaxis_title='Average Nightly Price (€)',
        height=450,
        font=dict(size=12)
    )
    
    return fig

def create_metro_accessibility():
    """Metro accessibility impact analysis"""
    metro_data = df.groupby('metro_accessibility', observed=True)['realSum'].mean().reset_index()
    metro_data.columns = ['metro_accessibility', 'avg_price']
    metro_data = metro_data.dropna()
    
    fig = go.Figure()
    
    colors = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c']
    
    fig.add_trace(go.Bar(
        x=metro_data['metro_accessibility'],
        y=metro_data['avg_price'],
        marker_color=colors[:len(metro_data)],
        text=metro_data['avg_price'].round(0),
        texttemplate='€%{text}',
        textposition='outside'
    ))
    
    fig.update_layout(
        title='Average Price by Metro Station Proximity',
        xaxis_title='Distance to Nearest Metro Station',
        yaxis_title='Average Nightly Price (€)',
        height=450,
        showlegend=False,
        font=dict(size=12)
    )
    
    return fig

def create_city_comparison():
    """City-by-city price comparison"""
    city_sorted = city_summary.sort_values('avg_price', ascending=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
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
    
    fig.update_layout(
        title='Average Nightly Price by City',
        xaxis_title='Average Nightly Price (€)',
        height=500,
        font=dict(size=12)
    )
    
    return fig

def create_price_distribution():
    """Price distribution across cities"""
    fig = go.Figure()
    
    for city in sorted(df['city'].unique()):
        city_df = df[df['city'] == city]
        fig.add_trace(go.Box(
            y=city_df['realSum'],
            name=city.capitalize(),
            boxmean='sd'
        ))
    
    fig.update_layout(
        title='Price Distribution by City (with Standard Deviation)',
        yaxis_title='Nightly Price (€)',
        height=500,
        showlegend=True,
        font=dict(size=12)
    )
    
    return fig

def create_price_per_person_analysis():
    """Price efficiency by room type"""
    room_analysis = df.groupby('room_type').agg({
        'price_per_person': 'mean',
        'realSum': 'mean',
        'person_capacity': 'mean'
    }).round(2).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=room_analysis['room_type'],
        y=room_analysis['price_per_person'],
        marker_color=['#3498db', '#2ecc71', '#f39c12'],
        text=room_analysis['price_per_person'].round(0),
        texttemplate='€%{text}/person',
        textposition='outside'
    ))
    
    fig.update_layout(
        title='Average Price per Person by Room Type',
        xaxis_title='Room Type',
        yaxis_title='Price per Person (€)',
        height=450,
        font=dict(size=12)
    )
    
    return fig

def create_correlation_heatmap():
    """Feature correlation analysis"""
    key_features = [
        'realSum', 'tourism_pressure_ratio', 'airport_distance_km',
        'dist', 'metro_dist', 'guest_satisfaction_overall',
        'price_per_person', 'city_avg_price'
    ]
    
    corr_matrix = df[key_features].corr()
    
    fig = go.Figure(data=go.Heatmap(
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
    
    fig.update_layout(
        title='Correlation Matrix of Key Features',
        height=600,
        font=dict(size=10)
    )
    
    return fig

# ============================================================================
# BUILD DASHBOARD
# ============================================================================

app = Dash(__name__)

app.layout = html.Div([
    # Header
    html.Div([
        html.H1('Airbnb Pricing Analysis: European Cities', 
                style={'color': 'white', 'textAlign': 'center', 'margin': '0', 'padding': '30px'}),
        html.P('Analysis of 52,810 Listings Across 10 Major European Destinations',
               style={'color': 'white', 'textAlign': 'center', 'margin': '0', 'fontSize': '16px'})
    ], style={'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 'marginBottom': '30px'}),
    
    # Key Metrics
    html.Div([
        create_key_metrics()
    ], style={'padding': '0 30px'}),
    
    # Main Content
    html.Div([
        # Tourism Analysis
        html.Div([
            html.H2('Tourism Demand Analysis', style={'color': '#2c3e50', 'borderBottom': '3px solid #3498db', 'paddingBottom': '10px'}),
            dcc.Graph(figure=create_tourism_intensity_scatter()),
        ], style={'marginBottom': '50px'}),
        
        # Location Analysis
        html.Div([
            html.H2('Location and Accessibility Impact', style={'color': '#2c3e50', 'borderBottom': '3px solid #2ecc71', 'paddingBottom': '10px'}),
            
            html.Div([
                html.Div([dcc.Graph(figure=create_distance_decay())], style={'flex': '1'}),
                html.Div([dcc.Graph(figure=create_metro_accessibility())], style={'flex': '1'})
            ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '30px'}),
            
            dcc.Graph(figure=create_airport_distance_analysis()),
        ], style={'marginBottom': '50px'}),
        
        # Price Analysis
        html.Div([
            html.H2('Price Distribution and Comparison', style={'color': '#2c3e50', 'borderBottom': '3px solid #f39c12', 'paddingBottom': '10px'}),
            dcc.Graph(figure=create_city_comparison()),
            dcc.Graph(figure=create_price_distribution()),
            dcc.Graph(figure=create_price_per_person_analysis()),
        ], style={'marginBottom': '50px'}),
        
        # Correlation Analysis
        html.Div([
            html.H2('Feature Correlation Analysis', style={'color': '#2c3e50', 'borderBottom': '3px solid #9b59b6', 'paddingBottom': '10px'}),
            dcc.Graph(figure=create_correlation_heatmap()),
        ], style={'marginBottom': '50px'}),
        
    ], style={'padding': '0 30px'}),
    
    # Footer
    html.Div([
        html.P('Data Analysis | 52,810 listings | 10 European cities | Real-time airport data from OpenFlights.org',
               style={'textAlign': 'center', 'color': '#7f8c8d', 'margin': '0', 'padding': '20px'})
    ], style={'marginTop': '50px', 'borderTop': '1px solid #ecf0f1'})
])

# ============================================================================
# RUN DASHBOARD
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("LAUNCHING DASHBOARD")
    print("="*70)
    print("\n✓ Dashboard starting...")
    print("✓ Navigate to: http://127.0.0.1:8050")
    print("✓ Press Ctrl+C to stop\n")
    
    app.run(debug=True, port=8050)
