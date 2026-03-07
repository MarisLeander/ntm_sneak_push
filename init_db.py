import duckdb as db

def initialise_db(con:db.DuckDBPyConnection):
    """ Build the database tables for Sneak, Premiere, ScrapingLog and NewSneak.
    :param con: An active connection to the DuckDB database.
    :return: None
    """

    con.execute("CREATE SEQUENCE IF NOT EXISTS sneak_id_seq START 1;")
    con.execute("""
        CREATE TABLE IF NOT EXISTS Sneak (
            id INTEGER DEFAULT nextval('sneak_id_seq') UNIQUE,
            date DATE NOT NULL,
            location VARCHAR NOT NULL,
            link VARCHAR NOT NULL,
        )
        """
    )

    con.execute("CREATE SEQUENCE IF NOT EXISTS premiere_id_seq START 1;")
    con.execute("""
        CREATE TABLE IF NOT EXISTS Premiere (
            id INTEGER DEFAULT nextval('premiere_id_seq') UNIQUE,
            date DATE NOT NULL,
            location VARCHAR NOT NULL,
            link VARCHAR NOT NULL,
            title VARCHAR NOT NULL,
            writer VARCHAR NOT NULL,
            length INTEGER NOT NULL,
            description VARCHAR NOT NULL
        )
        """
    )
    con.execute("CREATE SEQUENCE IF NOT EXISTS scraping_id_seq START 1;")
    con.execute("""
        CREATE TABLE IF NOT EXISTS ScrapingLog (
            id INTEGER DEFAULT nextval('scraping_id_seq') UNIQUE,
            date DATE NOT NULL,
            success BOOLEAN NOT NULL,
            message VARCHAR
        )
    """
    )

    con.execute("""
        CREATE TABLE IF NOT EXISTS NewSneak (
            scrape_id INTEGER NOT NULL REFERENCES ScrapingLog(id),
            sneak_id INTEGER NOT NULL REFERENCES Sneak(id),
            premiere_id INTEGER NOT NULL REFERENCES Premiere(id),
            PRIMARY KEY (scrape_id, sneak_id, premiere_id)
        )    
        """
    )

    print("Database tables have been created successfully.")

def drop_tables(con:db.DuckDBPyConnection):
    """ Drop the database tables for Sneak, Premiere, ScrapingLog and NewSneak, as well as the sequences for the ids.
    :param con: An active connection to the DuckDB database.
    :return: None
    """
    con.execute("DROP SEQUENCE IF EXISTS sneak_id_seq;")
    con.execute("DROP SEQUENCE IF EXISTS premiere_id_seq;")
    con.execute("DROP SEQUENCE IF EXISTS scraping_id_seq;")
    con.execute("DROP TABLE IF EXISTS Sneak;")
    con.execute("DROP TABLE IF EXISTS Premiere;")
    con.execute("DROP TABLE IF EXISTS ScrapingLog;")
    con.execute("DROP TABLE IF EXISTS NewSneak;")

def reset_db(con:db.DuckDBPyConnection):
    """ Reset the database by dropping the existing tables and sequences, and then rebuilding them.
        This will effectively clear all data from the database while keeping the structure intact.
    :param con: An active connection to the DuckDB database.
    :return: None
    """
    drop_tables(con)
    initialise_db(con)
    print("Database has been reset successfully.")