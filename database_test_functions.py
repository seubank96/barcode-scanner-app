from database import add_product, get_all_products, search_product, update_quantity, remove_product

# Add a test product
add_product("Electronics", "12345", "Iphone", 700.78, 87, 30)

# View all products
get_all_products()

# Search for a product
print(search_product("12345"))

# Update quantity
update_quantity("12345", 3)

# Remove a product
remove_product("12345")
