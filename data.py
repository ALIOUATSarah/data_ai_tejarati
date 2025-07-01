from faker import Faker
import random, json

Faker.seed(250000)
fake = Faker()

# Separate pools (feel free to expand them)
first_names = [
    "Yacine", "Khaled", "Sonia", "Farid", "Amel", "Tarek", "Nassima",
    "Walid", "Salima", "Rachid", "Meriem", "Nadir", "Zohra", "Kamel",
    "Amina", "Hichem", "Nour", "Ismail", "Lina", "Abdelkader"
]

family_names = [
    "Bouzid", "Ait Ahmed", "Bensalem", "Boudiaf", "Kaci", "Mehenni",
    "Zerrouki", "Hammoudi", "Benyamina", "Zemmouri", "Haddad", "Belkacem",
    "Amrane", "Guemache", "Kherbache", "Temmar", "Bensaid", "Cheniti",
    "Talbi", "Nezzar"
]

def random_dz_phone():
    prefix = random.choice(['552', '553', '661', '662', '771', '772'])
    number = ''.join(random.choices('0123456789', k=7))
    return f'+213{prefix}{number}'

def random_dz_id():
    return ''.join(random.choices('0123456789', k=16))

def make_blacklist(n_entries=120):
    blacklist = []
    for _ in range(n_entries):
        full_name = f"{random.choice(first_names)} {random.choice(family_names)}"
        entry = {
            "name": full_name,
            "idNumber": random_dz_id(),
            "phoneNumber": random_dz_phone(),
            "reason": random.choice([
                "Chargeback 2024-11", "Fraudulent returns",
                "Multiple address mismatches", "Stolen card usage"
            ])
        }
        blacklist.append(entry)
    return blacklist

# ===== main =====
blacklist = make_blacklist(250000)          # ← change number here as needed

with open('blacklist.json', 'w', encoding='utf-8') as f:
    json.dump(blacklist, f, indent=2, ensure_ascii=False)

print(f"✅ blacklist.json generated with {len(blacklist)} mixed Algerian names.")
