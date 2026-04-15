# Тестовое задание ТОО GBEMPIRE

## Ссылки

- Дашборд: https://orders-dashboard-delta.vercel.app/
- Репозиторий: https://github.com/Dawnpython/test_task
- Telegram уведомления: [/tg_notify](https://github.com/Dawnpython/test_task/blob/main/tg_notify/%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7.png)

---

## Описание

Проект включает:
- загрузку заказов из JSON
- обработку вложенных данных (items, delivery, customFields)
- запись в Supabase
- отображение и группировку заказов по `external_order_id`
- дашборд для анализа заказов

---

## Особенности реализации

- Группировка строк по `external_order_id` для объединения одного заказа
- Поддержка заказов с несколькими товарами (items)
- Генерация:
  - `external_customer_id`
  - `order_number`
  - `external_order_id`
- Подстановка даты создания при импорте
- Адрес доставки формируется из `city + text`
- Все заказы приводятся к единой структуре Supabase

---

## Supabase

Таблица `orders`:

```sql
create table orders (
    id bigserial primary key,
    last_name text,
    first_name text not null,
    middle_name text,
    phone text,
    email text,
    email_subscription boolean,
    external_customer_id text,
    country text not null default 'Казахстан',
    order_date date,
    order_number text,
    external_order_id text,
    status text,
    order_type text not null,
    product_name text,
    quantity integer,
    price numeric,
    delivery_type text,
    delivery_address text,
    payment_type text,
    payment_status text,
    comment text,
    paid_at timestamp
);
```
<details> <summary>Python: JSON → XLSX</summary>
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
</details> <details> <summary>RetailCRM API: получение заказов с пагинацией</summary>
вот пример из документации

Данное API предназначено для взаимодействия с системой со стороны интеграционных модулей, серверной части сайта, интернет-магазина либо из мобильного приложения. Для взаимодействия с системой из Javascript используйте Daemon Collector.

Важно!

При загрузке заказов/клиентов в систему рекомендуем отключать все триггеры, отвечающие за отправку E-mail и SMS сообщений.
Схема

При работе с API необходимо использовать версию v5. Предыдущие версии API сохранены для совместимости и не рекомендуются к использованию. Запросы необходимо отправлять по адресу:

https://{your-subdomain}.retailcrm.ru/api/{version}/

Все запросы принимаются только по https в кодировке UTF-8. Ответ формируется в JSON-формате.

Данные типа «Дата» указываются в формате Y-m-d (например 2014-03-21), данные типа «Дата/время» — в формате Y-m-d H:i:s (например 2014-03-21 05:14:07).
Авторизация

Авторизация производится с помощью API-ключа, который передается в GET|POST-параметре apiKey:

https://demo.retailcrm.ru/api/v5/orders?apiKey=X2EDxEta9U3lcsSV0dwdF38UvtSCxIuGh

Также API-ключ можно передавать через заголовок X-API-KEY: X2EDxEta9U3lcsSV0dwdF38UvtSCxIuGh

В настройках системы вы найдете раздел по управлению ключами API. В случае отсутствия API-ключа либо в случае, если он неверный, API сообщает об ошибке.

Если API-ключ дает доступ к данным нескольких магазинов, то в некоторых API-методах дополнительно требуется указывать символьный код магазина в GET|POST-параметре site. В справочнике вы можете посмотреть, какие методы требуют указания магазина.
Области действия API-ключей

Доступ API-ключа к API может быть ограничен определенными действиями, которые можно совершать над группами ресурсов (получение или редактирование).

Узнать, какие действия доступны для API-ключа, можно с помощью API метода /api/credentials. В поле scopes будет возвращен массив областей действий, доступный переданному ключу.

Найти информацию о том, какая область API необходима для доступа к методу, можно в описании каждого API метода.
GET-запросы

При обращении к API-методам типа GET параметры необходимо отправлять в виде GET-параметров.

Пример передаваемых данных:

https://demo.retailcrm.ru/api/v5/orders?filter[numbers][]=1235C&filter[customFields][nps][min]=5&apiKey=X2EDxEta9U3lcsSV0dwdF38UvtSCxIuGh
POST-запросы

При обращении к API-методам типа POST параметры необходимо отправлять в формате application/x-www-form-urlencoded. При этом если в каком-либо из параметров передается вложенная структура (например, в методе /api/v*/orders/create данные по заказу в параметре order), то значения таких параметров необходимо передавать в виде JSON-строки.

Пример передаваемых данных:

site=simple-site&order=%7B%22externalId%22%3A%22a123%22%2C%22firstName%22%3A%22Tom%22%7D
Частота обращения к API

При обращении к API разрешается обращаться не чаще 10 запросов в секунду с одного IP. К методам телефонии /api/telephony/* разрешается обращаться не чаще 40 запросов в секунду с одного IP. В случае более высокой нагрузки API будет отдавать ответ:

HTTP/1.1 503 Service Temporarily Unavailable
Постраничная разбивка ответа / Pagination

Постраничная разбивка доступна в запросах с потенциально большим ответом, который разбивается на порции.

В данных запросах помимо самого ответа присутствует мета-информация о постраничной разбивке:


      
HTTP/1.1 200 OK
{ 
    "success": true, 
    "pagination": {
        "limit": 20,
        "totalCount": 1583,
        "currentPage": 1,
        "totalPageCount": 80
    },
    // data
}

Мета-информация о постраничной разбивке включает:

limit — количество элементов в текущем ответе

totalCount — общее количество элементов

currentPage — текущая страница

totalPageCount — общее количество страниц с ответом

Если ответ состоит более чем из одной страницы, в запросе доступен GET-параметр page (по-умолчанию равен 1).

нужна функция, которая возвращает заказы, учти что может быть пагинация, используй print для отображения заказа в консоли

</details> <details> <summary>Пример ответа API</summary>
вот пример ответа

{'success': True, 'pagination': {'limit': 20, 'totalCount': 50, 'currentPage': 1, 'totalPageCount': 3}, 'orders': [{'slug': 104, 'bonusesCreditTotal': 0, 'bonusesChargeTotal': 0, 'id': 104, 'number': '1049', 'externalId': 'ext_1049', 'orderType': 'main', 'orderMethod': 'shopping-cart', 'privilegeType': 'none', 'countryIso': 'KZ', 'createdAt': '2026-04-15 21:43:09', 'statusUpdatedAt': '2026-04-15 21:43:10', 'summ': 81000, 'totalSumm': 81000, 'prepaySum': 0, 'purchaseSumm': 0, 'markDatetime': '2026-04-15 21:43:09', 'lastName': 'Юсупова', 'firstName': 'Феруза', 'phone': '+77090123450', 'email': 'feruza.yusupova@example.com', 'call': False, 'expired': False, 'managerComment': 'referral', 'customer': {'type': 'customer', 'id': 90, 'externalId': '50', 'isContact': False, 'createdAt': '2026-04-15 21:43:09', 'vip': False, 'bad': False, 'site': 'ijoni', 'contragent': {'contragentType': 'individual'}, 'tags': [], 'customFields': [], 'personalDiscount': 0, 'marginSumm': 0, 'totalSumm': 0, 'averageSumm': 0, 'ordersCount': 0, 'segments': [], 'firstName': 'Феруза', 'lastName': 'Юсупова', 'presumableSex': 'female', 'email': 'feruza.yusupova@example.com', 'customerSubscriptions': [{'subscription': {'id': 13, 'channel': 'email', 'name': 'Без тематики', 'code': 'default_marketing', 'active': True, 'autoSubscribe': True, 'ordering': 1}, 'subscribed': True}], 'phones': [{'number': '+77090123450'}], 'mgCustomers': []}, 'contact': {'type': 'customer', 'id': 90, 'externalId': '50', 'isContact': False, 'createdAt': '2026-04-15 21:43:09', 'vip': False, 'bad': False, 'site': 'ijoni', 'contragent': {'contragentType': 'individual'}, 'tags': [], 'customFields': [], 'personalDiscount': 0, 'marginSumm': 0, 'totalSumm': 0, 'averageSumm': 0, 'ordersCount': 0, 'segments': [], 'firstName': 'Феруза', 'lastName': 'Юсупова', 'presumableSex': 'female', 'email': 'feruza.yusupova@example.com', 'customerSubscriptions': [{'subscription': {'id': 13, 'channel': 'email', 'name': 'Без тематики', 'code': 'default_marketing', 'active': True, 'autoSubscribe': True, 'ordering': 1}, 'subscribed': True}, {'subscription': {'id': 15, 'channel': 'waba', 'name': 'Без тематики', 'code': 'default_marketing', 'active': True, 'autoSubscribe': True, 'ordering': 1}, 'subscribed': True}], 'phones': [{'number': '+77090123450'}], 'mgCustomers': []}, 'contragent': {'contragentType': 'individual'}, 'delivery': {'cost': 0, 'netCost': 0, 'address': {'countryIso': 'KZ', 'text': 'Алматы, ул. Мухамедханова 8, кв 73'}}, 'site': 'ijoni', 'status': 'offer-analog', 'items': [{'bonusesChargeTotal': 0, 'bonusesCreditTotal': 0, 'markingObjects': [], 'id': 243, 'initialPrice': 28000, 'discounts': [], 'discountTotal': 0, 'prices': [{'price': 28000, 'quantity': 1}], 'createdAt': '2026-04-15 21:43:09', 'quantity': 1, 'status': 'new', 'offer': {'displayName': 'Утягивающий комбидресс Nova Slim', 'id': 77, 'xmlId': 'cbc58b7e-0ac8-4072-ad24-73ad8833fa07', 'name': 'Утягивающий комбидресс Nova Slim', 'quantity': 0, 'unit': {'code': 'pc', 'name': 'Штука', 'sym': 'шт.'}}, 'properties': [], 'purchasePrice': 0, 'ordering': 0}, {'bonusesChargeTotal': 0, 'bonusesCreditTotal': 0, 'markingObjects': [], 'id': 244, 'initialPrice': 35000, 'discounts': [], 'discountTotal': 0, 'prices': [{'price': 35000, 'quantity': 1}], 'createdAt': '2026-04-15 21:43:09', 'quantity': 1, 'status': 'new', 'offer': {'displayName': 'Утягивающее боди Nova Body', 'id': 81, 'xmlId': '60b2b1cb-df06-4608-be49-bfd8f6f952ac', 'name': 'Утягивающее боди Nova Body', 'quantity': 0, 'unit': {'code': 'pc', 'name': 'Штука', 'sym': 'шт.'}}, 'properties': [], 'purchasePrice': 0, 'ordering': 0}, {'bonusesChargeTotal': 0, 'bonusesCreditTotal': 0, 'markingObjects': [], 'id': 245, 'initialPrice': 18000, 'discounts': [], 'discountTotal': 0, 'prices': [{'price': 18000, 'quantity': 1}], 'createdAt': '2026-04-15 21:43:09', 'quantity': 1, 'status': 'new', 'offer': {'displayName': 'Утягивающие леггинсы Nova Fit', 'id': 80, 'xmlId': '65523082-fdc9-4adb-86b2-45af5bc78459', 'name': 'Утягивающие леггинсы Nova Fit', 'quantity': 0, 'unit': {'code': 'pc', 'name': 'Штука', 'sym': 'шт.'}}, 'properties': [], 'purchasePrice': 0, 'ordering': 0}], 'payments': {}, 'fromApi': False, 'shipped': False, 'customFields': [], 'currency': 'RUB'}

теперь нужно написать скрипт для того, чтобы положить это в базу данных supabase.
Вот наша таблица
create table orders (
    id bigserial primary key,

    last_name text,
    first_name text not null,
    middle_name text,

    phone text,
    email text,
    email_subscription boolean,

    external_customer_id text,

    country text not null default 'Казахстан',
    order_date date,

    order_number text,
    external_order_id text,

    status text,
    order_type text not null,

    product_name text,
    quantity integer,
    price numeric,

    delivery_type text,
    delivery_address text,

    payment_type text,
    payment_status text,

    comment text,
    paid_at timestamp
);

соотнеси корректно поля из возвращаемых от апи с поляи в нашей таблице, все не нужные не пиши
</details> <details> <summary>Supabase маппинг</summary>
теперь нужно написать скрипт для того, чтобы положить это в базу данных supabase. Вот наша таблица create table orders ( id bigserial primary key, last_name text, first_name text not null, middle_name text, phone text, email text, email_subscription boolean, external_customer_id text, country text not null default 'Казахстан', order_date date, order_number text, external_order_id text, status text, order_type text not null, product_name text, quantity integer, price numeric, delivery_type text, delivery_address text, payment_type text, payment_status text, comment text, paid_at timestamp ); соотнеси корректно поля из возвращаемых от апи с поляи в нашей таблице, все не нужные не пиши
</details> <details> <summary>UI/Дашборд</summary>
I need a stylish dashboard for managing graphic design orders, powered by Supabase. The site must be fully responsive—optimized for both desktop and mobile devices—and feature animated charts that allow for interactive manipulation (such as rotation and similar interactions), adhering to modern UX design principles. You may include several different types of charts; just be sure to label them clearly. The dashboard should incorporate small, thematic images, but the overall aesthetic should remain minimalist and stylish, featuring elegant animations and ensuring rapid load times. Supabase Columns you can see in data.json Please note that the table contains individual items, which are grouped by external_order_id. This means that there may be multiple rows sharing the same external_order_id; essentially, this represents a single order containing multiple items, and therefore, these rows must be grouped together to form a single consolidated order. Site on russian language
</details>

Сложностей в процессе не возникло. Дополнительных комментариев нет. Спасибо за внимание.
