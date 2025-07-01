from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re

app = Flask(__name__)
CORS(app)  # Allow requests from any origin (useful for frontend testing)

# ─── Load blacklist.json ─────────────────────────────
with open("blacklist.json", encoding="utf-8") as f:
    _bl = json.load(f)

# Clean names for fast lookup
bad_names = {
    re.sub(r"\s+", " ", d["name"].lower()).strip(): d["reason"]
    for d in _bl
}

# ─── Load category_behavior.json ─────────────────────
with open("category_behaviour.json", encoding="utf-8") as f:
    category_behavior = json.load(f)

# Extract categories that are "often" returned
risky_categories = {
    cat for cat, behavior in category_behavior.items()
    if behavior.lower() == "often"
}

# ─── Define Risk Endpoint ────────────────────────────
@app.route("/risk", methods=["POST"])
def assess_risk():
    print('in rout')
    data = request.get_json()

    name = data.get("name", "")
    category = data.get("product_category", "")

    name_clean = re.sub(r"\s+", " ", name.lower()).strip()

    # Check blacklist first
    if name_clean in bad_names:
        return jsonify({
            "final_risk": "High",
            "reason": f"Blacklisted – {bad_names[name_clean]}"
        })

    # Check product category
    if category in risky_categories:
        return jsonify({
            "final_risk": "Medium",
            "reason": "High-return category"
        })

    # Otherwise safe
    return jsonify({
        "final_risk": "Low",
        "reason": "Safe behavior"
    })

# ─── Run Server ───────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
