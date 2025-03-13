from product import Product
from electronics import Electronics
from clothing import Clothing
from ims import IMS

ims = IMS()

validCategories = ["electronics", "clothing", "groceries"]

while True:

    if ims.isEmpty():

        print("\n=== Inventory System ===\n")
        print("1. Add Product")
        print("2. Load Data from File")
        print("3. Exit")
        
        try:
            
            userInputTemp = int(input("\nSelect an option: "))
        
        except ValueError:

            print("\nError: user input.")
        

        if userInputTemp == 1:

            userInput = 1

        elif userInputTemp == 2:

            userInput = 8

        elif userInputTemp == 3:
        
            userInput = 11

        else:

            print("\nError: invalid input.")

            continue

    else:

        print("\n=== E-Commerce Inventory System ===\n")
        print("1. Add Product")
        print("2. Display All Products")
        print("3. Search Product")
        print("4. Get Product Details")
        print("5. Sort Products")
        print("6. Update Stock for a Product")
        print("7. Save Data to File")
        print("8. Load Data from File")
        print("9. Remove Product")
        print("10. Calculate Shipping Cost")
        print("11. Exit")

        try:
            
            userInput = int(input("\nSelect an option: "))
        
        except ValueError:

            print("\nError: user input.")

    if userInput == 1:

        try:  
            
            category = input("\nEnter the product category (Electronics, Clothing, or Groceries): ")

            category = category.strip().lower()

            if category not in validCategories:

                print("\nError: Invalid category.")

                continue

            productID = input("Enter the product ID: ")

            if productID in ims.products.keys():

                print("\nError: Product ID already exists in inventory.")

                continue

            productName = input("Enter the product name: ")
            
            productPrice = int(input("Enter the product price: "))

            productQuantity = int(input("Enter the product quantity: "))

            productReturnPeriod = int(input("Enter the product return period in days: "))

            tempProduct = None

            if category == validCategories[0]:

                tempProduct = Electronics(category, productID, productName, productPrice, productQuantity, productReturnPeriod)

            if category == validCategories[1]:

                productSize = input("Enter the product size: ")

                productColor = input("Enter the product color: ")

                tempProduct = Clothing(category, productID, productName, productPrice, productQuantity, productReturnPeriod, productSize, productColor)

            if category == validCategories[2]:

                pass

            if tempProduct != None:

                ims.addProduct(tempProduct)

                print("\nProduct added successfully to inventory.")

        except ValueError:

            print("\nError: Invalid input.")

    elif userInput == 2:

        print("\nDisplaying all products:")

        ims.displayAllProducts()

    elif userInput == 3:

        searchProductID = input("\nEnter Product ID to search: ")

        if ims.searchProductByID(searchProductID) != None:

            print(f"\nProduct ID {searchProductID} found in inventory.")

        else:

            print(f"\nProduct ID {searchProductID} not found in inventory.")

    elif userInput == 4:
        
        searchProductID = input("\nEnter Product ID: ")

        productDetails = ims.searchProductByID(searchProductID)

        if (productDetails == None):

            print(f"\nError: Product ID {searchProductID} found in inventory.")

            continue

        print(productDetails)


    elif userInput == 5:

        pass





            




            


            
        

