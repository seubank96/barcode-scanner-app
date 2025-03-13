# Product Class

class Product:

    def __init__(self, category, productID, name, price, quantity, returnPeriod):

        if isinstance(category, str) and len(category) > 0:
            self.category = category
        else:
            raise ValueError("Error: Invalid category format.")

        if isinstance(productID, str) and len(productID) > 0:
            self.productID = productID
        elif isinstance(productID, int):
            self.productID = str(productID)
        else:
            raise ValueError("Error: Invalid product ID format.")

        if isinstance(name, str) and len(name) > 0:
            self.name = name
        else:
            raise ValueError("Error: Invalid name format.")
        
        if isinstance(price, (int, float)) and price >= 0:
            self.price = price
        else:
            raise ValueError("Error: Invalid price format.")
        
        if isinstance(quantity, int) and quantity >= 0:
            self.quantity = quantity
        else:
            raise ValueError("Error: Invalid quantity format.")
        
        if isinstance(returnPeriod, int) and returnPeriod >= 0:

            self.returnPeriod = returnPeriod
        else:
            raise ValueError("Error: Invalid return period format.")
        
    def getCategory(self):

        return self.category

    def getProductID(self):
    
        return self.productID
    
    def getName(self):
    
        return self.name
    
    def getPrice(self):
    
        return self.price

    def getQuantity(self):
    
        return self.quantity
    
    def getReturnPeriod(self):

        return self.returnPeriod 
    
    def updateStock(self, amount):

        if amount + self.quantity < 0:

            raise ValueError("Error: Stock quantity cannot be negative.")
        
        elif amount == 0:

            raise ValueError("Error: amount entered cannot be 0.")
        
        else:

            self.quantity += amount

    def getProductDetails(self):

        return f"{self.category}, {self.productID}, {self.name}, {self.price:.2f}, {self.quantity}, {self.returnPeriod}"


    def __str__(self):

        return f"Category: {self.category}, ProductID: {self.productID}, Name: {self.name}, Price: ${self.price:.2f}, Quantity: {self.quantity}, Return Period: {self.returnPeriod}"