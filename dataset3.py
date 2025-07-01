import pandas as pd, random
from faker import Faker

fake = Faker()
orders = pd.read_csv("orders_algerianized.csv")

def synth_order(cat, return_prob):
    return {
        "Customer Name": fake.name(),
        "Product Category": cat,
        "Product Price": round(random.uniform(500, 8000), 2),
        "Quantity": random.randint(1, 3),
        "Payment Method": random.choice(["Card", "Cash"]),
        "Returns": 1 if random.random() < return_prob else 0
    }

# ⬇️ add 500 synthetic 'Books' orders, only 8 % returns
new_rows = [synth_order("Books", 0.08) for _ in range(500)]
orders = pd.concat([orders, pd.DataFrame(new_rows)], ignore_index=True)

# save & redo behaviour script
orders.to_csv("orders_with_blacklist.csv", index=False)
