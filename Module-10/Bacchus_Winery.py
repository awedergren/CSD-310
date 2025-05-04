# Team Blue
# Module 10
# Amanda Wedergren
# Miguel Fernandez
# Jonah Aney
# Justin Marucci

import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values

# Load credentials from .env
secrets = dotenv_values(".env")
print("Loaded secrets:", secrets)

# Config object
config = {
    "user": secrets["user"],
    "password": secrets["password"],
    "host": secrets["host"],
    "database": secrets["database"],
    "raise_on_warnings": True
}

# Function to display contents of a table
def show_table(cursor, table_name):
    print(f"\n-- Contents of {table_name} --")
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        if not rows:
            print("  (No records found)")
        else:
            print("  | " + " | ".join(column_names) + " |")
            for row in rows:
                print("  | " + " | ".join(str(col) for col in row) + " |")
    except mysql.connector.Error as err:
        print(f"  Error reading table {table_name}: {err}")

try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    print("\n  Database user '{}' connected to MySQL on host '{}' with database '{}'".format(
        config["user"], config["host"], config["database"]
    ))

    # List of tables you want to show
    tables = [
        "Department", "Manager", "Employees", "Hours", "Wine",
        "Distributor", "Suppliers", "Orders", "Supplies"
    ]

    # Loop through tables and show data
    for table in tables:
        show_table(cursor, table)

    input("\n\n  Press any key to exit...")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")
    else:
        print(err)

finally:
    if 'db' in locals() and db.is_connected():
        cursor.close()
        db.close()
        print("\n  Connection closed.")