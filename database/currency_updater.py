from connect import connect
from config import load_config
import json
import time

def update_currency():
    config = load_config()
    conn = connect(config)

    with conn.cursor() as cur:
        cur.execute("CALL update_currency()")
    conn.commit()

if __name__ == "__main__":
    while True:
        with open("last_updated.json", "r") as f:
            last_updated_date = json.load(f)["last_update"]
        if time.time() - last_updated_date > 60*60*24:
            print("outofdate")
            json_time = {"last_update": time.time()}
            json_time = json.dumps(json_time)

            with open("last_updated.json", "w") as f:
                f.write(json_time)

            update_currency()

