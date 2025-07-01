# risk_engine.py
# ---------------------------------------------------------
# Combines blacklist status + product-category behaviour
# to output a single risk label for each order.
#
# Requires:
#   blacklist.json              ← the 120-name file you made
#   category_behaviour.json     ← produced by the return-rate script
# ---------------------------------------------------------

import json
import re
from pathlib import Path

# ── config ──────────────────────────────────────────────
BLACKLIST_FILE  = "blacklist.json"
BEHAVIOUR_FILE  = "category_behaviour.json"

# ── 1. Load and normalise blacklist data once ───────────
def _clean_name(x):
    return re.sub(r"\s+", " ", x.lower()).strip()

with open(BLACKLIST_FILE, encoding="utf-8") as f:
    _bad_names = {
        _clean_name(rec["name"]): rec.get("reason", "Blacklisted")
        for rec in json.load(f)
    }

# ── 2. Load category behaviour table once ───────────────
if not Path(BEHAVIOUR_FILE).is_file():
    raise FileNotFoundError("Run the return-rate script first -> category_behaviour.json")

with open(BEHAVIOUR_FILE, encoding="utf-8") as f:
    _behaviour = json.load(f)          # e.g. {"Books": "often", "Shoes": "rarely"}

# ── 3. Main helper -------------------------------------------------------------
def get_final_risk(name: str, product_category: str) -> dict:
    """
    Returns {
        "final_risk": "High" | "Medium" | "Low",
        "reason": str
    }
    """
    cname = _clean_name(name)

    # 1. Blacklist check
    if cname in _bad_names:
        return {"final_risk": "High", "reason": f"Blacklisted – {_bad_names[cname]}"}

    # 2. Product behaviour check
    behaviour = _behaviour.get(product_category, "rarely")   # default to safe

    if behaviour == "often":
        return {"final_risk": "Medium", "reason": "High-return category"}
    else:   # rarely
        return {"final_risk": "Low", "reason": "No blacklist & low-return category"}

# ── 4. Quick demo  (use `python risk_engine.py` to test) ───────────────────────
if __name__ == "__main__":
    test_orders = [
        {"name": "Yacine Bouzid", "product": "Clothing"},   # blacklisted name
        {"name": "Emma Johnson",   "product": "Clothing"},   # not blacklisted, risky product
        {"name": "Ali Berrah",     "product": "Books"}       # safe
    ]
    for o in test_orders:
        print(o["name"], "→", get_final_risk(o["name"], o["product"]))
