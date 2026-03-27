import streamlit as st
import pandas as pd
import sqlite3
import os

#Force Light Mode & Page Setup
st.set_page_config(page_title="Perak IoT Dashboard", layout="wide")

st.title("✈️ Perak Flight Data Monitor")
st.write("Current Status: System Online")

#Stable Database Connection
def get_data():
    db_path = os.path.join(os.getcwd(), 'perak_flights.db')
    if not os.path.exists(db_path):
        return pd.DataFrame()
        
    conn = sqlite3.connect(db_path)
    try:
        #Pull the latest 50 rows
        df = pd.read_sql_query("SELECT * FROM flight_logs ORDER BY time_recorded DESC LIMIT 50", conn)
    except:
        df = pd.DataFrame()
    finally:
        conn.close()
    return df

#Display Data
try:
    df = get_data()

    if not df.empty:
        #Metrics Section
        col1, col2 = st.columns(2)
        col1.metric("Total Logs", len(df))
        col2.metric("Unique Aircraft", df['icao24'].nunique())

        #Data Table Section
        st.subheader("Latest 50 Records")
        st.dataframe(df, use_container_width=True)
        
        # Simple coordinate list for report
        st.write("### GPS Coordinates Captured:")
        st.write(df[['icao24', 'latitude', 'longitude']].head(10))

    else:
        st.warning("Database is empty or not found. Please wait for the collector to save data.")

except Exception as e:
    st.error(f"Dashboard Error: {e}")

#Refresh Button
if st.button('🔄 Refresh Now'):
    st.rerun()
