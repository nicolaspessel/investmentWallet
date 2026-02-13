import datetime as dt, json 

class Transaction:
    def __init__(self, asset_code:str, operation:str, amount:int, price:float) -> None:
        self.asset_code = asset_code
        self.operation = operation  # purchase or sell
        self.amount = amount
        self.price = price
        self.date = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __repr__(self) -> str:
        return f'The operation {self.operation} was executed.\n | Date: {self.date} | Asset: {self.asset_code} \n \
                Amount: {self.amount} | Price: ${self.price} | Total price: ${self._calculate_total_price()}'

    def calculate_total_price(self) -> float | int:
        return self.amount * self.price

    def convert_to_dict(self) -> dict:
        return {
            'operation': self.operation,
            'asset_code': self.asset_code,
            'amount': self.amount,
            'price': self.price,
            'total': self.calculate_total_price(),
            'date': self.date
        }
    

class Assets:
    def __init__(self, code:str, name:str, type:str, amount:int = 0, price:float = 0) -> None:
        self.code = code
        self.name = name
        self.type = type  
        self.amount = amount
        self.medium_price = price
        self.curr_price = price 

    def __repr__(self):
        return f'Asset: {self.code} | Type: {self.type} | Amount: {self.amount} | Medium price: ${self.medium_price:.2f}\n \
                Current price: ${self.curr_price:.2f}'

    def _calculate_invested_val(self) -> float | int:  # Here we don't need to pass amount, for example, because the instance
        return self.amount * self.medium_price         # already have the self.amount when initialized, and so does the method.

    def _calculate_actual_val(self) -> float | int:
        return self.amount * self.curr_price

    def calculate_valorization(self) -> float | int:  # Calculation functions dont't update values, they calculate and return!
        return self.calculate_actual_val() - self.calculate_invested_val()
    
    def update_price(self, new_price:float) :  # Update functions don't return, they just update values!
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