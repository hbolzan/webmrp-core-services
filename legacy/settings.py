import os

databases = {
    "default": {
        "host": os.eviron.get("DB_HOST", "localhost"),
        "port": os.eviron.get("DB_PORT", "5432"),
        "user": os.eviron.get("DB_USER", "postgres"),
        "password": os.eviron.get("DB_PASS", ""),
        "dbname": os.eviron.get("DB_NAME", ""),
    }
}
