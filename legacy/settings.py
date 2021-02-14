import os

databases = {
    "default": {
        "host": os.environ.get("DB_HOST", "localhost"),
        "port": os.environ.get("DB_PORT", "5432"),
        "user": os.environ.get("DB_USER", "postgres"),
        "password": os.environ.get("DB_PASS", ""),
        "dbname": os.environ.get("DB_NAME", ""),
    }
}
