import csv, random, textwrap, os

out_dir = "app/generated"   # choose folder; change if you want
os.makedirs(out_dir, exist_ok=True)

# 1) login.csv: realistic SauceDemo users repeated to 500 rows
sauce_users = ["standard_user","locked_out_user","problem_user","performance_glitch_user","error_user","visual_user"]
login_path = os.path.join(out_dir, "testdata_login.csv")
with open(login_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["username","password","csrf_token"])
    for i in range(500):
        user = sauce_users[i % len(sauce_users)]
        writer.writerow([user, "secret_sauce", f"token_{i:04d}"])

# 2) products.csv: product_id (1-6), category_id random, search_keyword from list
keywords = ["shoes","backpack","tshirt","bike_light","jacket","watch"]
product_path = os.path.join(out_dir, "testdata_products.csv")
with open(product_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["product_id","category_id","search_keyword"])
    for i in range(500):
        pid = (i % 6) + 1  # 1..6
        cat = random.randint(1,10)
        kw = random.choice(keywords)
        writer.writerow([pid, cat, kw])

# 3) checkout.csv: names, zip, address, payment id, cart id, promo
first_names = ["Rahul","Asha","John","Priya","Alex","Sam","Taylor","Jordan","Casey","Morgan"]
last_names = ["Dey","Sen","Kumar","Das","Smith","Lee","Patel","Nguyen","Garcia","Brown"]
checkout_path = os.path.join(out_dir, "testdata_checkout.csv")
with open(checkout_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["cart_id","item_id","quantity","first_name","last_name","postal_code","address","payment_id","promo"])
    for i in range(500):
        cart = f"C{i+1000}"
        item = f"I{random.randint(1000,9999)}"
        qty = random.randint(1,3)
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        postal = f"{random.randint(10000,99999)}"
        addr = f"{random.randint(1,999)} Main St"
        pay = f"PAY{random.randint(1,500)}"
        promo = random.choice(["NEW50","FLAT10","SAVE20","NONE","WELCOME"])
        writer.writerow([cart,item,qty,fn,ln,postal,addr,pay,promo])