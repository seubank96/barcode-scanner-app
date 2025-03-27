from product import Product

class Clothing(Product):

    def __init__(self, category, productID, name, price, quantity, returnPeriod, size, color):

        super().__init__(category, productID, name, price, quantity, returnPeriod)

        if isinstance(size, str) and len(size) > 0:

            self.size = size
        else:

            raise ValueError("Error: Invalid size format.")
        
        if isinstance(color, str) and len(color) > 0:

            self.color = color

        else:
            raise ValueError("Error: Invalid color format.")
        

    def getSize(self):

        return self.size
    
    def getColor(self):

        return self.color
    
    def getProductDetails(self):

        return super().getProductDetails() + f", {self.size}, {self.color}"
    
    def __str__(self):

        return super().__str__() + f", Size: {self.size}, Color: {self.color}"