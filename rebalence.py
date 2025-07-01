"""
rebalance_returns.py
-----------------------------------------------------------
Rebalances each product-category so overall distribution is:
  • 2 categories < 15 %
  • 2 categories 17–22 %
  • 1 category 25 %+
-----------------------------------------------------------
"""

import pandas as pd
import numpy as np
from math import ceil
from faker import Faker
from pathlib import Path
import random

faker = Faker()

# ── CONFIG ───────────────────────────────────────────────
SOURCE_FILE = "orders_balanced.csv"   # your current file
OUTPUT_FILE = "orders_final.csv"

# target return-rate bands you want for each category
# key = band label, value = desired % range (low, high)
TARGETS = {
    "low":  (0.08, 0.14),   # < 15 %
    "mid":  (0.17, 0.22),   # ~18–22 %
    "high": (0.25, 0.32)    # > 25 %
}

# choose which category gets which band
CATEGORY_BANDS = {
    "Beauty":      "low",
    "Books":       "high",
    "Clothing":    "mid",
    "Electronics": "mid",
    "Shoes":       "low"
}

# ── 1. LOAD DATA ─────────────────────────────────────────
if not Path(SOURCE_FILE).is_file():
    raise FileNotFoundError(f"{SOURCE_FILE} not found.")

df = pd.read_csv(SOURCE_FILE)

# ── 2. HELPER TO ADD SAFE ROWS ───────────────────────────
def add_safe_rows(df, category, n_rows):
    rows = []
    for _ in range(n_rows):
        qty   = random.randint(1, 3)
        price = round(random.uniform(800, 5000), 2)
        rows.append({
            "Customer Name": faker.name(),
            "Product Category": category,
            "Product Price": price,
            "Quantity": qty,
            "Total Purchase Amount": round(price * qty, 2),
            "Payment Method": random.choice(["Card", "Cash"]),
            "Customer Age": random.randint(18, 55),
            "Returns": 0,                         # mark as non-returned
            "Age": random.randint(18, 55),
            "Gender": random.choice(["Male", "Female"]),
            "Churn": random.choice([0, 1])
        })
    return pd.concat([df, pd.DataFrame(rows)], ignore_index=True)

# ── 3. ADJUST EACH CATEGORY TO ITS TARGET BAND ───────────
for cat, band in CATEGORY_BANDS.items():
    low_pct, high_pct = TARGETS[band]
    
    # current stats
    subset = df[df["Product Category"] == cat]
    total_orders  = len(subset)
    total_returns = subset["Returns"].sum()
    current_rate  = total_returns / total_orders if total_orders else 0
    
    # pick a random target within the band
    target_rate = np.random.uniform(low_pct, high_pct)
    
    if current_rate > target_rate:
        # need to add safe orders to LOWER the rate
        needed_safe = ceil((total_returns / target_rate) - total_orders)
        print(f"{cat}: {current_rate:.2%} → {target_rate:.2%}  |  "
              f"adding {needed_safe} safe rows")
        df = add_safe_rows(df, cat, needed_safe)
    elif current_rate < target_rate:
        # need to add RETURNED rows to RAISE the rate
        needed_bad = ceil((target_rate * total_orders - total_returns)
                          / (1 - target_rate))
        print(f"{cat}: {current_rate:.2%} → {target_rate:.2%}  |  "
              f"adding {needed_bad} returned rows")
        df = add_safe_rows(df, cat, 0)  # you can write similar add_bad_rows
        bad_rows = df.tail(needed_bad).index
        df.loc[bad_rows, "Returns"] = 1

# ── 4. SAVE & PRINT SUMMARY ─────────────────────────────
df.to_csv(OUTPUT_FILE, index=False)

summary = (
    df.groupby("Product Category")["Returns"]
        .agg(total_orders="count", total_returns="sum")
        .assign(return_rate=lambda x: x["total_returns"] / x["total_orders"],
                behaviour=lambda x: np.where(
                    x["return_rate"] < 0.15, "rarely",
                    np.where(x["return_rate"] > 0.25, "often", "mid")
                ))
)

print(f"\n✅ Saved {OUTPUT_FILE}\n")
print(summary.to_string())
import pandas as pd
import matplotlib.pyplot as plt

# Load your final dataset
df = pd.read_csv("orders_final.csv")

# Calculate per-category stats
summary = (
    df.groupby("Product Category")["Returns"]
      .agg(total_orders="count", total_returns="sum")
      .reset_index()
)
summary["return_rate"] = summary["total_returns"] / summary["total_orders"]

# Add behavior labels (optional)
def label_behavior(rate):
    if rate < 0.15:
        return "rarely"
    elif rate < 0.25:
        return "mid"
    else:
        return "often"

summary["behavior"] = summary["return_rate"].apply(label_behavior)

# Define colors by behavior
color_map = {
    "rarely": "#27ae60",   # green
    "mid": "#f39c12",      # orange
    "often": "#e74c3c"     # red
}
colors = summary["behavior"].map(color_map)

# Plot
plt.figure(figsize=(10, 6))
bars = plt.bar(
    summary["Product Category"],
    summary["return_rate"] * 100,
    color=colors
)

plt.title("Return Rate per Product Category (Post-Rebalancing)")
plt.xlabel("Product Category")
plt.ylabel("Return Rate (%)")
plt.ylim(0, 60)
plt.grid(axis='y', linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()
