import streamlit as st
import pandas as pd
from snowflake.snowpark import Session

# 1. Page Config
st.set_page_config(page_title="AI Review Decoder", page_icon="🕵️‍♂️", layout="wide")

# This handles the connection to my 400k rows
def create_session():
    return Session.builder.configs(st.secrets["snowflake"]).create()

if 'snowpark_session' not in st.session_state:
    st.session_state.snowpark_session = create_session()

session = st.session_state.snowpark_session

# --- HERO SECTION ---
st.title("Saddy is my name and this is the amazon sentiment analysis")

# columns edits
header_col1, header_col2 = st.columns([2, 1])

with header_col1:
    st.markdown("""
    ### Project Overview
    This application leverages **Snowflake Snowpark** to perform real-time sentiment analysis 
    on a dataset of **399,989 Amazon reviews**. 
    
    * **The Goal:** Instantly decode the "vibe" of customer feedback using custom SQL logic.
    * **The Tech:** Python, Streamlit, and Snowflake Cloud Data Warehouse.
    """)

with header_col2:
    # status box for warehouse connectivity
    st.success("🛰️ Connected to Singapore AWS")
    st.info("📦 Warehouse: COMPUTE_WH")

st.write("---")

# 2. Interactive Sidebar for User Inputs
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2092/2092215.png", width=100)
st.sidebar.header("Discovery Lab")
search_term = st.sidebar.text_input("Find a product keyword (e.g., 'pizza', 'phone'):", "pizza")
limit_val = st.sidebar.slider("Number of reviews to scan:", 10, 100, 25)

# Added a unique key to the sidebar button to avoid duplicate ID errors
if st.sidebar.button("Celebrate Data Success", key="sidebar_balloons"):
    st.balloons()

# 3. The Data Query Logic
if search_term:
    # Adding a 'Status' container for a professional loading animation
    with st.status("🔍 Scanning 400k reviews in Snowflake...", expanded=True) as status:
        st.write("Establishing secure handshake...")
        
        # Core SQL logic for sentiment classification
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
        
        # Execute and convert to pandas
        df = session.sql(query).to_pandas()
        
        st.write("Categorizing sentiment vibes...")
        status.update(label="Analysis Complete!", state="complete", expanded=False)
    
    st.toast("Data decoded successfully!", icon="✅")
    
    # 4. Visual Layout for Charts and Metrics
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Vibe Analysis Chart")
        st.bar_chart(df, y="VIBE_SCORE", color="#00d4ff")

    with col2:
        st.subheader("📈 Data Stats")
        st.metric("Reviews Analyzed", len(df))
        st.metric("Warehouse Status", "Online")
        
        # Added a unique key here to distinguish it from the sidebar button
        if st.button("Celebrate Data Success", key="main_balloons"):
            st.balloons()

    # 5. Live Data Feed & Export Feature
    st.write("---")
    data_col, download_col = st.columns([3, 1])
    
    with data_col:
        st.write("### 📄 Live Data Feed")
    
    with download_col:
        # Convert the dataframe to CSV for exporting
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Report",
            data=csv,
            file_name=f'amazon_vibe_report_{search_term}.csv',
            mime='text/csv',
            use_container_width=True
        )

    # Displaying raw data using 2026 'stretch' parameter
    st.dataframe(df, width='stretch')

    # --- PORTFOLIO FOOTER ---
    st.write("---")
    st.caption("Built by SADDY (LinkedIn: https://www.linkedin.com/in/mohammed-saaduddin-siddique-13776b271/) | Tech Stack: Python, Streamlit, Snowflake Snowpark & AWS Singapore")

else:
    # Initial state warning
    st.warning("👈 Enter a keyword in the 'Discovery Lab' sidebar to start the Snowflake analysis.")
