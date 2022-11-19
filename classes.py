class Coffee:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Sizes:
    def __init__(self, size, price):
        self.size = size
        self.price = price

class Food:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Order:
    def __init__(self, name, coffee, size, food):
        self.name = name
        self.coffee = coffee
        self.size = size
        self.food = food
    def get_total_price(self):
        return self.coffee.price + self.size.price + self.food.price
    def about_order(self):
        return f"{self.name} has ordered a {self.size.size} {self.coffee.name} and a {self.food.name} for a total of ${self.get_total_price():.2f}"