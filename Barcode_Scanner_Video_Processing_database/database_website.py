# Inventory database management module

import sqlite3  # ✅ SCIENTIFIC COMPUTING: Enables structured data storage and retrieval (relational DBMS)

# Connect to the database (or create it if it doesn’t exist)
def connect_db():
    conn = sqlite3.connect("inventory.db")  # ✅ SCIENTIFIC COMPUTING: Persistent data access for reproducible experiments
    return conn

# Initialize the database with a table for products
def initialize_database():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            productID TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            returnPeriod INTEGER NOT NULL
        )
    ''')  # ✅ SCIENTIFIC COMPUTING: Defines schema and enforces data types (data modeling)

    conn.commit()  # ✅ SCIENTIFIC COMPUTING: Ensures atomic transaction
    conn.close()
    print("Database initialized successfully.")

# Add a new product to the database
def add_product(category, productID, name, price, quantity, returnPeriod):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO inventory (category, productID, name, price, quantity, returnPeriod) VALUES (?, ?, ?, ?, ?, ?)",
                       (category, productID, name, price, quantity, returnPeriod)) 
        conn.commit()  # ✅ SCIENTIFIC COMPUTING: Structured data insertion with parameterized query
        print(f"Added product: {name} (ID: {productID})")
    except sqlite3.IntegrityError:  # ✅ SCIENTIFIC COMPUTING: Built-in exception handling ensures robustness and reliability
        print(f"Error: Product ID {productID} already exists.")
    finally:
        conn.close()

# Update the quantity of a product in the database
def update_quantity(productID, quantity_change):
    conn = connect_db()
    cursor = conn.cursor()

    # Retrieve the current quantity of the product
    cursor.execute("SELECT quantity FROM inventory WHERE productID = ?", (productID,))  # ✅ SCIENTIFIC COMPUTING: Query optimization using indexing (via primary key)
    result = cursor.fetchone()

    if result:
        new_quantity = result[0] + quantity_change  # ✅ SCIENTIFIC COMPUTING: Programmatic manipulation of stored data
        
        # Update the quantity in the database
        cursor.execute("UPDATE inventory SET quantity = ? WHERE productID = ?", (new_quantity, productID))
        conn.commit()
        
        print(f"Updated quantity for Product ID {productID}: New Quantity = {new_quantity}")
    else:
        print(f"Error: Product ID {productID} not found in inventory.")

    conn.close()

# Remove a product from the inventory
def remove_product(productID):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM inventory WHERE productID = ?", (productID,))  # ✅ SCIENTIFIC COMPUTING: Safe and traceable deletion with condition
    conn.commit()
    
    if cursor.rowcount > 0:
        print(f"Product ID {productID} removed from inventory.")
    else:  
        print(f"Error: Product ID {productID} not found in inventory.")

    conn.close()

# Retrieve and display all products
def get_all_products():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM inventory")  # ✅ SCIENTIFIC COMPUTING: Bulk retrieval supports analysis and reporting
    products = cursor.fetchall()

    if products:
        print("\nInventory Data:")
        for row in products:
            print(row)
    else:
        print("No products found in inventory.")

    conn.close()

# Search for a product by product ID
def search_product(productID):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM inventory WHERE productID = ?", (productID,))  # ✅ SCIENTIFIC COMPUTING: Conditional data filtering using SQL
    result = cursor.fetchone() 

    conn.close()
    return result  # Returns product info instead of printing it

# Function to reset the entire inventory table
def reset_inventory():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS inventory")  # ✅ SCIENTIFIC COMPUTING: Database management and schema evolution
    initialize_database()  # Recreate the table after dropping it

    conn.commit()
    conn.close()
    print("Inventory database has been reset.")

# Automatically initialize the database when this script runs
if __name__ == "__main__":
    initialize_database()  # ✅ SCIENTIFIC COMPUTING: Automation and reproducibility on module execution
