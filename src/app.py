import streamlit as st

# --- 1. USER AUTHENTICATION LOGIC (SIMPLE IN-MEMORY) ---
# Initialize session state for mock database and login status if they don't exist
if 'user_db' not in st.session_state:
    # Pre-populate with one test user
    st.session_state['user_db'] = {
        "admin": {"password": "password123", "email": "admin@example.com"}
    }
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None

def login_user(username, password):
    db = st.session_state['user_db']
    # Check if user exists and password matches
    if username in db and db[username]['password'] == password:
        st.session_state['logged_in'] = True
        st.session_state['current_user'] = username
        st.success("Logged in successfully!")
        st.rerun() # Refresh the app to show the logged-in view
    else:
        st.error("Incorrect username or password")

def signup_user(username, email, password):
    db = st.session_state['user_db']
    if username in db:
        st.warning("Username already exists!")
    elif not username or not password:
         st.warning("Username and password are required.")
    else:
        # Add new user to the in-memory database
        db[username] = {"password": password, "email": email}
        st.session_state['user_db'] = db
        st.success("Account created! You can now log in.")

def logout_user():
    st.session_state['logged_in'] = False
    st.session_state['current_user'] = None
    st.rerun()

# --- 2. MAIN APP INTERFACE ---
st.title("Simple Login App")

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
    if st.sidebar.button("Logout"):
        logout_user()

    st.markdown("## Main Application Area")
    st.write(f"You are securely logged in. Your email is: {st.session_state['user_db'][st.session_state['current_user']]['email']}")
    st.balloons()
