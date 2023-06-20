import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
import json

# I will create dictionary to connect this table others

with open("datasets/match_results.json") as f:
    data = json.load(f)
df_match = pd.DataFrame(data[0]['matchSummary'])
match_ids = {}
for index, row in df_match.iterrows():
    key1 = row["team1"] + " Vs " + row["team2"]
    key2 = row["team2"] + " Vs " + row["team1"]
    match_ids[key1] = row["match_id"]
    match_ids[key2] = row["match_id"]

def match_results_file(cur, filepath,conn):
    # open song file
    with open(filepath) as f:
        data = json.load(f)
    df_match = pd.DataFrame(data[0]['matchSummary'])
    # I will use scorecard column as a primary key because it is unique for every game
    # I don't want to see T20I# part in the column too.
    # there is a pattern so we can take after 7th element in the string
    df_match["match_id"] = df_match["scorecard"].apply(lambda x: x[7:11])
    df_match.drop(["scorecard"], inplace=True, axis=1)
    # changing column orders.
    df_match = df_match.loc[:, ['match_id', 'team1', 'team2', 'winner', 'margin', 'ground', 'matchDate']]

    # insert match records
    for index, row in df_match.iterrows():
        cur.execute(match_table_insert, (
            row['match_id'],
            row['team1'],
            row['team2'],
            row['winner'],
            row['margin'],
            row['ground'],
            row['matchDate']
        ))
        conn.commit()
    





def process_batting_file(cur, filepath,conn):
    # open log file
    # After reading data, json file has one list this list contains 45 batting summary for each game
    with open(filepath) as f:
        data = json.load(f)
        all_data = []
        for record in data:
            all_data.extend(record["battingSummary"])

    # basically we made dataframe from those dictonaries.
    df_batting = pd.DataFrame(all_data)

    # in df_batting dataset if the dismissal columns is blank that means player didn't change entire game.
    # let's create new column for just show out or not out instead of long text contains players name
    # apply(lambda x: np.square(x) if x.name == 'd' else x, axis=1)
    df_batting["dismissal"] = df_batting["dismissal"].apply(lambda x: "out" if len(x) > 0 else "not_out")

    # there are some special characters in the batsmanName column I am going to remove them
    df_batting["batsmanName"] = df_batting["batsmanName"].apply(lambda x: x.replace("â€", ""))
    df_batting["batsmanName"] = df_batting["batsmanName"].apply(lambda x: x.replace("\xa0", ""))
    # with this code we get the unique match_id columns to our batting table
    # in sql queries and power BI we will need columns to join the tables
    df_batting["match_id"] = df_batting["match"].map(match_ids)

    # Arranging the column order
    df_batting = df_batting.loc[:, ['match_id', 'match', 'teamInnings', 'battingPos', 'batsmanName', 'dismissal',
                                    'runs', 'balls', '4s', '6s', 'SR']]
    # Insert the new values
    for index, row in df_batting.iterrows():
        cur.execute(batting_table_insert, (
            row['match_id'],
            row['match'],
            row['teamInnings'],
            row['battingPos'],
            row['batsmanName'],
            row['dismissal'],
            row['runs'],
            row['balls'],
            row['4s'],
            row['6s'],
            row['SR']
        ))
    conn.commit()



def process_bowling_data(cur, filepath, conn):
    # get all files matching extension from directory
    with open(filepath) as f:
        data = json.load(f)
        all_data = []
        for record in data:
            all_data.extend(record["bowlingSummary"])

    df_bowling = pd.DataFrame(all_data)
    df_bowling["match_id"] = df_bowling["match"].map(match_ids)

    # arranging the column order
    df_bowling = df_bowling.loc[:, ['match_id', 'match', 'bowlingTeam', 'bowlerName', 'overs', 'maiden', 'runs',
                                    'wickets', 'economy', '0s', '4s', '6s', 'wides', 'noBalls', ]]

    for index, row in df_bowling.iterrows():
        cur.execute(bowling_table_insert, (
            row['match_id'],
            row['match'],
            row['bowlingTeam'],
            row['bowlerName'],
            float(row['overs']),
            row['maiden'],
            row['runs'],
            row['wickets'],
            row['economy'],
            row['0s'],
            row['4s'],
            row['6s'],
            row['wides'],
            row['noBalls'],
        ))
        conn.commit()



def player_file(cur, filepath, conn):
    # open song file
    with open(filepath) as f:
        data = json.load(f)
        df_players = pd.DataFrame(data)
    ## clean the special characters from the names
    df_players["name"] = df_players["name"].apply(lambda x: x.replace("â€", ""))
    df_players["name"] = df_players["name"].apply(lambda x: x.replace("\xa0", ""))
    df_players['name'] = df_players['name'].apply(lambda x: x.replace('Ã¢â‚¬', ''))
    df_players['name'] = df_players['name'].apply(lambda x: x.replace('â€ ', ''))
    df_players['name'] = df_players['name'].apply(lambda x: x.replace('\\xa0', ''))
    # Iterate over the DataFrame and insert the data into the players table

    for index, row in df_players.iterrows():
        cur.execute(players_table_insert, (
            row['name'],
            row['team'],
            row['battingStyle'],
            row['bowlingStyle'],
            row['playingRole'],
            row['description']
        ))
        conn.commit()

def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=cricket user=postgres password=user")
    cur = conn.cursor()

    match_results_file(cur, "datasets/match_results.json",conn)
    process_batting_file(cur, "datasets/batting_summary.json",conn)
    process_bowling_data(cur, "datasets/bowling_summary.json", conn)
    player_file(cur, "datasets/player_info.json", conn)
    conn.close()


if __name__ == "__main__":
    main()