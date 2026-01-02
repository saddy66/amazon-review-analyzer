import streamlit as st
import pandas as pd
from snowflake.snowpark import Session

# 1. PAGE SETUP (The Foundation)
st.set_page_config(page_title="SADDY | Neural Portfolio", page_icon="🌐", layout="wide")

# 2. CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp {
        background-color: #05050a;
        color: #e0e0e0;
    }
    
    /* Sci-Fi Project Card */
    .project-container {
        border: 1px solid #00d4ff;
        padding: 30px;
        border-radius: 15px;
        background: rgba(0, 212, 255, 0.03);
        margin-bottom: 50px;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.1);
    }
    
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. NAVIGATION & HEADER
st.title("SADDY NEURAL INTERFACE v1.0")
st.write("Welcome to the central node. Select a project to initialize.")

# Navigation Buttons
nav_col1, nav_col2, nav_col3 = st.columns(3)
with nav_col1:
    if st.button("📡 [ 01: AMAZON SENTIMENT ANALYSIS ]", use_container_width=True):
        st.write('<style>html {scroll-behavior: smooth;}</style>', unsafe_allow_html=True)
with nav_col2:
    st.button("🧬 [ 02: NEURAL ENGINE ]", use_container_width=True, disabled=True)
with nav_col3:
    st.button("🌑 [ 03: GHOST PROTOCOL ]", use_container_width=True, disabled=True)

st.write("---")

# 4. DATABASE CONNECTION (Keep this at the top level)
def create_session():
    return Session.builder.configs(st.secrets["snowflake"]).create()

if 'snowpark_session' not in st.session_state:
    st.session_state.snowpark_session = create_session()
session = st.session_state.snowpark_session

# ==========================================================
# PROJECT 01: AMAZON SENTIMENT ANALYSIS
# ==========================================================
st.markdown('<div class="project-container">', unsafe_allow_html=True)
st.header("📡 PROJECT 01: AMAZON SENTIMENT ANALYSIS")

# Sidebar Logic for this specific project
st.sidebar.header("📡 Project 01 Controls")
search_term = st.sidebar.text_input("Vibe Keyword:", "pizza", key="p1_search")
limit_val = st.sidebar.slider("Scan Depth:", 10, 100, 25, key="p1_slider")

# Run the Amazon Query
if search_term:
    query = f"""
        SELECT $1 as REVIEW_TEXT,
        CASE 
            WHEN $1 ILIKE '%great%' OR $1 ILIKE '%amazing%' THEN 1
            WHEN $1 ILIKE '%bad%' OR $1 ILIKE '%awful%' THEN -1
            ELSE 0 
        END as VIBE_SCORE
        FROM CUSTOMER_REVIEWS_AMAZON.PUBLIC.AMAZON_TEST_DATA
        WHERE $1 ILIKE '%{search_term}%'
        LIMIT {limit_val}
    """
    df = session.sql(query).to_pandas()

    # Visuals
    c1, c2 = st.columns([2, 1])
    with c1:
        st.bar_chart(df, y="VIBE_SCORE", color="#00d4ff")
    with c2:
        st.metric("Total Records", "399,989")
        st.metric("Target Keyword", search_term)
        if st.button("Celebrate Success", key="p1_balloons"):
            st.balloons()
            
    st.dataframe(df, width='stretch')
st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# PROJECT 02: PLACEHOLDER (My Next Big Idea)
# ==========================================================
st.markdown('<div class="project-container">', unsafe_allow_html=True)
st.header("🧬 PROJECT 02: EPST1EN FlLES")
st.write("### [ SYSTEM STATUS: ENCRYPTED ]")
st.info("Coming Soon: ill try lol.")
st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.write("---")
st.caption("Saad Neural Portfolio (LinkedIn: https://www.linkedin.com/in/mohammed-saaduddin-siddique-13776b271/) | AWS Singapore Node | 2026")
