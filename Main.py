import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import math
import json

# 1. DATABASE (The Store-Centric JSON we built)
with open('stores.json', 'r') as f:
    STORES_DB = json.load(f)

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
user_lat = st.sidebar.number_input("Your Latitude", value=52.400, format="%.4f")
user_lon = st.sidebar.number_input("Your Longitude", value=-1.5500, format="%.4f")
fuel_cost_per_mile = st.sidebar.slider("Travel Cost (£/mile)", 0.10, 1.00, 0.45)

# Main Area: Shopping List
# Grab items from the first store in your JSON list
all_items = list(STORES_DB["stores"][0]["inventory"].keys())
selected_items = st.multiselect("Build your shopping list:", all_items)

if selected_items:
    results = []
    for s in STORES_DB["stores"]:
        basket_price = sum(s["inventory"].get(item, 0) for item in selected_items)
        store_lat = s["location"]["lat"]
        store_lon = s["location"]["lon"]
        
        dist = get_distance(user_lat, user_lon, store_lat, store_lon)
        travel_cost = (dist * 2) * fuel_cost_per_mile
        total_cost = basket_price + travel_cost
        
        results.append({
            "Store": s["name"],
            "Address": s["location"]["address"],
            "Basket Price (£)": round(basket_price, 2),
            "Travel Cost (£)": round(travel_cost, 2),
            "Total (£)": round(total_cost, 2),
            "Distance (mi)": round(dist, 2),
            "lat": store_lat, 
            "lon": store_lon
        })

    # 1. CREATE AND SORT DATAFRAME (Only do this once)
    df = pd.DataFrame(results).sort_values("Total (£)")
    
    # 2. DISPLAY TABLE (Only do this once)
    st.subheader("Results: Best Value for your Trip")
    st.dataframe(df.drop(columns=['lat', 'lon']), use_container_width=True)

    # 3. MAP VISUALIZATION
    st.subheader("Store Locations")
    m = folium.Map(location=[user_lat, user_lon], zoom_start=13)
    
    # Add User
    folium.Marker([user_lat, user_lon], tooltip="You are here", icon=folium.Icon(color='red')).add_to(m)
    
    # Add Stores
    for i, row in df.iterrows():
        # The first row in our sorted dataframe is the winner
        is_winner = (row['Total (£)'] == df['Total (£)'].min())
        color = 'green' if is_winner else 'blue'
        
        folium.Marker(
            [row['lat'], row['lon']], 
            popup=f"{row['Store']}: £{row['Total (£)']}",
            tooltip=f"{row['Store']} (£{row['Total (£)']})",
            icon=folium.Icon(color=color)
        ).add_to(m)
    
    st_folium(m, width=700, height=400)

else:
    st.info("Please select some items to see the best store for your trip.")
