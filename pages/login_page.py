import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

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

def register_user(username, password, email):
    """Register a new user"""
    users = load_users()
    if username in users:
        return False, "Username already exists!"
    
    users[username] = {
        "password": password,
        "email": email,
        "saved_basket": [],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_users(users)
    return True, "Registration successful! Please login."

def login_user(username, password):
    """Authenticate user"""
    users = load_users()
    if username not in users:
        return False, "Username not found!"
    
    if users[username]["password"] != password:
        return False, "Incorrect password!"
    
    return True, "Login successful!"

# Page configuration
st.set_page_config(page_title="ShopOptima - Login", layout="wide")

# Add navigation button to main page
col1, col2 = st.columns([0.9, 0.1])
with col2:
    if st.button("Home"):
        st.switch_page("Main.py")

st.title("Shoptimizer: User Login")

# Check if already logged in
if st.session_state.logged_in:
    st.success(f"Welcome back, {st.session_state.current_user}!")
    
    users = load_users()
    user_data = users.get(st.session_state.current_user, {})
    
    # Display saved baskets (history)
    st.subheader("Your Saved Baskets")
    
    # handle legacy format where we only kept a flat list
    if "saved_basket" in user_data and "saved_baskets" not in user_data:
        # migrate legacy format into new history structure
        legacy = user_data.pop("saved_basket")
        legacy_ts = None
        if isinstance(legacy, list) and legacy:
            legacy_ts = legacy[0].get("added_at")
        legacy_ts = legacy_ts or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_data["saved_baskets"] = [{
            "items": [entry.get("name") for entry in legacy] if isinstance(legacy, list) else [],
            "added_at": legacy_ts,
            "total": user_data.get("last_total")
        }]
        save_users(users)  # persist migration

    saved_baskets = user_data.get("saved_baskets", [])

    if saved_baskets:
        # iterate through each saved basket and provide a use button
        for idx, basket in enumerate(saved_baskets):
            st.markdown(f"**Basket {idx + 1}** (added {basket.get('added_at', 'n/a')}) - £{basket.get('total', 'n/a')}")
            st.write(", ".join(basket.get("items", [])))
            if st.button(f"Use Basket {idx + 1}", key=f"use_{idx}"):
                st.session_state.selected_items = basket.get("items", [])
                st.switch_page("Main.py")
    else:
        st.info("You haven't saved any baskets yet. Create one on the home page!")
    
    # User account details
    st.subheader("Account Details")
    col1, col2 = st.columns(2)
    with col1:
        st.text(f"Username: {st.session_state.current_user}")
    with col2:
        st.text(f"Email: {user_data.get('email', 'N/A')}")
    
    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()

else:
    # Tab switching between Login and Register
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login to Your Account")
        
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if not username or not password:
                st.error("Please fill in all fields!")
            else:
                success, message = login_user(username, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
    
    with tab2:
        st.subheader("Create a New Account")
        
        new_username = st.text_input("Choose Username", key="register_username")
        new_email = st.text_input("Email Address", key="register_email")
        new_password = st.text_input("Password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm")
        
        if st.button("Register"):
            if not new_username or not new_email or not new_password:
                st.error("Please fill in all fields!")
            elif new_password != confirm_password:
                st.error("Passwords do not match!")
            elif len(new_password) < 4:
                st.error("Password must be at least 4 characters!")
            else:
                success, message = register_user(new_username, new_password, new_email)
                if success:
                    st.success(message)
                else:
                    st.error(message)
