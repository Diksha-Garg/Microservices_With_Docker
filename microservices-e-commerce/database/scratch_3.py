import json
with open('bookings.json', 'r') as f:
    data = json.load(f)

print(data['pooja_kalra']['2019_12_25'])