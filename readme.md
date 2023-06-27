Schema for Cricket Database

The first dataset is a subset of real data from the Cricket game dataset. Source; https://codebasics.io/resources/data-analytics-project-for-beginners



I create ETL processes to get data from JSON files which are scrapped from the ESPN website and created a database that has star schema.


The purpose of the project make cricket data more understandable and make it an easy query and analyses the data.
Make dashboards and visualizations to understand teams' and players performance.

To run these files properly, you must have PostgreSQL software on your computer.

Fact Tables ; 
1. fact_bowling - records in the batting_summary.json file shows batting summary.

2. fact_bowling - records in the bowling_summary.json file shows bowling summary.

Dimension Tables; 
1. match_result - records in the match_result.json file shows match results.

2. players - records in the players_info.json file show information about players.

5. time - timestamps of records in song plays broken down into specific units start_time, hour, day, week, month, year, weekday

Create Tables; sql_quaries.py contains CREATE and INSERT SQL codes to create tables and insert values to tables. 
create_tables.py by running this file it will create a new database and create the necessary tables 
NOTE: you have to modify these parts "host=127.0.0.1 dbname=cricket user=postgres password=user" according to your environment

Build ETL Processes: Run etl.py develops ETL processes(reads and preprocess and inserts them to the table) for each table.

After creating a database and its tables we import this dataset to POWER BI 

Data Modeling;
![img.png](img.png)
<img width="1452" alt="image" src="https://github.com/turgutguvenc/End-to-end-data-powerBI-dashboard/assets/63226091/cc695ff4-bc35-41fd-92e7-f2099ff33c41">
