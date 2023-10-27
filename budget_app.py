class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=''):
        self.ledger.append({'amount':amount, 'description':description})

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({'amount':-amount, 'description':description})
            return True
        return False

    def get_balance(self):
        return sum(item['amount'] for item in self.ledger)

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {category.name}')
            category.deposit(amount, f'Transfer from {self.name}')
            return True
        return False

    def check_funds(self, amount):
        return  amount <= self.get_balance()

    def __str__(self):
        output = self.name.center(30, '*') + '\n'
        for item in self.ledger:
            output += f'{item["description"][:23].ljust(23)}{item["amount"]:>7.2f}' + '\n'
        output += f'Total {self.get_balance()}' + '\n'
        return output

def create_spend_chart(categories):
    withdrawals = [sum(item['amount'] for item in cat.ledger if item['amount'] < 0) for cat in categories]
    total = sum(withdrawals)

    if total == 0:
        return 'No data to chart'

    percentages = [int(w / total * 10) * 10 + 1 for w in withdrawals]

    chart ='Percentages of withdrawals\n'
    for i in range(100, -1, -10):
        chart += str(i).ljust(3) + '| ' + ' '.join('o' if p >= i else ' ' for p in percentages) + '\n'
    chart += '   ' + '_' *(len(categories) * 3 +1) + '\n'

    max_len = (max(len(cat.name) for cat in categories))
    names = [cat.name.ljust(max_len) for cat in categories]

    for x in zip(*names):
        chart += '   ' + ' '.join(x) + '\n'

    return chart.rstrip() + '  '

food = Category("Food")
clothing = Category("Clothing")
auto = Category("Auto")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, 'restaurant')
food.transfer(50, clothing)
clothing.deposit(100, 'initial deposit')
clothing.withdraw(50.75, "shoes")
clothing.transfer(20, food)
auto.deposit(1000, 'initial deposit')

#auto.withdraw(400, "fuel")
auto.withdraw(15.89, 'oil change')
auto.transfer(50, food)

categories = [food, clothing, auto]

print(food)
print()
print(clothing)
print()
print(auto)

print(create_spend_chart(categories))

