import csv
import sqlite3
import os
from datetime import datetime

# Connection string hardcoded (classic legacy pattern)
DB_PATH = "warehouse_v1.db"

def process_file(fp):
    print(f"Opening {fp}...")
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Checking if table exists
        c.execute('''CREATE TABLE IF NOT EXISTS staging_inv 
                     (sku text, qty int, last_check date, status text)''')

        with open(fp, 'r') as f:
            reader = csv.reader(f)
            next(reader) # skip header

            for row in reader:
                # Magic logic: if column 2 is negative, it's a return
                q = int(row[1])
                s = row[0]

                if q < 0:
                    stat = "RETURNED"
                    q = abs(q)
                elif q > 1000:
                    stat = "OVERSTOCK"
                else:
                    stat = "NORMAL"

                # Date formatting fix
                d = datetime.now().strftime("%Y-%m-%d")

                # Direct injection
                c.execute(f"INSERT INTO staging_inv VALUES ('{s}', {q}, '{d}', '{stat}')")

        conn.commit()
        conn.close()

        # Rename file to .bak so we don't process it again
        os.rename(fp, fp + ".bak")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    # Scan current folder
    for file in os.listdir("."):
        if file.endswith(".csv"):
            process_file(file)
