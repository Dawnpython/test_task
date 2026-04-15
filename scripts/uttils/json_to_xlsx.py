import json
from datetime import datetime
from openpyxl import Workbook

with open("scripts/data/raw/mock_orders.json", "r", encoding="utf-8") as f:
    data = json.load(f)

wb = Workbook()
ws = wb.active
ws.title = "Orders"

headers = [
    "Фамилия",
    "Имя",
    "Отчество",
    "Телефон",
    "Email",
    "Подписка",
    "ExternalId клиента",
    "Страна",
    "Дата заказа",
    "Номер заказа",
    "ExternalId заказа",
    "Статус заказа",
    "Тип заказа",
    "Название товара",
    "Количество",
    "Цена",
    "Тип доставки",
    "Адрес",
    "Тип оплаты",
    "Статус оплаты",
    "Комментарий",
    "Дата полной оплаты"
]

ws.append(headers)

client_id = 1
order_id = 1000

today = datetime.now().strftime("%Y-%m-%d")

for order in data:
    full_address = f"{order['delivery']['address']['city']}, {order['delivery']['address']['text']}"
    comment = order.get("customFields", {}).get("utm_source", "")

    for item in order["items"]:
        row = [
            order.get("lastName"),
            order.get("firstName"),
            "",  # отчество
            order.get("phone"),
            order.get("email"),
            "",  # подписка
            client_id,
            "Казахстан",
            today,
            order_id,
            f"ext_{order_id}",
            "Новый", # статус заказа
            "Основной", # Тип клиента, основной - физ лицо
            item.get("productName"),
            item.get("quantity"),
            item.get("initialPrice"),
            "",  # тип доставки
            full_address,
            "",  # тип оплаты
            "",  # статус оплаты
            comment,
            ""   # дата полной оплаты
        ]

        ws.append(row)

    client_id += 1
    order_id += 1

wb.save("scripts/data/output/orders.xlsx")

""" 
PROMT:
напиши python скрипт для добавления данных из json в xlsx таблицу.
Пример Json:
[
  {
    "firstName": "Айгуль",
    "lastName": "Касымова",
    "phone": "+77001234501",
    "email": "aigul.kasymova@example.com",
    "orderType": "eshop-individual",
    "orderMethod": "shopping-cart",
    "status": "new",
    "items": [
      {
        "productName": "Корректирующее бельё Nova Classic",
        "quantity": 1,
        "initialPrice": 15000
      }
    ],
    "delivery": {
      "address": {
        "city": "Алматы",
        "text": "ул. Абая 150, кв 12"
      }
    },
    "customFields": {
      "utm_source": "instagram"
    }
  },
  {
    "firstName": "Дина",
    "lastName": "Жуматова",
    "phone": "+77012345602",
    "email": "dina.zhumatova@example.com",
    "orderType": "eshop-individual",
    "orderMethod": "shopping-cart",
    "status": "new",
    "items": [
      {
        "productName": "Утягивающий комбидресс Nova Slim",
        "quantity": 1,
        "initialPrice": 28000
      },
      {
        "productName": "Корректирующие шорты Nova Shape",
        "quantity": 1,
        "initialPrice": 12000
      }
    ],
    "delivery": {
      "address": {
        "city": "Алматы",
        "text": "мкр. Самал-2, д. 44, кв 78"
      }
    },
    "customFields": {
      "utm_source": "google"
    }
  },
  {
    "firstName": "Нургуль",
    "lastName": "Ахметова",
    "phone": "+77023456703",
    "email": "nurgul.akhmetova@example.com",
    "orderType": "eshop-individual",
    "orderMethod": "shopping-cart",
    "status": "new",
    "items": [
      {
        "productName": "Бюстье корректирующее Nova Lift",
        "quantity": 1,
        "initialPrice": 22000
      },
      {
        "productName": "Утягивающие леггинсы Nova Fit",
        "quantity": 2,
        "initialPrice": 18000
      }
    ],
    "delivery": {
      "address": {
        "city": "Астана",
        "text": "пр. Туран 45, кв 3"
      }
    },
    "customFields": {
      "utm_source": "instagram"
    }
  },
...
Поля, которые надозаполнить в экселе (они идут по порядку):
Фамилия - lastName
Имя (обязательно) - firstName
Отчество - [пропуск, его нет]
Номер телефона - phone
E-mail - email
Подписан на e-mail рассылку (да/нет) - пропуск
ExternalId клиента - сгенерируй уникальный (можно просто порядковый номер)
Страна (обязательно) - Казахстан у всех
Дата заказа - дата когда добавляем данные
Номер заказа -  сгенерируй уникальный
ExternalId заказа - сгенерируй уникальный
Статус заказа - status
Тип заказа (обязательно) - orderType
Название товара - в ключе items есть productName
Количество товара - quantity
Стоимость продажи товара - initialPrice
Тип доставки - пропуск
Адрес доставки - delivery, внутри надо объединить city и text это и будет полный адрес
Тип оплаты - пропуск
Статус оплаты - пропуск
Комментарий к заказу - customFields ->  utm_source
Дата полной оплаты - пропуск
"""