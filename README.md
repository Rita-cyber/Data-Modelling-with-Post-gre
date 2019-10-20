# Data-Modelling-with-Post-gre

https://drive.google.com/open?id=1fAbEM6DayxwRVQJwH77_4S9TViXEjbPz

Postgre database:ritzy
password:machinehng

This is the repository for the Data modelling with Post-gre sql using the One million songs datset. 

To run the code below go to your specified directory and clone this repo:

1.Download the required modules in the requirements.txt file.

2.Running Data_Exploration.ipynb does data exploration on a secion of the One millions dataset.

3.Running the create_tables.py script in a terminal creates and initializes the tables for the ritzy database.
  Another file sql_queries.py contains all SQL queries and is imported into create_tables.py.
   
4.Running test.ipynb in a Jupyter notebook confirms that the tables were successfully created with the correct columns.

5.Running the notebook etl.ipynb develops the ETL processes for each table and is used to prepare a python script for processing all the datasets.

6.In a terminal, the python etl.py script is run to process the all the datasets. The script connects to the ritzy database, extracts and processes the log_data and song_data, and loads data into the five tables. The file sql_queries.py contains all SQL queries and is imported into etl.py.

7.Again, running test.ipynb confirms that the records were successfully inserted into each table.

After this is all done, our Postgres database is finally modeled and ready to be queried!
