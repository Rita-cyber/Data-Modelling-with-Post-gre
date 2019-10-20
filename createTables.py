import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def create_database():
    """
    Return cursor and connection to local database
    """
    # connect to default database
    conn = psycopg2.connect("host=127.0.0.1 dbname=ritzy user=ritzy password=machinehng")
    conn.set_session(autocommit=True)
    cur = conn.cursor()
   
    
    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS ritzy")
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()    
    
    # connect to ritzydatabase
    conn = psycopg2.connect("host=127.0.0.1 dbname=ritzy user=ritzy password=machinehng")
    cur = conn.cursor()
    
    return cur, conn


def drop_tables(cur, conn):
    """
    Drop each existing table from ritzy database.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Create tables for ritzy database.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    cur, conn = create_database()
    
    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
