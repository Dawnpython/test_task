# Тестовое задание WB—Tech

## Ссылки

- Дашборд: https://orders-dashboard-delta.vercel.app/
- Репозиторий: https://github.com/Dawnpython/test_task
- Telegram уведомления: /tg_notify

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

<details> <summary>Python: JSON → XLSX</summary>
PROMPT:
напиши python скрипт для добавления данных из json в xlsx таблицу...
</details> <details> <summary>RetailCRM API: получение заказов с пагинацией</summary>
PROMPT:
нужна функция, которая возвращает заказы, учти что может быть пагинация...
</details> <details> <summary>Пример ответа API</summary>
PROMPT:
вот пример ответа...
</details> <details> <summary>Supabase маппинг</summary>
PROMPT:
теперь нужно написать скрипт для того, чтобы положить это в базу данных supabase...
</details> <details> <summary>UI/Дашборд</summary>
PROMPT:
I need a stylish dashboard for managing graphic design orders...
</details>

Сложностей в процессе не возникло. Дополнительных комментариев нет. Спасибо за внимание.