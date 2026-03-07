import duckdb as db

def insert_sneak(con: db.DuckDBPyConnection, sneak: dict[str, str]):
    con.execute("""
                INSERT INTO Sneak (date, location, ticket_link, ical_link)
                VALUES (?, ?, ?, ?) ON CONFLICT DO NOTHING;
                """, [sneak['date'], sneak['location'], sneak['ticket_link'], sneak['ical_link']])

def insert_premiere(con: db.DuckDBPyConnection, premiere: dict[str, str]):
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
