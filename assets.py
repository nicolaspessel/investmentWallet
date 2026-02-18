import datetime as dt, json 

class Transaction:
    def __init__(self, asset_code:str, operation:str, amount:int, price:float) -> None:
        self.asset_code = asset_code
        self.operation = operation  # purchase or sell
        self.amount = amount
        self.price = price
        self.date = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __repr__(self) -> str:
        return f'{self.operation.upper()} EXECUTED! | Date: {self.date} | Asset: {self.asset_code} | Amount: {self.amount} | Price: ${self.price} | Total price: ${self.calculate_total_price()}\n'

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
    

class Asset:
    def __init__(self, code:str, type:str, amount:int = 0, price:float = 0) -> None:
        self.code = code
        self.type = type  
        self.amount = amount
        self.medium_price = price
        self.curr_price = price 

    def __repr__(self):
        return f'Asset: {self.code} | Type: {self.type} | Amount: {self.amount} | Medium price: ${self.medium_price:.2f} | Current price: ${self.curr_price:.2f}'

    def calculate_invested_val(self) -> float | int:  # Here we don't need to pass amount, for example, because the instance
        return self.amount * self.medium_price        # already have the self.amount when initialized, and so does the method.

    def calculate_actual_val(self) -> float | int:
        return self.amount * self.curr_price

    def calculate_valorization(self) -> float | int:  # Calculation functions dont't update values, they calculate and return!
        return self.calculate_actual_val() - self.calculate_invested_val()
    
    def update_price(self, new_price:float) -> None:  # Update functions don't return, they just update values!
        self.curr_price = new_price
    
    def purchase(self, amount:int, price:float) -> None:
        if self.amount == 0:  # First possible purchase
            self.amount = amount
            self.medium_price = price
        else:        
            invested_val = self.calculate_invested_val()
            invested_val += (amount * price)
            self.amount += amount
            self.medium_price = invested_val / self.amount

    def sell(self, amount:int) -> int:
        if amount > self.amount:
            raise ValueError(f'Cannot sell amount {amount} shares, only have {self.amount}.')
        
        self.amount -= amount
        return self.amount        


class Portifolio:
    def __init__(self) -> None:
        self.assets:list[Asset] = []
        self.transactions:list[Transaction] = []
        self._load_transactions()
    
    def _add_asset(self, code:str, type:str, amount:int, price:float) -> None:
        new_asset = Asset(code, type, amount, price)
        self.assets.append(new_asset)
        print(f'New asset {code} added to the portifolio')

    def _add_transaction(self, transaction:Transaction) -> None:
        self.transactions.append(transaction)
        self._save_transaction()

    def buy_asset(self, asset_code:str, asset_type:str, amount:int, price:float) -> None:
        asset = self._get_asset(asset_code)

        if not asset:
            self._add_asset(asset_code, asset_type, amount, price)
        else:
            asset.purchase(amount, price)
            
        transaction = Transaction(asset_code, 'purchase', amount, price)
        self._add_transaction(transaction)

    def sell_asset(self, asset_code:str, amount:int, price:float) -> None:
        asset = self._get_asset(asset_code)

        if not asset:
            print('Asset not found in portfolio. Execute a purchase first.')
            return None
        else:
            try:
                asset.sell(amount)

                transaction = Transaction(asset_code, 'sell', amount, price)
                self._add_transaction(transaction)

                if asset.amount == 0:
                    self.assets.remove(asset)

            except ValueError:
                print(f'It was not possible to sell the asset {asset_code}. Actual amount: {asset.amount}')
                return None                

    def _get_asset(self, code:str) -> Asset | None:        
        for asset in self.assets:
            if asset.code == code:
                return asset
        return None

    def _save_transaction(self) -> None:
        data = [t.convert_to_dict() for t in self.transactions]

        with open('transaction_log.json', 'w', encoding='utf8') as json_file:
            json.dump(data, json_file, indent=4)

    def _load_transactions(self) -> None:        
        try:
            with open('transaction_log.json', 'r', encoding='utf8') as json_file:
                data = json.load(json_file)

                self.transactions = [
                    Transaction(t['asset_code'], t['operation'], t['amount'], t['price'])
                    for t in data
                ]

        except FileNotFoundError:
            self.transactions = []
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from the file.")

    def view_type(self, filter) -> None:
        filter_type =  [a for a in self.assets if a.type == filter]
        print(filter_type)

    def calculate_total_invested(self) -> int | float:
        total = 0
        
        for a in self.assets:
            total += a.calculate_invested_val()
        return total
    
    def calculate_actual_total(self) -> int | float:
        total = 0
        
        for a in self.assets:
            total += a.calculate_actual_val()
        return total

    def calculate_total_valorization(self) -> int | float:
        return self.calculate_total_invested() - self.calculate_actual_total()
    

p = Portifolio()
p.buy_asset('PETR4', 'Action', 10, 40)
print(p.assets)
print(p.transactions)

print(f'Actual total: {p.calculate_actual_total()}\nInvested total: {p.calculate_total_invested()}')
p.buy_asset('PETR4', 'Action', 10, 50)
p.sell_asset('PETR4', 10, 40)

print(f'Actual total: {p.calculate_actual_total()}\nInvested total: {p.calculate_total_invested()}')
print(p.transactions)