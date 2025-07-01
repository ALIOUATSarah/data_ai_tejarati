# return_rate_chart.py
# ---------------------------------------------------------
# 1. Read merged order dataset
# 2. Calculate return rate per product category
# 3. Plot and save a bar chart
# ---------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ── CONFIG ───────────────────────────────────────────────
CSV_PATH   = "orders_merged.csv"   # <— your merged dataset
OUTPUT_PNG = "return_rate_chart.png"
THRESHOLD  = 0.15                  # optional visual threshold (15 %)

# ── 1. Load data ─────────────────────────────────────────
if not Path(CSV_PATH).is_file():
    raise FileNotFoundError(f"{CSV_PATH} not found")

df = pd.read_csv(CSV_PATH)

# ── 2. Aggregate return stats ────────────────────────────
stats = (
    df.groupby("Product Category")["Returns"]
      .agg(total_orders="count", total_returns="sum")
)
stats["return_rate"] = stats["total_returns"] / stats["total_orders"] * 100
stats = stats.sort_values("return_rate", ascending=False)

# ── 3. Plot ──────────────────────────────────────────────
plt.figure(figsize=(10, 6))
bars = plt.bar(
    stats.index,
    stats["return_rate"],
)

# Optional: color categories above threshold
for bar, rate in zip(bars, stats["return_rate"]):
    if rate >= THRESHOLD * 100:
        bar.set_color("#E87C0E")   # orange for “often returned”
    else:
        bar.set_color("#4CAF50")   # green for “rarely returned”

plt.title("Return Rate per Product Category")
plt.xlabel("Product Category")
plt.ylabel("Return Rate (%)")
plt.grid(axis="y", linestyle=":", alpha=0.4)
plt.tight_layout()

# ── 4. Save & show ───────────────────────────────────────
plt.savefig(OUTPUT_PNG, dpi=300)
plt.show()

print(f"✅ Chart saved to {OUTPUT_PNG}")
