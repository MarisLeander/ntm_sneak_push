import sys
import init_db
import scraping
import insert_db
import duckdb as db
from pathlib import Path


def connect_to_db(read_only: bool = False) -> db.DuckDBPyConnection:
    """ Connect to the DuckDB database using a path relative to the script location.
    :param read_only: If True, connect in read-only mode.
    :return: A connection object to the DuckDB database.
    """
    # Get the directory of the current script (__file__)
    script_dir = Path(__file__).parent

    # Navigate two levels up to the project root directory
    project_root = script_dir.parent

    # Construct the path to the database from the project root
    db_path = project_root / "data" / "database" / "ntm.duckdb"

    return db.connect(database=str(db_path), read_only=read_only)

def db_working(con: db.DuckDBPyConnection):
    """ Checks if the database is working by verifying the existence of required tables.
    :param con: An active DuckDB connection object.
    :return: True if all required tables exist, False otherwise.
    """
    tables = ['Sneak', 'Premiere', 'ScrapingLog', 'NewSneak']
    for table in tables:
        exists = con.execute(f"""
                SELECT EXISTS (
                    SELECT 1 
                    FROM information_schema.tables 
                    WHERE table_name = '{table}'
                )
            """).fetchone()[0]
        if not exists:
            # If any table does not exist, print a message and return False
            print(f"Table '{table}' does not exist in the database.")
            return False
    # If all tables exist, return True
    return True

def scrape_new_data(con: db.DuckDBPyConnection):
    sneaks = scraping.get_sneak_performances()
    for sneak in sneaks:
        # Check with the ticketlink and date if the sneak already exists in the database
        exists = con.execute("""
                             SELECT EXISTS (SELECT 1
                                            FROM Sneak
                                            WHERE date = ? AND ticket_link = ?)
                             """, [sneak['ticket_link'], sneak['date']]).fetchone()[0]
        if exists:
            continue
        else:
            insert_db.insert_sneak(con, sneak)
            location = sneak['location']
            premieres = scraping.get_premiere_performances(location=location)
            for premiere in premieres:
                # Check with the link and date if the premiere already exists in the database
                exists = con.execute("""
                                     SELECT EXISTS (SELECT 1
                                                    FROM Premiere
                                                    WHERE date = ? AND link = ?)
                                     """, [premiere['details_link'], premiere['date']]).fetchone()[0]
                if exists:
                    continue
                else:
                    insert_db.insert_premiere(con, premiere)


def main():
    con = connect_to_db()
    if not db_working(con):
        print("Database not build appropriately. Do you want to initialize it? (y/n)")
        answer = input().strip().lower()
        if answer == 'y':
            init_db.initialise_db(con)
        else:
            print("Exiting without initializing the database.")
            sys.exit(1)

if __name__ == '__main__':
    main()