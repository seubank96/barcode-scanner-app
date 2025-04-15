# Inventory database management module

import sqlite3  # ✅ Built-in library for lightweight relational databases – supports reproducibility & data persistence

# ✅ Modular function for consistent database access
def connect_db():
    conn = sqlite3.connect("inventory.db")  # Opens or creates the SQLite database file
    return conn

# ✅ Structured data storage: initializing table schema – a principle of clean data handling
def initialize_database():
    conn = connect_db()
    cursor = conn.cursor()

    # ✅ Table definition with strict types & constraints (helps maintain data integrity and reproducibility)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,        -- Auto-incrementing unique identifier
            category TEXT NOT NULL,                      -- Product category (e.g., electronics)
            productID TEXT UNIQUE NOT NULL,              -- Unique identifier (barcode/QR)
            name TEXT NOT NULL,                          -- Product name
            price REAL NOT NULL,                         -- Floating point for currency values
            quantity INTEGER NOT NULL DEFAULT 1,         -- Inventory tracking
            returnPeriod INTEGER NOT NULL                -- Days allowed for return
        )
    ''')

    conn.commit()  # ✅ Ensures the database changes are saved — transactional reliability
    conn.close()
    print("Database initialized successfully.")

# ✅ CRUD: Add product — uses parameterized SQL queries to prevent injection (secure, clean)
def add_product(category, productID, name, price, quantity, returnPeriod):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO inventory (category, productID, name, price, quantity, returnPeriod) VALUES (?, ?, ?, ?, ?, ?)",
                       (category, productID, name, price, quantity, returnPeriod))
        conn.commit()
        print(f"Added product: {name} (ID: {productID})")
    except sqlite3.IntegrityError:  # ✅ Handles errors gracefully — good practice for robust code
        print(f"Error: Product ID {productID} already exists.")
    finally:
        conn.close()

# ✅ Updating values using basic arithmetic — scientific computing relevance: numerical state update
def update_quantity(productID, quantity_change):
    conn = connect_db()
    cursor = conn.cursor()

    # ✅ Query current quantity (pull from persistent store)
    cursor.execute("SELECT quantity FROM inventory WHERE productID = ?", (productID,))
    result = cursor.fetchone()

    if result:
        new_quantity = result[0] + quantity_change  # ✅ Arithmetic operation on data – reflects computational logic
        cursor.execute("UPDATE inventory SET quantity = ? WHERE productID = ?", (new_quantity, productID))
        conn.commit()
        print(f"Updated quantity for Product ID {productID}: New Quantity = {new_quantity}")
    else:
        print(f"Error: Product ID {productID} not found in inventory.")

    conn.close()

# ✅ Record deletion – ensures clean data state when removing obsolete or incorrect entries
def remove_product(productID):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM inventory WHERE productID = ?", (productID,))
    conn.commit()
    
    if cursor.rowcount > 0:
        print(f"Product ID {productID} removed from inventory.")
    else:  
        print(f"Error: Product ID {productID} not found in inventory.")

    conn.close()

# ✅ Data visualization through console output – interprets relational data for user review
def get_all_products():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM inventory")
    products = cursor.fetchall()

    if products:
        print("\nInventory Data:")
        for row in products:
            print(row)  # ✅ Data inspection — allows for verification and debugging
    else:
        print("No products found in inventory.")

    conn.close()

# ✅ Direct lookup using a key (productID) – efficient for fast access, a concept central to indexed data structures
def search_product(productID):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM inventory WHERE productID = ?", (productID,)) 
    result = cursor.fetchone() 

    conn.close()
    return result  # ✅ Returns the result for use in automation workflows

# ✅ Optional table reset for experimentation or reproducibility (scientific principle)
def reset_inventory():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS inventory")  # Destroys current schema/data
    initialize_database()  # Recreates schema

    conn.commit()
    conn.close()
    print("Inventory database has been reset.")

# ✅ Reproducibility: auto-initialize if run as standalone script
if __name__ == "__main__":
    initialize_database()
