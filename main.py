import duckdb as db
from pathlib import Path

def connect_to_db(read_only: bool = False) -> db.DuckDBPyConnection:
    """
    Connect to the DuckDB database using a path relative to the script location.

    Args:
        read_only (bool): If True, connect in read-only mode.

    Returns:
        db.DuckDBPyConnection: A connection object to the DuckDB database.
    """
    # Get the directory of the current script (__file__)
    script_dir = Path(__file__).parent

    # Navigate two levels up to the project root directory
    project_root = script_dir.parent

    # Construct the path to the database from the project root
    db_path = project_root / "data" / "database" / "ntm.duckdb"

    return db.connect(database=str(db_path), read_only=read_only)

def checkdb(con: db.DuckDBPyConnection):
    """
    A simple function to check if the connection to the database is working and if the table exist, by running a test query.

    Args:
        con (db.DuckDBPyConnection): An active connection to the DuckDB database.

    Returns:
    """



def main():
    con = connect_to_db()
    checkdb(con)

if __name__ == '__main__':
    main()