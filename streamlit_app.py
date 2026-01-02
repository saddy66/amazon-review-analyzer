import streamlit as st
import pandas as pd
from snowflake.snowpark import Session

# 1. Page Config
st.set_page_config(page_title="AI Portfolio | Review Decoder", page_icon="🕵️‍♂️")

st.title("🕵️‍♂️ SADDY: The Interactive Review Decoder")
st.write("---")

# 2. Connection Logic 
def create_session():
    # This specifically uses the credentials you just saved in 'Secrets'
    return Session.builder.configs(st.secrets["snowflake"]).create()

# Check if session exists, if not, create it
if 'snowpark_session' not in st.session_state:
    st.session_state.snowpark_session = create_session()

session = st.session_state.snowpark_session

# 3. Interactive Sidebar
st.sidebar.header("Control Panel")
sample_size = st.sidebar.slider("Reviews to analyze:", 10, 100, 50)
search_query = st.sidebar.text_input("Search keyword:", "good")

# 4. Data Query
query = f"""
    SELECT $1 as REVIEW_TEXT,
    CASE 
        WHEN $1 ILIKE '%great%' OR $1 ILIKE '%amazing%' THEN 1
        WHEN $1 ILIKE '%bad%' OR $1 ILIKE '%awful%' THEN -1
        ELSE 0 
    END as VIBE_SCORE
    FROM CUSTOMER_REVIEWS_AMAZON.PUBLIC.AMAZON_TEST_DATA
    WHERE $1 ILIKE '%{search_query}%'
    LIMIT {sample_size}
"""

df = session.sql(query).to_pandas()

# 5. Visuals
st.subheader("Vibe Analysis")
st.bar_chart(df, y="VIBE_SCORE", color="#FF4B4B")
st.dataframe(df)

if st.button("Celebrate!"):
    st.balloons()
