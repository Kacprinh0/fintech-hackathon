import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import math

# 1. DATABASE (The Store-Centric JSON we built)
STORES_DB = {
    "stores": [
        {
            "name": "Tesco Superstore",
            "lat": 51.5074, "lon": -0.1278,
            "inventory": {"milk": 1.20, "bread": 0.85, "eggs": 2.10, "apples": 2.00},
            "parking_fee": 0.0
        },
        {
            "name": "Waitrose & Partners",
            "lat": 51.5150, "lon": -0.1400,
            "inventory": {"milk": 1.55, "bread": 1.20, "eggs": 3.00, "apples": 2.50},
            "parking_fee": 2.50
        },
        {
            "name": "Asda Express",
            "lat": 51.5000, "lon": -0.1100,
            "inventory": {"milk": 1.15, "bread": 0.70, "eggs": 1.90, "apples": 2.20},
            "parking_fee": 0.0
        }
    ]
}

# 2. LOGIC: Distance & Cost Calculation
def get_distance(lat1, lon1, lat2, lon2):
    # Quick Haversine distance
    radius = 3958.8 
    dlat, dlon = math.radians(lat2-lat1), math.radians(lon2-lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return radius * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))

# 3. STREAMLIT UI
st.set_page_config(page_title="ShopOptima", layout="wide")
st.title("🛒 ShopOptima: Basket Optimizer")

# Sidebar: User Inputs
st.sidebar.header("Your Trip Details")
user_lat = st.sidebar.number_input("Your Latitude", value=51.5090, format="%.4f")
user_lon = st.sidebar.number_input("Your Longitude", value=-0.1300, format="%.4f")
fuel_cost_per_mile = st.sidebar.slider("Travel Cost (£/mile)", 0.10, 1.00, 0.45)

# Main Area: Shopping List
all_items = list(STORES_DB["stores"][0]["inventory"].keys())
selected_items = st.multiselect("Build your shopping list:", all_items, default=["milk", "bread"])

if selected_items:
    results = []
    for s in STORES_DB["stores"]:
        # Calculate Costs
        basket_price = sum(s["inventory"].get(item, 0) for item in selected_items)
        dist = get_distance(user_lat, user_lon, s["lat"], s["lon"])
        travel_cost = (dist * 2) * fuel_cost_per_mile
        total_cost = basket_price + travel_cost + s["parking_fee"]
        
        results.append({
            "Store": s["name"],
            "Basket Price (£)": round(basket_price, 2),
            "Travel Cost (£)": round(travel_cost, 2),
            "Total (£)": round(total_cost, 2),
            "Distance (mi)": round(dist, 2),
            "lat": s["lat"], "lon": s["lon"]
        })

    # Sort by cheapest total
    df = pd.DataFrame(results).sort_values("Total (£)")
    
    # Show Results Table
    st.subheader("Results: Best Value for your Trip")
    st.dataframe(df.drop(columns=['lat', 'lon']), use_container_width=True)

    # MAP VISUALIZATION
    st.subheader("Store Locations")
    m = folium.Map(location=[user_lat, user_lon], zoom_start=13)
    
    # Add User
    folium.Marker([user_lat, user_lon], tooltip="You are here", icon=folium.Icon(color='red')).add_to(m)
    
    # Add Stores
    for i, row in df.iterrows():
        color = 'green' if i == df.index[0] else 'blue'
        folium.Marker(
            [row['lat'], row['lon']], 
            popup=f"{row['Store']}: £{row['Total (£)']}",
            tooltip=row['Store'],
            icon=folium.Icon(color=color)
        ).add_to(m)
    
    st_folium(m, width=700, height=400)

else:
    st.info("Please select some items to see the best store for your trip.")
