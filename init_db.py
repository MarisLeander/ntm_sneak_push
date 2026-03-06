import duckdb as db

def build_db(con:db.DuckDBPyConnection):
    con.execute("CREATE SEQUENCE IF NOT EXISTS sneak_id_seq START 1;")
    # Create the speaker which will be used to identify a speaker
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

    con.execute("""
        CREATE TABLE IF NOT EXISTS NewSneak (
            scrape_date DATE NOT NULL,
            sneak_id INTEGER NOT NULL REFERENCES Sneak(id),
            premiere_id INTEGER NOT NULL REFERENCES Premiere(id),
            PRIMARY KEY (sneak_id, premiere_id)
        )    
        """
    )

    con.execute("""
        
    """
    )
def drop_tables(con:db.DuckDBPyConnection):

def reset_db():
    build_db()