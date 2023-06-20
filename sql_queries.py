# DROP TABLES

batting_table_drop = "DROP TABLE IF EXISTS batting"
bowling_table_drop = "DROP TABLE IF EXISTS bowling"
match_table_drop = "DROP TABLE IF EXISTS match_results"
players_table_drop = "DROP TABLE IF EXISTS players"


# CREATE TABLES


match_table_create = ("""
    CREATE TABLE IF NOT EXISTS match_results (
        match_id INT NOT NULL PRIMARY KEY,
        team1 VARCHAR,
        team2 VARCHAR,
        winner VARCHAR,
        margin VARCHAR,
        ground VARCHAR,
        matchDate TEXT
    )
""")


batting_table_create = ("""
                         CREATE TABLE IF NOT EXISTS batting (
                             match_id INT NOT NULL PRIMARY KEY,
                             match TEXT,
                             teamInnings VARCHAR,
                             battingPos INT,
                             batsmanName VARCHAR,
                             dismissal VARCHAR,
                             runs INT,
                             balls INT,
                             fours INT,
                             sixs INT,
                             SR FLOAT
                         );
                         """)



bowling_table_create = ("""
                         CREATE TABLE IF NOT EXISTS bowling (
                             match_id INT NOT NULL PRIMARY KEY,
                             match text,
                             bowlingTeam varchar,
                             bowlerName varchar,
                             overs int,
                             maiden int,
                             runs int,
                             wickets int,
                             economy float,
                             zeros int,
                             fours int,
                             sixs int,
                             wides int,
                             noBalls int);
                         """)

players_table_create = ("""
                       CREATE TABLE IF NOT EXISTS players (
                           name varchar,
                           team varchar,
                           battingStyle varchar,
                           bowlingStyle varchar,
                           playingRole varchar,
                           description text);
                       """)


# INSERT RECORDS

batting_table_insert = """
    INSERT INTO batting (
        match_id,
        match,
        teamInnings,
        battingPos,
        batsmanName,
        dismissal,
        runs,
        balls,
        fours,
        sixs,
        SR
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (match_id) DO NOTHING;
"""



match_table_insert = """
    INSERT INTO match_results (
        match_id,
        team1,
        team2,
        winner,
        margin,
        ground,
        matchDate
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (match_id) DO NOTHING
"""

bowling_table_insert = ("""
                     INSERT INTO bowling (
                             match_id,
                             match,
                             bowlingTeam,
                             bowlerName,
                             overs,
                             maiden,
                             runs,
                             wickets,
                             economy,
                             zeros,
                             fours,
                             sixs,
                             wides,
                             noBalls)
                      VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s)
                      ON CONFLICT (match_id) DO NOTHING;
                      """)

players_table_insert = ("""
                       INSERT INTO players (
                           name,
                           team,
                           battingStyle,
                           bowlingStyle,
                           playingRole,
                           description
                       )
                       VALUES (%s, %s, %s, %s, %s, %s);
                       """)




# QUERY LISTS

create_table_queries = [batting_table_create,
                      bowling_table_create,
                      match_table_create ,
                      players_table_create]

drop_table_queries = [batting_table_drop,
                      bowling_table_drop,
                      match_table_drop,
                      players_table_drop]
