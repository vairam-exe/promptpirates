import streamlit as st
import db_manager
import auth_service

# --- Initialize Database ---
# Ensure the database and tables are set up on application start.
# This will also create the default admin user if the table is empty.
db_manager.init_db()

# --- 1. USER AUTHENTICATION LOGIC ---
# Initialize session state for login status if they don't exist
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None
if 'current_user_email' not in st.session_state:
    st.session_state['current_user_email'] = None
if 'current_user_role' not in st.session_state:
    st.session_state['current_user_role'] = None

def login_user(username, password):
    """
    Authenticates a user using the auth_service and updates session state.
    """
    user_data = auth_service.authenticate_user(username, password)
    if user_data:
        st.session_state['logged_in'] = True
        st.session_state['current_user'] = user_data['username']
        st.session_state['current_user_email'] = user_data['email']
        st.session_state['current_user_role'] = user_data['role']
        st.success(f"Logged in successfully as {user_data['username']} ({user_data['role']})!")
        st.rerun()  # Refresh the app to show the logged-in view
    else:
        st.error("Incorrect username or password")

def signup_user(username, email, password):
    """
    Registers a new user using the auth_service and displays status.
    """
    # For now, new users default to 'user' role
    success, message = auth_service.register_user(username, email, password, role='user')
    if success:
        st.success(message)
    else:
        st.warning(message)

def logout_user():
    """
    Logs out the current user by clearing relevant session state variables.
    """
    st.session_state['logged_in'] = False
    st.session_state['current_user'] = None
    st.session_state['current_user_email'] = None
    st.session_state['current_user_role'] = None
    st.rerun()

# --- 2. MAIN APP INTERFACE ---
st.title("Streamlit Persistent Login App")

# If the user is NOT logged in, show the Tabs
if not st.session_state['logged_in']:
    tab1, tab2 = st.tabs(["Login", "Signup"])

    # --- LOGIN TAB ---
    with tab1:
        st.header("Welcome Back")
        login_user_input = st.text_input("Username", key="login_user")
        login_pass_input = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            login_user(login_user_input, login_pass_input)

    # --- SIGNUP TAB ---
    with tab2:
        st.header("Create Account")
        new_user = st.text_input("Username (Name)", key="signup_user")
        new_email = st.text_input("Email", key="signup_email")
        new_pass = st.text_input("Password", type="password", key="signup_pass")

        if st.button("Signup"):
            signup_user(new_user, new_email, new_pass)

# If the user IS logged in, show the main app content
else:
    st.sidebar.header(f"Welcome, {st.session_state['current_user']}!")
    st.sidebar.info(f"Role: {st.session_state.get('current_user_role', 'N/A')}")
    if st.sidebar.button("Logout"):
        logout_user()

    st.markdown("## Main Application Area")
    st.write(f"You are securely logged in as **{st.session_state['current_user']}**.")
    st.write(f"Your email is: **{st.session_state.get('current_user_email', 'Not available')}**")
    st.write(f"Your role is: **{st.session_state.get('current_user_role', 'Not available')}**")
    st.balloons()