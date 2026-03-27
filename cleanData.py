import sqlite3
import pandas as pd

conn = sqlite3.connect('perak_flights.db')

try:
    df = pd.read_sql_query("SELECT * FROM flight_logs", conn)
    print(f"📊 Total raw records: {len(df)}")
    print(f"🔎 Columns found in your DB: {list(df.columns)}")

    #Find the right names for altitude and velocity
    #Look for any column that contains the word 'alt' or 'velo'
    alt_col = [c for c in df.columns if 'alt' in c.lower()]
    vel_col = [c for c in df.columns if 'vel' in c.lower()]
    call_col = [c for c in df.columns if 'call' in c.lower()]

    if not alt_col or not vel_col:
        print("❌ Could not find altitude or velocity columns. Please check the 'Columns found' list above.")
    else:
        #Clean using the discovered column names
        target_cols = [call_col[0], alt_col[0], vel_col[0]]
        df_clean = df.dropna(subset=target_cols)
        
        #Trim whitespace
        df_clean[call_col[0]] = df_clean[call_col[0]].str.strip()

        #Save to CSV
        df_clean.to_csv('perak_flights_CLEANED.csv', index=False)
        print(f"✅ Success! {len(df_clean)} records saved to 'perak_flights_CLEANED.csv'.")

except Exception as e:
    print(f"❌ An error occurred: {e}")

finally:
    conn.close()
