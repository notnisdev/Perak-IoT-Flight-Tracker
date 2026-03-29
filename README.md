PROJECT OVERVIEW:
The goal of this project is to monitor and analyze real-time aircraft telemetry over the Perak region using an end-to-end IoT data pipeline. Over a 3 monitoring period, we collected 2,708 aircraft records using the OpenSky Network API.

REPOSITORY STRUCTURE:
The project is organized into the following functional scripts:
- collector.py: This is the code to collect the data from OpenSky Network API then passes it into a local SQLite database.
- cleanData.py: This is the code to clean the raw data that we have collected over the 3 day period to help prepare for the data analysis.
- dashboard.py: This is the code for the dashboard that provides an overview of the captured data, like displaying the key metrics or real time flight status.
- .gitignore: This file ensures that temporary environment files and large raw databases are not accidentally pushed to the public repository, keeping the project clean.

HOW TO RUN:
1. Run the python collector.py first to gather the raw data.
2. Run the cleanData.py to scrub raw logs and generate a clean dataset after the data collection period.
3. Run the python dashboard.py to view the processed flight insights and statisical trends. 
