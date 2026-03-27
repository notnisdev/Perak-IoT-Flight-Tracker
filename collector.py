import time
import sqlite3
import requests
import pandas as pd

print("DEBUG: Script Started")

#---CONFIGURATION---
#OpenSky uses:(min_lat, min_lon, max_lat, max_lon)
PERAK_BBOX = (3.6, 100.0, 6.0, 101.8)
DB_NAME = 'perak_flights.db'
FETCH_INTERVAL = 120 

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flight_logs (
            icao24 TEXT,
            callsign TEXT,
            longitude REAL,
            latitude REAL,
            altitude REAL,
            velocity REAL,
            time_recorded DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

def start_collecting():
    db_conn = setup_database()
    url = "https://opensky-network.org/api/states/all"
    params = {
        'lamin': PERAK_BBOX[0],
        'lomin': PERAK_BBOX[1],
        'lamax': PERAK_BBOX[2],
        'lomax': PERAK_BBOX[3]
    }
    
    print("--------------------------------------------------")
    print("DIRECT API MODE: Monitoring Perak Airspace")
    print("--------------------------------------------------")

    while True:
        try:
            print(f"[{time.ctime()}] Fetching from OpenSky...")
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            #Check if 'states' exists in the response
            if data and "states" in data and data["states"] is not None:
                states = data["states"]
                cursor = db_conn.cursor()
                
                for s in states:
                    #s[0]=icao24, s[1]=callsign, s[5]=lon, s[6]=lat, s[7]=baro_alt, s[9]=velocity
                    cursor.execute('''
                        INSERT INTO flight_logs (icao24, callsign, longitude, latitude, altitude, velocity)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (s[0], s[1].strip(), s[5], s[6], s[7], s[9]))
                
                db_conn.commit()
                print(f"[{time.ctime()}] SUCCESS: Recorded {len(states)} planes.")
            else:
                print(f"[{time.ctime()}] MONITORING: 0 planes found in Perak box.")
            
            print(f"Waiting {FETCH_INTERVAL} seconds...")
            time.sleep(FETCH_INTERVAL)

        except Exception as e:
            print(f"[{time.ctime()}] NOTICE: {e}")
            time.sleep(60)

if __name__ == "__main__":
    start_collecting()
