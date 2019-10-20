%load_ext sql
%sql postgresql://student:student@127.0.0.1/sparkifydb
%sql SELECT * FROM songplays WHERE artist_id IS NOT NULL ORDER BY artist_id LIMIT 5;
%sql SELECT * FROM users LIMIT 5;
%sql SELECT * FROM artists LIMIT 5;
%sql SELECT * FROM time LIMIT 5;
