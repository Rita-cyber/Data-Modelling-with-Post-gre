import os
import glob
import numpy as np
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Processes song file from song_data directory to create two tables: song_data and artist_data

    Args:
    - cur: Allows to run Postgres command
    - filepath: File to be processed and extracted to Postgres tables
    
    Returns:
    None
    """
    # open song file
    df = pd.read_json(filepath, lines = True)

    # insert song record
    song_data = df[["song_id", "title", "artist_id", "year", "duration"]].values[0]
    # print(len(song_data))
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]].values[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Processes log file from log_data directory to create three tables: time, users, and songplays 
    
    Args:
    - cur: Allows to run Postgres command
    - filepath: File to be processed and extracted to Postgres tables
    
    Returns: None
    """
    # open log file
    df = pd.read_json(filepath, lines = True)

    # filter by NextSong action
    df = df.query(" page == 'NextSong' ")

    # convert timestamp column to datetime
    t = pd.to_datetime(df["ts"]/1000, unit = 's')
    
    # insert time data records
    time_data = np.transpose(np.array([df["ts"].values, t.dt.hour.values, t.dt.day.values, t.dt.week.values,\
                                       t.dt.month.values, t.dt.year.values, t.dt.weekday.values]))
    column_labels = ("timestamp", "hour", "day", "week of year", "month", "year", "weekday")
    time_df = pd.DataFrame(data = time_data, columns = column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Process all the files in data directory and creates Postgres tables
    
    Args:
        - cur: Allows to run Postgres command
        - conn: Connection to Postgres database
        - filepath: File to be processed and extracted to Postgres tables
        - func: Function to be allowed for ETL, can take two values
            + process_song_data: when filepath is song_data, or
            + process_log_data: when filepath is log_data
    
    Returns:
    None
    """
    
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    # connect to Postgress database
    conn = psycopg2.connect("host=127.0.0.1 dbname=ritzy user=ritzy password=machinehng")
    
    # create a cursor to run SQL queries
    cur = conn.cursor()
    
    # process song_data directory
    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    
    # process log_data directory
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
