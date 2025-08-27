import json
import random
from faker import Faker

fake = Faker()

# Number of rows for each table
ROWS = 1000

# 1️⃣ Customers
customers = []
for _ in range(ROWS):
    customers.append({
        "Name": fake.name(),
        "Gender": random.choice(["M", "F"]),
        "BirthDate": fake.date_of_birth(minimum_age=18, maximum_age=70).strftime("%Y-%m-%d"),
        "Phone": fake.msisdn()[:11],
        "Email": fake.email(),
        "City": fake.city()
    })

with open("customers.json", "w", encoding="utf-8") as f:
    json.dump(customers, f, ensure_ascii=False, indent=4)

# 2️⃣ Branches
branches = []
for _ in range(ROWS):
    branches.append({
        "BranchName": fake.company(),
        "City": fake.city(),
        "Address": fake.address()
    })

with open("branches.json", "w", encoding="utf-8") as f:
    json.dump(branches, f, ensure_ascii=False, indent=4)

# 3️⃣ Products
products = []
for _ in range(ROWS):
    products.append({
        "ProductName": fake.word().capitalize(),
        "Category": random.choice(["Electronics", "Clothing", "Food", "Books", "Furniture"]),
        "Price": round(random.uniform(10, 5000), 2),
        "Supplier": fake.company()
    })

with open("products.json", "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=4)

# 4️⃣ Sales
sales = []
for _ in range(ROWS):
    sales.append({
        "CustomerID": random.randint(1, ROWS),
        "BranchID": random.randint(1, ROWS),
        "SaleDate": fake.date_this_decade().strftime("%Y-%m-%d"),
        "TotalAmount": round(random.uniform(50, 20000), 2)
    })

with open("sales.json", "w", encoding="utf-8") as f:
    json.dump(sales, f, ensure_ascii=False, indent=4)

# 5️⃣ SaleDetails
sale_details = []
for _ in range(ROWS):
    qty = random.randint(1, 20)
    price = round(random.uniform(10, 2000), 2)
    sale_details.append({
        "SaleID": random.randint(1, ROWS),
        "ProductID": random.randint(1, ROWS),
        "Quantity": qty,
        "UnitPrice": price,
        "TotalPrice": round(qty * price, 2)
    })

with open("sale_details.json", "w", encoding="utf-8") as f:
    json.dump(sale_details, f, ensure_ascii=False, indent=4)

print("✅ JSON files for all 5 tables have been generated successfully.")
