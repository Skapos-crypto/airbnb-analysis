"""
Streamlined Dataset Builder
===========================
Keeps only essential columns for hackathon presentation:
- All 21 original CSV columns
- city_avg_price
- distance_bin
- metro_accessibility
- airport_distance_km
- airport_distance_bin
- price_per_person
- tourism_pressure_ratio (tourists per resident)
"""

import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
import requests
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# EXTERNAL DATA (Curated)
# ============================================================================

CITY_DATA = {
    'amsterdam': {'population': 872680, 'tourist_arrivals': 9000000},
    'athens': {'population': 664046, 'tourist_arrivals': 5500000},
    'barcelona': {'population': 1620809, 'tourist_arrivals': 12000000},
    'berlin': {'population': 3769495, 'tourist_arrivals': 14000000},
    'budapest': {'population': 1752286, 'tourist_arrivals': 4400000},
    'lisbon': {'population': 504718, 'tourist_arrivals': 7000000},
    'london': {'population': 9002488, 'tourist_arrivals': 21000000},
    'paris': {'population': 2165423, 'tourist_arrivals': 19100000},
    'rome': {'population': 2860009, 'tourist_arrivals': 10000000},
    'vienna': {'population': 1911191, 'tourist_arrivals': 7500000}
}

# ============================================================================
# SCRAPE OPENFLIGHTS API
# ============================================================================

def scrape_openflights_api():
    """Scrape airport data from OpenFlights.org GitHub repository"""
    print("\n" + "="*70)
    print("SCRAPING OPENFLIGHTS.ORG API")
    print("="*70)
    
    url = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat"
    
    try:
        print(f"\n→ Fetching: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print(f"✓ Successfully retrieved data ({len(response.content):,} bytes)")
        
        columns = ['airport_id', 'name', 'city', 'country', 'iata', 'icao', 
                   'latitude', 'longitude', 'altitude', 'timezone', 'dst', 
                   'tz_database', 'type', 'source']
        
        from io import StringIO
        airports_df = pd.read_csv(StringIO(response.text), names=columns, na_values='\\N')
        
        airports_df = airports_df[
            (airports_df['type'].isin(['airport', 'large_airport', 'medium_airport'])) &
            (airports_df['latitude'].notna()) &
            (airports_df['longitude'].notna())
        ].copy()
        
        print(f"✓ Processed {len(airports_df):,} airports")
        
        return airports_df
        
    except Exception as e:
        print(f"✗ Error: {e}")
        print("! Using fallback data")
        return None

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate great-circle distance using Haversine formula"""
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    r = 6371  # Earth radius in kilometers
    return c * r

# ============================================================================
# LOAD AND PROCESS DATA
# ============================================================================

print("\n" + "="*70)
print("BUILDING STREAMLINED DATASET")
print("="*70)

# Load original data
print("\n[1/6] Loading original dataset...")
df = pd.read_csv('merged_dataset.csv')
print(f"✓ Loaded {len(df):,} listings with {len(df.columns)} columns")

# Scrape airport data
print("\n[2/6] Scraping airport data...")
airports = scrape_openflights_api()

# Add external city data
print("\n[3/6] Adding city population and tourism data...")
df['population'] = df['city'].str.lower().map(lambda x: CITY_DATA.get(x, {}).get('population'))
df['tourist_arrivals'] = df['city'].str.lower().map(lambda x: CITY_DATA.get(x, {}).get('tourist_arrivals'))
df['tourism_pressure_ratio'] = df['tourist_arrivals'] / df['population']
print(f"✓ Added population and tourism data for {df['population'].notna().sum():,} listings")

# Calculate city average prices
print("\n[4/6] Calculating city average prices...")
city_avg = df.groupby('city')['realSum'].mean().to_dict()
df['city_avg_price'] = df['city'].map(city_avg)
print(f"✓ Calculated average prices for {len(city_avg)} cities")

# Calculate price per person
print("\n[5/6] Calculating price per person...")
df['price_per_person'] = df['realSum'] / df['person_capacity']
df['price_per_person'] = df['price_per_person'].replace([np.inf, -np.inf], np.nan)
print(f"✓ Calculated price per person for {df['price_per_person'].notna().sum():,} listings")

# Distance binning
print("\n[6/6] Creating distance bins...")
df['distance_bin'] = pd.cut(
    df['dist'],
    bins=[0, 1, 2, 3, 5, 100],
    labels=['<1km (City Core)', '1-2km (Inner City)', '2-3km (Mid-Range)', '3-5km (Outer Zone)', '>5km (Periphery)'],
    include_lowest=True
)

df['metro_accessibility'] = pd.cut(
    df['metro_dist'],
    bins=[0, 0.5, 1, 2, 100],
    labels=['<500m (Excellent)', '500m-1km (Good)', '1-2km (Moderate)', '>2km (Limited)'],
    include_lowest=True
)

# Calculate airport distances
if airports is not None:
    print("\n[BONUS] Calculating airport distances...")
    df['airport_distance_km'] = np.nan
    
    for city in df['city'].unique():
        city_df = df[df['city'] == city]
        city_airports = airports[airports['city'].str.contains(city, case=False, na=False)]
        
        if len(city_airports) > 0:
            city_center_lat = city_df['lat'].mean()
            city_center_lon = city_df['lng'].mean()
            
            closest_airport = city_airports.iloc[
                ((city_airports['latitude'] - city_center_lat)**2 + 
                 (city_airports['longitude'] - city_center_lon)**2).argmin()
            ]
            
            distances = city_df.apply(
                lambda row: haversine_distance(
                    row['lat'], row['lng'],
                    closest_airport['latitude'], closest_airport['longitude']
                ), axis=1
            )
            
            df.loc[df['city'] == city, 'airport_distance_km'] = distances
            print(f"  ✓ {city}: {len(city_df):,} listings → {closest_airport['name']}")
    
    df['airport_distance_bin'] = pd.cut(
        df['airport_distance_km'],
        bins=[0, 5, 10, 25, 50, 1000],
        labels=['<5km (Very Close)', '5-10km (Close)', '10-25km (Moderate)', '25-50km (Far)', '>50km (Very Far)'],
        include_lowest=True
    )
    print(f"✓ Calculated airport distances for {df['airport_distance_km'].notna().sum():,} listings")

# ============================================================================
# SELECT FINAL COLUMNS
# ============================================================================

print("\n" + "="*70)
print("FINALIZING DATASET")
print("="*70)

# Original columns (all 21 from merged_dataset.csv)
original_cols = [
    'city', 'day_type', 'room_type', 'bedrooms', 'person_capacity',
    'room_shared', 'room_private', 'host_is_superhost', 'multi', 'biz',
    'realSum', 'cleanliness_rating', 'guest_satisfaction_overall',
    'lng', 'lat', 'dist', 'metro_dist', 'attr_index', 'attr_index_norm',
    'rest_index', 'rest_index_norm'
]

# New essential columns
new_cols = [
    'city_avg_price',
    'distance_bin',
    'metro_accessibility',
    'airport_distance_km',
    'airport_distance_bin',
    'price_per_person',
    'population',
    'tourist_arrivals',
    'tourism_pressure_ratio'
]

final_columns = original_cols + new_cols
df_streamlined = df[final_columns].copy()

print(f"\n✓ Original columns: {len(original_cols)}")
print(f"✓ New engineered columns: {len(new_cols)}")
print(f"✓ Total columns: {len(final_columns)}")
print(f"✓ Total listings: {len(df_streamlined):,}")

# ============================================================================
# SAVE
# ============================================================================

output_file = 'dataset.csv'
df_streamlined.to_csv(output_file, index=False)
print(f"\n✓ Saved to: {output_file}")

# Summary statistics
print("\n" + "="*70)
print("DATASET SUMMARY")
print("="*70)

print(f"\nShape: {df_streamlined.shape[0]:,} rows × {df_streamlined.shape[1]} columns")
print(f"\nNew Features:")
for col in new_cols:
    missing = df_streamlined[col].isna().sum()
    print(f"  • {col}: {missing:,} missing ({missing/len(df_streamlined)*100:.1f}%)")

print("\n" + "="*70)
print("COMPLETE")
print("="*70)
