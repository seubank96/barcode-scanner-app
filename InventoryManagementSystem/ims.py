# Inventory database management module

from product import Product
from electronics import Electronics
from clothing import Clothing

import sqlite3

class IMS:

    def __init__(self):

        self.products = dict()

    def addProduct(self, product):

        if isinstance(product, Product):
            self.products.update({product.getProductID(): product})
        else:
            raise ValueError("Error: Product is not valid.")

    def removeProduct(self, productID):

        if productID in self.products.keys():
            del self.products[productID]
        else:
            raise ValueError("Error: Product ID not found in inventory.")


    def displayAllProducts(self):

        if self.isEmpty():

            print("Error: Inventory is empty.")
            return
        
        for product in self.products.values():

            print(product)

    def isEmpty(self):

        return len(self.products) == 0
    
    def searchProductByID(self, productID):

        if productID in self.products.keys():

            return self.products.get(productID)
        
        return None
    
    def sortByProductID(self):

        if self.isEmpty():
            return "Error: inventory is empty."
        
        self.products = dict(sorted(self.products.items()))

        return "Inventory successfully sorted by product ID."
    
    def loadDataFromFile(self):
        pass 

    def saveDataToFile(self):
        pass #todo