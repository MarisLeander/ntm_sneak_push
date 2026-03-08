import duckdb as db
from write_log import log_error

def insert_sneak(con: db.DuckDBPyConnection, sneak: dict[str, str]):
    """ Insert a sneak performance into the Sneak table in the database.
    :param con: An active connection to the DuckDB database.
    :param sneak: A dictionary containing the details of the sneak performance, with keys 'date', 'location', 'ticket_link' and 'ical_link'.
    :return: None
    """
    con.execute("""
                INSERT INTO Sneak (date, location, ticket_link, ical_link)
                VALUES (?, ?, ?, ?) ON CONFLICT DO NOTHING;
                """, [sneak['date'], sneak['location'], sneak['ticket_link'], sneak['ical_link']])

def insert_premiere(con: db.DuckDBPyConnection, premiere: dict[str, str]):
    """ Insert a premiere performance into the Premiere table in the database.
    :param con: An active connection to the DuckDB database.
    :param premiere: A dictionary containing the details of the premiere performance, with keys 'datetime', 'location', 'details_link',
                    'title', 'writer', 'length' and 'description'.
    :return: None
    """
    con.execute("""
                INSERT INTO Premiere (date, location, link, title, writer, length, description)
                VALUES (?, ?, ?, ?, ?, ?, ?) ON CONFLICT DO NOTHING;
                """, [
                    premiere['datetime'],
                    premiere['location'],
                    premiere['details_link'],
                    premiere['title'],
                    premiere['writer'],
                    premiere['length'],
                    premiere['description']
                ])


def insert_scraping_log(con: db.DuckDBPyConnection, success: bool, message: str) -> int:
    """ Insert a scraping log entry into the ScrapingLog table in the database.
    :param con: An active connection to the DuckDB database.
    :param success: A boolean indicating whether the scraping was successful or not.
    :param message: A string containing any relevant message about the scraping process.
    :return: The ID of the newly inserted scraping log entry.
    """

    # Using RETURNING id at the end of the query, and fetchone() to grab the result
    result = con.execute("""
                         INSERT INTO ScrapingLog (date, success, message)
                         VALUES (CURRENT_TIMESTAMP, ?, ?) RETURNING id;
                         """, [success, message]).fetchone()

    return result[0] if result else None

def insert_new_sneak(con: db.DuckDBPyConnection, premiere_id: int, sneak: dict[str, str], scraping_id: int):
    """ Insert a new sneak performance into the NewSneak table in the database, linking it to the corresponding premiere and scraping log.
    :param con: An active connection to the DuckDB database.
    :param premiere_id: The ID of the matching premiere performance (can be None if no match was found).
    :param sneak: A dictionary containing the details of the sneak performance, with keys 'date', 'location', 'ticket_link' and 'ical_link'.
    :param scraping_id: The ID of the scraping log entry for this scraping run.
    :return: None
    """
    # First, we need to get the ID of the sneak we just inserted (or that already exists)
    result = con.execute("""
                         SELECT id FROM Sneak WHERE date = ? AND location = ? AND ticket_link = ?;
                         """, [sneak['date'], sneak['location'], sneak['ticket_link']]).fetchone()

    sneak_id = result[0] if result else None

    if sneak_id is not None:
        con.execute("""
                    INSERT INTO NewSneak (scrape_id, sneak_id, premiere_id)
                    VALUES (?, ?, ?) ON CONFLICT DO NOTHING;
                    """, [scraping_id, sneak_id, premiere_id])
    else:
        log_error(f"Failed to find sneak ID for sneak with date {sneak['date']} and location {sneak['location']} after insertion.")
