import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import math
import json
import os

# 1. DATABASE (The Store-Centric JSON we built)
with open('stores.json', 'r') as f:
    STORES_DB = json.load(f)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Users database file
USERS_DB = 'users_data.json'

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_DB):
        with open(USERS_DB, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_DB, 'w') as f:
        json.dump(users, f, indent=2)

def save_basket_for_user(username, items, total_cost):
    """Save basket to user's account"""
    users = load_users()
    if username in users:
        users[username]["saved_basket"] = [{"name": item, "added_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} for item in items]
        users[username]["last_total"] = round(total_cost, 2)
        save_users(users)
        return True
    return False

# 2. LOGIC: Distance & Cost Calculation
def get_distance(lat1, lon1, lat2, lon2):
    # Quick Haversine distance
    radius = 3958.8 
    dlat, dlon = math.radians(lat2-lat1), math.radians(lon2-lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return radius * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))

# 3. STREAMLIT UI
st.set_page_config(page_title="Shoptimizer", layout="wide")

# Top navigation bar with login button
col1, col2 = st.columns([0.85, 0.15])
with col1:
    st.title("🛒 Shoptimizer: Basket Optimizer")
with col2:
    if st.button("👤 Login"):
        st.switch_page("pages/login_page.py")

# Display logged-in user info
if st.session_state.logged_in and st.session_state.current_user:
    st.info(f"✅ Logged in as: **{st.session_state.current_user}**")

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
    
    # Save basket button (if logged in)
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.logged_in and st.session_state.current_user:
            best_store = df.iloc[0]
            if st.button("💾 Save This Basket to My Account"):
                if save_basket_for_user(st.session_state.current_user, selected_items, best_store["Total (£)"]):
                    st.success(f"✅ Basket saved! Best option: {best_store['Store']} (£{best_store['Total (£)']})")
                else:
                    st.error("Failed to save basket. Please login first.")
    
    with col2:
        if st.button("➕ Start New Search"):
            st.rerun()

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
    st.info("📝 Please select some items to see the best store for your trip. 🔓 Login to save your favorite baskets!")
