import pandas as pd
import json
import random

# Load the orders file
orders = pd.read_csv("orders.csv")

# Load the blacklist file
with open("blacklist.json", encoding="utf-8") as f:
    blacklist = json.load(f)

# Extract Algerian-style names and phones
name_phone_pairs = []
for entry in blacklist:
    name = entry.get("name", "Unknown")
    phone = entry.get("phoneNumber", {})
    
    # Ensure phone is a dict
    if isinstance(phone, dict):
        number_str = f'{phone.get("countryCode", "")}{phone.get("areaCode", "")}{phone.get("number", "")}'
    else:
        number_str = "+213000000000"  # fallback

    name_phone_pairs.append((name, number_str))


# If you have fewer blacklist names than orders, allow repetition
expanded_pairs = random.choices(name_phone_pairs, k=len(orders))

# Replace names and generate full phone strings
orders["Customer Name"] = [name for name, phone in name_phone_pairs]
orders["Phone Number"] = [phone for _, phone in name_phone_pairs]


# Save updated orders
orders.to_csv("orders_algerianized.csv", index=False)
print("✅ Updated orders saved as 'orders_algerianized.csv'")
