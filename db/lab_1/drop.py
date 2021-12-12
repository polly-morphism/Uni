import psycopg2
import os


def get_env(name):
    return os.environ.get(name)


if __name__ == "__main__":
    conn = psycopg2.connect(
        dbname=get_env("db_name"),
        user=get_env("db_user"),
        password=get_env("db_password"),
        host=get_env("db_url"),
    )
    cursor = conn.cursor()
    cursor.execute("DROP TABLE zno_table, lastrowtable;")
    conn.commit()
    cursor.close()
    conn.close()