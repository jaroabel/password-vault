
db_queries = {
    "master": """
        CREATE TABLE IF NOT EXISTS master_password(
        id INTEGER PRIMARY KEY,
        password TEXT NOT NULL);
        """,
    "login": """
        CREATE TABLE IF NOT EXISTS vault(
        id INTEGER PRIMARY KEY,
        site_name TEXT NOT NULL,
        website TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL);
        """,
    "insert": """['Google', 'www.google.com', 'joum', 'Test-123'],
        ['Northon', 'www.northon.com', 'jaro', 'jaro-123'],
        ['github', 'www.github.com', 'jmabel', '1234-jmabel']'
        ['Master gold', 'www.mastergold.com', 'jmabel', 'gold#123'],
        ['Apple', 'www.apple.com', 'jeff', 'colt@123']
        """
}