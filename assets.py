class Portifolio():
    ...


class Transaction():
    ...
        

class Assets:
    def __init__(self, code:str, name:str, type:str, amount:int | 0, price:float | 0):
        self.code = code
        self.name = name
        self.type = type  
        self.amount = amount
        self.medium_price = price
        self.curr_price = price 

    def _calculate_invested_val(self):           # Here we don't need to pass amount, for example, because the instance
        return self.amount * self.medium_price  # already have the self.amount when initialized, and so does the method.

    def _calculate_actual_val(self):
        return self.amount * self.curr_price

    def calculate_valorization(self):  # Calculation functions dont't update values, they calculate and return!
        return self.calculate_actual_val() - self.calculate_invested_val()
    
    def update_price(self, new_price:float):  # Update functions don't return, they just update values!
        self.curr_price = new_price
    
    def purchase(self, amount:int, price:float):
        if self.amount == 0:  # First possible purchase
            self.amount = amount
            self.medium_price = price
        else:        
            invested_val = self.calculate_invested_val()
            invested_val += (amount * price)
            self.amount += amount
            self.medium_price = invested_val / self.amount       