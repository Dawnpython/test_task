import requests

from config import SUPABASE_API, SUPABASE_URL



def insert_orders_to_supabase(rows):
    url = f"{SUPABASE_URL}/rest/v1/design_orders"

    headers = {
        "apikey": SUPABASE_API,
        "Authorization": f"Bearer {SUPABASE_API}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    response = requests.post(url, json=rows, headers=headers)

    if response.status_code not in (200, 201):
        print("Ошибка вставки:", response.status_code, response.text)

