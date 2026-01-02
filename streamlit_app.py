import streamlit as st
import pandas as pd
from snowflake.snowpark import Session

st.set_page_config(page_title="AI Review Decoder", page_icon="🕵️‍♂️", layout="wide")

# This handles the connection to your 400k rows
def create_session():
    return Session.builder.configs(st.secrets["snowflake"]).create()

if 'snowpark_session' not in st.session_state:
    st.session_state.snowpark_session = create_session()

session = st.session_state.snowpark_session

st.title("🕵️‍♂️ SADDY: Amazon Review Vibe Decoder")
st.markdown("---")

# COOL INTERACTIVE SIDEBAR
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2092/2092215.png", width=100)
st.sidebar.header("Discovery Lab")
search_term = st.sidebar.text_input("Find a product keyword:", "pizza")
limit_val = st.sidebar.slider("Number of reviews to scan:", 10, 100, 25)

# SUCCESS ANIMATION TRIGGER
if st.sidebar.button("Celebrate Data Success"):
    st.balloons()

# THE MAGIC QUERY
df = session.sql(f"""
    SELECT $1 as REVIEW_TEXT,
    CASE 
        WHEN $1 ILIKE '%great%' OR $1 ILIKE '%amazing%' THEN 1
        WHEN $1 ILIKE '%bad%' OR $1 ILIKE '%awful%' THEN -1
        ELSE 0 
    END as VIBE_SCORE
    FROM CUSTOMER_REVIEWS_AMAZON.PUBLIC.AMAZON_TEST_DATA
    WHERE $1 ILIKE '%{search_term}%'
    LIMIT {limit_val}
""").to_pandas()

# LAYOUT
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Vibe Analysis Chart")
    st.bar_chart(df, y="VIBE_SCORE", color="#00d4ff")

with col2:
    st.subheader("Data Stats")
    st.metric("Total Rows in Warehouse", "399,989")
    st.info("Analysis powered by Snowflake Snowpark")

st.write("### Live Data Feed")
st.dataframe(df, width='stretch')

