
import streamlit as st

from database import init_db
from auth import show_login, show_signup
from dashboard import show_dashboard


# Page configuration
st.set_page_config(
    page_title="EduTrack | Student Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Initialize database
init_db()


# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None


# Custom styling
st.markdown("""
<style>

.main {
    background-color: #f8fafc;
}

[data-testid="stHeader"] {
    background-color: transparent;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #172554;
}

.stButton button[kind="primaryFormSubmit"] {
    background-color: #2563eb;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# Application routing
if (
    st.session_state["authenticated"]
    and st.session_state["user"] is not None
):

    # Show protected dashboard
    show_dashboard(st.session_state["user"])

else:

    # Show authentication page
    st.markdown("# 🎓 EduTrack")

    st.markdown(
        "### Student Dropout Risk & Academic Success System"
    )

    st.write(
        "An interactive academic analytics platform "
        "designed to explore student performance and outcomes."
    )

    st.divider()

    login_tab, signup_tab = st.tabs([
        "Login",
        "Create Account"
    ])

    with login_tab:
        show_login()

    with signup_tab:
        show_signup()
