import psycopg2

def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == '__main__':
    config = load_config()
    conn = connect(config)
    conn2 = connect(config)
    cur = conn.cursor()
    cur2 = conn2.cursor()

    cur.execute("SELECT * FROM cars")
    print(cur.fetchone())

    cur2.execute("SELECT * FROM cars")
    print(cur2.fetchone())