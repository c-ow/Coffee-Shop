from asyncio.windows_events import NULL
import sqlite3, random, time
con = sqlite3.connect('SQL w Python/coffee shop.db')

daily_sales = 0
daily_earning = 0


def order_maker():
    global currentID
    cur = con.cursor() 
    id = cur.execute (f"select max(id) from orders").fetchone()[0] or 0
    id += 1 
    currentID = id
    name = cur.execute ("select name from names order by random()").fetchone()[0]
    coffee, price = cur.execute ("select name, price from coffee order by random()").fetchone()
    size = cur.execute ("select size, price from sizes order by random()").fetchone()
    food = cur.execute ("select name, price from food order by random()").fetchone()
    price += size[1] + food[1]
    cur.execute (f"insert into orders values ({id}, '{name}', '{coffee}', '{size[0]}', '{food[0]}', {price})")
    print(f"{name} has ordered a {size[0]} {coffee} and a {food[0]}")
    con.commit()
    return id

def payment(x):
    payment = random.choice(["Cash", "Card"])
    if payment == "Cash":
        cash = random.randint(int(x), 100)
        cash = (x + 9)//10 * random.choice([10,20])
        change = cash - x
        print("Total: $%s, Paid: $%s, Change: $%s" % ("{:.2f}".format(x), "{:.2f}".format(cash), "{:.2f}".format(change)) + "\n")
    elif payment == "Card":
        print("Total: $%s, Card Payment" % ("{:.2f}".format(x))+ "\n")

def checkout(id):
    global daily_sales, daily_earning
    cur = con.cursor()
    order = cur.execute (f"select * from orders where id = {id}").fetchone()
    print(f"{order[3]} {order[2]} \n{order[4]}")
    payment(order[5])
    daily_sales += 1
    daily_earning += order[5]

def sim_order():
    delay = random.randint(1,3)
    time.sleep(delay)
    id = order_maker()
    return id

def fulfill_order(id):
    delay = random.randint(1,2)
    time.sleep(delay)
    checkout(id)

end_day = time.time() + random.randint(60,90)
while True:
    id = sim_order()
    fulfill_order(id)
    if time.time() > end_day:
        break

daily_earning = "{:.2f}".format(daily_earning)
print(f"Your shop has made {daily_sales} sales today with total earnings of ${daily_earning}")
cur = con.cursor()
total_sales, total_earning = cur.execute(f"select max(id), sum(price) from orders").fetchone()

print(f"Your shop has made {total_sales} total lifetime sales with total earnings of {total_earning}")