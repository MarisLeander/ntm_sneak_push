import duckdb as db

def insert_sneak(con: db.DuckDBPyConnection, sneak: dict[str, str]):
    con.execute("INSERT INTO sneaks VALUES (?, ?, ?, ?) ON CONFLICT DO NOTHING;",
                (sneak['date'], sneak['location'], sneak['ticket_link'], sneak['ical_link']))

def insert_premiere(con: db.DuckDBPyConnection, premiere: dict[str, str]):
    con.execute("INSERT INTO premieres VALUES (?, ?, ?, ?, ?, ?, ?) ON CONFLICT DO NOTHING;",
                (premiere['datetime'], premiere['location'], premiere['details_link'], premiere['title'], premiere['writer'], premiere['length'], premiere['description']))
