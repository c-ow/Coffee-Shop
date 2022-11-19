import sqlite3, random, time
import classes
con = sqlite3.connect('SQL w Python/coffee shop.db')
cur = con.cursor() 

daily_sales = 0
daily_earning = 0

def new_order_maker():
    list_coffee = cur.execute ('select name, price from coffee').fetchall()
    coffees = {}
    for i in list_coffee:
        coffees[i[0]] = classes.Coffee(i[0], i[1])

    list_sizes = cur.execute ('select size, price from sizes').fetchall()
    sizes = {}
    for i in list_sizes:
        sizes[i[0]] = classes.Sizes(i[0], i[1])

    list_food = cur.execute ('select name, price from food').fetchall()
    foods = {}
    for i in list_food:
        foods[i[0]] = classes.Food(i[0], i[1])

    rand_name = cur.execute ('select name from names order by random()').fetchone()[0]
    rand_coffee = random.choice(list(coffees.values()))
    rand_size = random.choice(list(sizes.values()))
    rand_food = random.choice(list(foods.values()))

    new_order = classes.Order(rand_name, rand_coffee, rand_size, rand_food)

    cur.execute (f"insert into orders (name, coffee, size, food, price) values ('{new_order.name}', '{new_order.coffee.name}', '{new_order.size.size}', '{new_order.food.name}', {new_order.get_total_price()})")
    con.commit()
    print(new_order.about_order())
    return new_order

def payment(order_total):
    payment = random.choice(["Cash", "Card"])
    if payment == "Cash":
        cash = random.randint(int(order_total), 100)
        cash = (order_total + 9)//10 * random.choice([10,20])
        change = cash - order_total
        print("Total: $%s, Paid: $%s, Change: $%s" % ("{:.2f}".format(order_total), "{:.2f}".format(cash), "{:.2f}".format(change)) + "\n")
    elif payment == "Card":
        print("Total: $%s, Card Payment" % ("{:.2f}".format(order_total))+ "\n")

def checkout(order):
    global daily_sales, daily_earning
    payment(order.get_total_price())
    daily_sales += 1
    daily_earning += order.get_total_price()

def sim_order():
    delay = random.randint(1,3)
    time.sleep(delay)
    new_order = new_order_maker()
    return new_order

def fulfill_order(order):
    delay = random.randint(1,2)
    time.sleep(delay)
    checkout(order)

end_day = time.time() + random.randint(60,90)
while True:
    new_order = sim_order()
    fulfill_order(new_order)
    if time.time() > end_day:
        break

daily_earning = "{:.2f}".format(daily_earning)
print(f"Your shop has made {daily_sales} sales today with total earnings of ${daily_earning}")
total_sales, total_earning = cur.execute(f"select max(id), sum(price) from orders").fetchone()
print(f"Your shop has made {total_sales} total lifetime sales with total earnings of {total_earning}")
con.close()