from product import Product

class Electronics(Product):

    def __init__(self, category, productID, name, price, quantity, returnPeriod):

        super().__init__(category, productID, name, price, quantity, returnPeriod)    