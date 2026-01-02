import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd

# 1. Page Config (Adds a professional browser tab title)
st.set_page_config(page_title="AI Portfolio | Review Decoder", page_icon="🕵️‍♂️")

st.title("🕵️‍♂️ SADDY: The Interactive Review Decoder")
st.write("---")

# 2. Interactive Sidebar
st.sidebar.header("Control Panel")
sample_size = st.sidebar.slider("How many reviews to analyze?", 10, 100, 50)
search_query = st.sidebar.text_input("Filter by keyword (e.g., 'quality', 'bad')")

session = get_active_session()

# 3. Dynamic SQL based on user input
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

# 4. Visual Layout 
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Vibe Distribution")
    st.bar_chart(df, y="VIBE_SCORE", color="#FF4B4B")

with col2:
    st.subheader("Project Specs")
    st.info(f"**Dataset:** 400,000 Amazon Reviews")
    st.success(f"**Tech:** Snowflake + Streamlit")

# 5. Animated Progress Bar
if st.button("Run Deep Analysis"):
    with st.spinner('Calculating vibes...'):
        st.balloons()
        st.dataframe(df)