"""
build_category_behaviour.py
-------------------------------------------------
Reads orders_with_blacklist.csv
→ calculates return rate per product category
→ flags categories as "often" (≥15 % returns) or "rarely"
→ writes category_behaviour.json
"""

import pandas as pd
import json
from pathlib import Path

# ── config ──────────────────────────────────────────────
INPUT_CSV = "orders_with_blacklist.csv"   # make sure it exists!
OUTPUT_JSON = "category_behaviour.json"
THRESHOLD = 0.15                          # 15 % return rate → “often”

# ── 1. load data ────────────────────────────────────────
if not Path(INPUT_CSV).is_file():
    raise FileNotFoundError(f"{INPUT_CSV} not found. "
                            "Place it in the same folder then rerun.")

orders = pd.read_csv(INPUT_CSV)

# ── 2. sanity check ─────────────────────────────────────
if "Product Category" not in orders.columns or "Returns" not in orders.columns:
    raise ValueError("CSV must have 'Product Category' and 'Returns' columns.")

# ── 3. compute return stats ────────────────────────────
stats = (
    orders.groupby("Product Category")["Returns"]
    .agg(total_orders="count", total_returns="sum")
)
stats["return_rate"] = stats["total_returns"] / stats["total_orders"]

# ── 4. label behaviour ─────────────────────────────────
stats["behaviour"] = stats["return_rate"].apply(
    lambda r: "often" if r >= THRESHOLD else "rarely"
)

# ── 5. save json ───────────────────────────────────────
behaviour_dict = stats["behaviour"].to_dict()
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(behaviour_dict, f, indent=2, ensure_ascii=False)

print("✅ Saved", OUTPUT_JSON)
print(stats[["total_orders", "total_returns", "return_rate", "behaviour"]])
