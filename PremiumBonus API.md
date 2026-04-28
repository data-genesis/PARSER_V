```
PB API (231012-1)
```
E-mail: info@premiumbonus.ru
Change log
10.10.2023 - Добавлен метод buyer-invite-code - получение кода приглашения MLM
10.10.2023 - В метод buyer-register добавлен аргумент referral_code
08.02.2024 - В метод purchase-info добавлен аргумент status . Актуализирован метод
purchase-info
07.05.2024 - Добавлен метод buyer-info-messages для получения списка сообщений
пользователей
09.07.2024 - В методе buyer-info добавлен параметр extra_fields
20.03.2025 - В методе buyer-register добавлен параметр promocode
04.06.2025 - Добавлена возможность использования email пользователя в качестве
идентификатора в некоторых запросах
10.06.2025 - Добавлен метод card-get-info
19.01.2026 - В методе buyer-register добавлен параметр ident_by_type
28.01.2026 - Дополнен метод purchase-list . Добавлен метод promocode/activate-
promocode . Дополнен метод buyer-info . Дополнен метод purchase-request . Дополнен
метод purchase-dry-run
17.03.2026 - В методе purchase-dry-run добавлен параметр items.write_on_bonus по
требованию
Покупатель
Методы работы с данными о покупателе
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
1 of 81 4/27/26, 9:23 PM
buyer-register
Регистрация покупателя
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Регистрация покупателя, требуется указать значение хотя бы для одного из полей: phone,
external_id или email.
```
string (Телефонный номер) ^7\d{10}$
```
```
string (Код пригласившего (MLM))
```
```
string (Номер физической карты покупателя)
```
```
string (Фамилия покупателя)
```
```
string (Имя покупателя)
```
```
string (Отчество покупателя)
```
```
string (Дата рождения покупателя) ([0-9]{4})-(?:
```
```
[0-9]{2})-([0-9]{2})
```
```
string (Пол покупателя)
```
```
Enum: "male" "female"
```
```
string (Электронная почта покупателя)
```
```
string (Дата рождения первого ребенка покупателя)
```
```
([0-9]{4})-(?:[0-9]{2})-([0-9]{2})
```
```
string (Имя первого ребенка покупателя)
```
```
string (Пол первого ребенка покупателя)
```
```
Enum: "male" "female"
```
```
string (Дата рождения второго ребенка покупателя)
```
```
([0-9]{4})-(?:[0-9]{2})-([0-9]{2})
```
phone
required
referral_code
card_number
surname
name
middle_name
birth_date
gender
email
child1_birth_date
child1_name
child1_gender
child2_birth_date
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
2 of 81 4/27/26, 9:23 PM
```
string (Имя второго ребенка покупателя)
```
```
string (Пол второго ребенка покупателя)
```
```
Enum: "male" "female"
```
```
string (Дата рождения третьего ребенка покупателя)
```
```
([0-9]{4})-(?:[0-9]{2})-([0-9]{2})
```
```
string (Имя третьего ребенка покупателя)
```
```
string (Пол третьего ребенка покупателя)
```
```
Enum: "male" "female"
```
```
string (Дата рождения четвертого ребенка
```
```
покупателя) ([0-9]{4})-(?:[0-9]{2})-([0-9]{2})
```
```
string (Имя четвертого ребенка покупателя)
```
```
string (Пол четвертого ребенка покупателя)
```
```
Enum: "male" "female"
```
```
string (Канал регистрации)
```
```
string (Точка регистрации)
```
```
string <uuid> (ID группы покупателя)
```
```
string (ID города, можно получить из метода city-list)
```
```
boolean (Верифицирован ли номер телефона кодом
```
```
из SMS)
```
```
boolean (Разрешение получения акций и рекламных
```
```
уведомлений)
```
```
boolean (Разрешение получения электронных писем)
```
```
boolean (Разрешение получения электронных чеков)
```
```
number <double> (Количество покупок до
```
```
регистрации в PremiumBonus)
```
```
number <double> (Сумма оплат до регистрации в
```
```
PremiumBonus)
```
child2_name
child2_gender
child3_birth_date
child3_name
child3_gender
child4_birth_date
child4_name
child4_gender
registration_channel
registration_point
group_id
city_id
phone_checked
is_refused_receive_messages
is_refused_receive_emails
is_agreed_receive_electronic_receipt
init_purchase_count
init_payment_amount
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
3 of 81 4/27/26, 9:23 PM
```
string (Имя кассира)
```
```
string (ID покупателя во внешней системе)
```
```
string (Промокод)
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
cashier_name
external_id
promocode
POST /buyer-register
application/json
"phone": "79251234567"
"referral_code": "111222333"
"card_number": "123456"
"surname": "Иванов"
"name": "Иван"
"middle_name": "Иванович"
"birth_date": "2000-05-06"
"gender": "male"
"email": "buyer@mail.ru"
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
4 of 81 4/27/26, 9:23 PM
Response samples
200 400 429 500
"child1_birth_date": "2000-05-06"
"child1_name": "Иван"
"child1_gender": "male"
"child2_birth_date": "2000-05-06"
"child2_name": "Иван"
"child2_gender": "male"
"child3_birth_date": "2000-05-06"
"child3_name": "Иван"
"child3_gender": "male"
"child4_birth_date": "2000-05-06"
"child4_name": "Иван"
"child4_gender": "male"
"registration_channel": "Касса"
"registration_point": "Точка 1"
"group_id": "3f04c71b-fbd7-4310-a84b-6fd34f0bd8ff"
"city_id": "152ed6ac-8bd4-b7aa-88ff-33571ba99c2a"
"phone_checked": true
"is_refused_receive_messages": false
"is_refused_receive_emails": false
"is_agreed_receive_electronic_receipt": false
"init_purchase_count": 10
"init_payment_amount": 1000
"cashier_name": "Алексеев Алексей"
"external_id": "1234567"
"promocode": "promocode"
application/json
"success": true
"is_register": true
"blocked": false
"phone": "79251234567"
"card_number": "123456"
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
5 of 81 4/27/26, 9:23 PM
"surname": "Иванов"
"name": "Иван"
"middle_name": "Иванович"
"birth_date": "2000-05-06"
"gender": "male"
"email": "buyer@mail.ru"
"child1_birth_date": "2000-05-06"
"child1_name": "Иван"
"child1_gender": "male"
"child2_birth_date": "2000-05-06"
"child2_name": "Иван"
"child2_gender": "male"
"child3_birth_date": "2000-05-06"
"child3_name": "Иван"
"child3_gender": "male"
"child4_birth_date": "2000-05-06"
"child4_name": "Иван"
"child4_gender": "male"
"group_id": "3f04c71b-fbd7-4310-a84b-6fd34f0bd8ff"
"city":-
"id": "152ed6ac-8bd4-b7aa-88ff-33571ba99c2a"
"name": "Москва"
"group_name": "Стандартная группа 10%"
"balance": 1000.25
"balance_bonus_accumulated": 100
"balance_bonus_present": 100
"balance_bonus_action": 100
"bonus_inactive": 420.65
"bonus_next_activation_text": "30.45 бон. через 3 дней 5 часов"
"phone_checked": true
"is_refused_receive_messages": false
"is_refused_receive_emails": false
"is_agreed_receive_electronic_receipt": false
"additional_info": ""
"init_purchase_count": 10
"init_payment_amount": 1000
"external_id": "1234567"
"write_off_confirmation_required": true
"ident_by_type": "phone"
"logger": "Aa1aA1aa"
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
6 of 81 4/27/26, 9:23 PM
buyer-info
Информация о покупателе
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
```
Запрос может быть выполнен по идентификатору покупателя(identiYcator), client_id (identiYcator)
```
```
или по ID покупателя из внешней системы(external_id), присвоить external_id можно только при
```
```
регистрации)
```
```
string (Может принимать номер телефона, email, номер физической или
```
```
электронной карты, код заказа из SMS или МП)
```
```
string (ID покупателя во внешней системе)
```
```
string <uuid> (ID точки продаж(не обязательно, если используется токен с
```
```
привязанной точкой продаж)
```
Array of strings
Дополнительные поля
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
identificator
required
external_id
sale_point_id
extra_fields
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
7 of 81 4/27/26, 9:23 PM
Request samples
Payload
Response samples
200 400 429 500
POST /buyer-info
application/json
"identificator": "79251234567"
"external_id": "1234567"
"sale_point_id": "02c7b11f-4924-4719-9325-39fbdcd49be4"
"extra_fields":-
"payments_amount"
application/json
"success": true
"is_registered": true
"blocked": false
"client_id": "123456789"
"phone": "79251234567"
"card_number": "123456"
"surname": "Иванов"
"name": "Иван"
"middle_name": "Иванович"
"birth_date": "2000-05-06"
"gender": "male"
"email": "buyer@mail.ru"
"child1_birth_date": "2000-05-06"
Content type
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
8 of 81 4/27/26, 9:23 PM
"child1_name": "Иван"
"child1_gender": "male"
"child2_birth_date": "2000-05-06"
"child2_name": "Иван"
"child2_gender": "male"
"child3_birth_date": "2000-05-06"
"child3_name": "Иван"
"child3_gender": "male"
"child4_birth_date": "2000-05-06"
"child4_name": "Иван"
"child4_gender": "male"
"group_id": "3f04c71b-fbd7-4310-a84b-6fd34f0bd8ff"
"city":-
"id": "152ed6ac-8bd4-b7aa-88ff-33571ba99c2a"
"name": "Москва"
"group_name": "Стандартная группа 10%"
"balance": 1000.25
"balance_bonus_accumulated": 100
"balance_bonus_present": 100
"balance_bonus_action": 100
"bonus_inactive": 420.65
"bonus_next_activation_text": "30.45 бон. через 3 дней 5 часов"
"phone_checked": true
"is_refused_receive_messages": false
"is_refused_receive_emails": false
"is_agreed_receive_electronic_receipt": false
"additional_info": ""
"init_purchase_count": 10
"init_payment_amount": 1000
"external_id": "1234567"
"identificator_type": "phone"
"registration_confirmation_required": true
"is_allowed_change_card": false
"write_off_confirmation_required": true
"payments_amount": 1000
"logger": "Aa1aA1aa"
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
9 of 81 4/27/26, 9:23 PM
buyer-info-detail
Подробная информация о покупателе
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Подробная информация о покупателе
```
string (Может принимать номер телефона, email, номер физической или
```
```
электронной карты, код заказа из SMS или МП)
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
identificator
required
POST /buyer-info-detail
application/json
"identificator": "79251234567"
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
10 of 81 4/27/26, 9:23 PM
Response samples
200 400 429 500
application/json
"success": true
"identificator_type": "phone"
"is_registered": true
"blocked": false
"phone": "79251234567"
"surname": "Иванов"
"name": "Иван"
"middle_name": "Иванович"
"birth_date": "2000-05-06"
"gender": "male"
"email": "buyer@mail.ru"
"group_id": "3f04c71b-fbd7-4310-a84b-6fd34f0bd8ff"
"city":-
"id": "152ed6ac-8bd4-b7aa-88ff-33571ba99c2a"
"name": "Москва"
"group_name": "Стандартная группа 10%"
"balance": 1000.25
"balance_bonus_accumulated": 100
"balance_bonus_present": 100
"balance_bonus_action": 100
"balance_deposit": 100
"can_present_bonus_amount": 100
"registration_date": "2000-01-01T12:00:00+00:00"
"last_purchase_date": "2000-01-01T12:00:00+00:00"
"is_refused_receive_messages": false
"purchases":-
…+
"mlm_referrer": "79251234567"
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
11 of 81 4/27/26, 9:23 PM
"mlm_referrals":-
…+
"transactions":-
…+
"cards":-
…+
"logger": "Aa1aA1aa"
buyer-info-messages
Список сообщений покупателя
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Список сообщений покупателя
```
string (Может принимать номер телефона, email, номер физической или
```
```
электронной карты, код заказа из SMS или МП)
```
```
string (ID покупателя во внешней системе)
```
```
Array of strings (Тип сообщения)
```
Items Enum: "sms" "push" "viber" "email" "wallet"
```
Array of integers (Статус сообщения: * 200 - Отправлено * 300 - Доставлено *
```
```
400 - Не доставлено * 500 - Отклонено )
```
Items Enum: 200 300 400 500
```
Array of integers (Источник сообщения * 1 - Ручные рассылки * 2 - Триггерные
```
```
сообщения (по программе) * 5 - Коды подтверждения Примечание: *Коды
```
подтверждения выводятся при установленном разрешении `Подробная
```
информация о покупателе - Список сообщений - Коды подтверждения`* )
```
Items Enum: 1 2 5
identificator
required
external_id
type
status
source
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
12 of 81 4/27/26, 9:23 PM
```
string <Y-m-dTH:i:sZ> (Период отправки (от))
```
```
string <Y-m-dTH:i:sZ> (Период отправки (до))
```
```
integer (Лимит сообщений) <= 100
```
```
Default: 10
```
```
integer (Смещение по списку сообщений (для пагинации))
```
```
Default: 0
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
period_from
period_to
limit
offset
POST /buyer-info-messages
application/json
"identificator": "79251234567"
"external_id": "1234567"
"type":-
"sms"
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
13 of 81 4/27/26, 9:23 PM
Response samples
200 400 429 500
"status":-
300
"source":-
1
"period_from": "2024-05-07T10:20:30Z"
"period_to": "2024-05-07T23:10:00Z"
"limit": 20
"offset": 10
application/json
"success": true
"totalCount": 100
"rows":-
…+
buyer-invite-code
Получение кода приглашения в MLM
```
AUTHORIZATIONS:ApiToken
```
HEADER PARAMETERS
any
```
Example: application/json
```
Content-Type
required
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
14 of 81 4/27/26, 9:23 PM
REQUEST BODY SCHEMA: application/json
```
Запрос может быть выполнен по идентификатору покупателя (identiYcator)
```
```
string (Может принимать номер телефона, email, номер физической или
```
```
электронной карты, код заказа из SMS или МП)
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
Response samples
200 400 429 500
identificator
required
POST /buyer-invite-code
application/json
"identificator": "79251234567"
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
15 of 81 4/27/26, 9:23 PM
application/json
"success": true
"amount_referrals": 8
"referral_code": "ooqv50"
"is_new": false
"logger": "Aa1aA1aa"
buyer-edit
Редактирование покупателя
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Редактирование покупателя, требуется указать значение хотя бы для одного из полей: phone,
external_id или email.
```
string (Телефонный номер) ^7\d{10}$
```
```
string (ID покупателя во внешней системе)
```
```
string (Номер физической карты покупателя)
```
```
string (Фамилия покупателя)
```
```
string (Имя покупателя)
```
```
string (Отчество покупателя)
```
```
string (Дата рождения покупателя) ([0-9]{4})-(?:
```
```
[0-9]{2})-([0-9]{2})
```
phone
required
external_id
card_number
surname
name
middle_name
birth_date
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
16 of 81 4/27/26, 9:23 PM
```
string (Пол покупателя)
```
```
Enum: "male" "female"
```
```
string (Электронная почта покупателя)
```
```
string (Дата рождения первого ребенка покупателя)
```
```
([0-9]{4})-(?:[0-9]{2})-([0-9]{2})
```
```
string (Имя первого ребенка покупателя)
```
```
string (Пол первого ребенка покупателя)
```
```
Enum: "male" "female"
```
```
string (Дата рождения второго ребенка покупателя)
```
```
([0-9]{4})-(?:[0-9]{2})-([0-9]{2})
```
```
string (Имя второго ребенка покупателя)
```
```
string (Пол второго ребенка покупателя)
```
```
Enum: "male" "female"
```
```
string (Дата рождения третьего ребенка покупателя)
```
```
([0-9]{4})-(?:[0-9]{2})-([0-9]{2})
```
```
string (Имя третьего ребенка покупателя)
```
```
string (Пол третьего ребенка покупателя)
```
```
Enum: "male" "female"
```
```
string (Дата рождения четвертого ребенка
```
```
покупателя) ([0-9]{4})-(?:[0-9]{2})-([0-9]{2})
```
```
string (Имя четвертого ребенка покупателя)
```
```
string (Пол четвертого ребенка покупателя)
```
```
Enum: "male" "female"
```
```
string <uuid> (ID группы покупателя)
```
```
string (ID Города (Можно указать только если он не
```
```
был указан при регистрации))
```
```
boolean (Верифицирован ли номер телефона кодом
```
```
из SMS)
```
gender
email
child1_birth_date
child1_name
child1_gender
child2_birth_date
child2_name
child2_gender
child3_birth_date
child3_name
child3_gender
child4_birth_date
child4_name
child4_gender
group_id
city_id
phone_checked
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
17 of 81 4/27/26, 9:23 PM
```
boolean (Разрешение получения акций и рекламных
```
```
уведомлений)
```
```
boolean (Разрешение получения электронных писем)
```
```
boolean (Разрешение получения электронных чеков)
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
is_refused_receive_messages
is_refused_receive_emails
is_agreed_receive_electronic_receipt
POST /buyer-edit
application/json
"phone": "79251234567"
"external_id": "1234567"
"card_number": "123456"
"surname": "Иванов"
"name": "Иван"
"middle_name": "Иванович"
"birth_date": "2000-05-06"
"gender": "male"
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
18 of 81 4/27/26, 9:23 PM
Response samples
200 400 429 500
"email": "buyer@mail.ru"
"child1_birth_date": "2000-05-06"
"child1_name": "Иван"
"child1_gender": "male"
"child2_birth_date": "2000-05-06"
"child2_name": "Иван"
"child2_gender": "male"
"child3_birth_date": "2000-05-06"
"child3_name": "Иван"
"child3_gender": "male"
"child4_birth_date": "2000-05-06"
"child4_name": "Иван"
"child4_gender": "male"
"group_id": "3f04c71b-fbd7-4310-a84b-6fd34f0bd8ff"
"city_id": "152ed6ac-8bd4-b7aa-88ff-33571ba99c2a"
"phone_checked": true
"is_refused_receive_messages": false
"is_refused_receive_emails": false
"is_agreed_receive_electronic_receipt": false
application/json
"success": true
"is_register": true
"blocked": false
"phone": "79251234567"
"card_number": "123456"
"surname": "Иванов"
"name": "Иван"
"middle_name": "Иванович"
"birth_date": "2000-05-06"
"gender": "male"
"email": "buyer@mail.ru"
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
19 of 81 4/27/26, 9:23 PM
"child1_birth_date": "2000-05-06"
"child1_name": "Иван"
"child1_gender": "male"
"child2_birth_date": "2000-05-06"
"child2_name": "Иван"
"child2_gender": "male"
"child3_birth_date": "2000-05-06"
"child3_name": "Иван"
"child3_gender": "male"
"child4_birth_date": "2000-05-06"
"child4_name": "Иван"
"child4_gender": "male"
"group_id": "3f04c71b-fbd7-4310-a84b-6fd34f0bd8ff"
"group_name": "Стандартная группа 10%"
"balance": 1000.25
"balance_bonus_accumulated": 100
"balance_bonus_present": 100
"balance_bonus_action": 100
"bonus_inactive": 420.65
"bonus_next_activation_text": "30.45 бон. через 3 дней 5 часов"
"phone_checked": true
"is_refused_receive_messages": false
"is_refused_receive_emails": false
"is_agreed_receive_electronic_receipt": false
"additional_info": ""
"init_purchase_count": 10
"init_payment_amount": 1000
"cashier_name": "Алексеев Алексей"
"external_id": "1234567"
"city":-
"id": "152ed6ac-8bd4-b7aa-88ff-33571ba99c2a"
"name": "Москва"
"bonus_reserved": 100
"logger": "Aa1aA1aa"
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
20 of 81 4/27/26, 9:23 PM
buyer/status-transition-info
Информация о динамическом статусе покупателя
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Информация о динамическом статусе покупателя
```
string (Телефонный номер) ^7\d{10}$
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
phone
required
POST /buyer/status-transition-info
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
21 of 81 4/27/26, 9:23 PM
Response samples
200 400 429 500
application/json
"phone": "79251234567"
application/json
"client_group_transitions_leftover":-
…+
"transition_up":-
…+
"transition_down":-
…+
"client_group_transitions_list":-
…+
buyer/purchase-list
Детальная информация о покупках гостя
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Content type
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
22 of 81 4/27/26, 9:23 PM
Детальная информация о покупках гостя
```
string (Телефонный номер) ^7\d{10}$
```
Responses
200 OK
— 400
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
Response samples
200 429 500
phone
required
POST /buyer/purchase-list
application/json
"phone": "79251234567"
application/json
Content type
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
23 of 81 4/27/26, 9:23 PM
"success": true
"list":-
…+
"logger": "AbCDef"
generate-order-code
Генерация кода покупателя
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Требуется указать значение phone или email.
```
string (Телефонный номер) ^7\d{10}$
```
```
string (Электронная почта покупателя)
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
phone
required
email
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
24 of 81 4/27/26, 9:23 PM
Request samples
Payload
Response samples
200 400 429 500
POST /generate-order-code
application/json
"phone": "79251234567"
"email": "buyer@mail.ru"
application/json
"success": true
"order_code": "123456"
"logger": "Aa1aA1aa"
card-activate
Активация карты
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Активация карты
Content type
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
25 of 81 4/27/26, 9:23 PM
```
string (Телефонный номер) ^7\d{10}$
```
```
string (Номер карты, которую нужно активировать)
```
```
string (ID точки продаж (необязательно))
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
Response samples
200 400 429 500
phone
card_number
sale_point_id
POST /card-activate
application/json
"phone": "79251234567"
"card_number": "1234567"
"sale_point_id": "3f04c71b-fbd7-4310-a84b-6fd34f0bd8ff"
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
26 of 81 4/27/26, 9:23 PM
application/json
"success": true
"logger": "Aa1aA1aa"
card-get-info
Получение электронной карты покупателя
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Получение электронной карты покупателя
```
string (Телефонный номер) ^7\d{10}$
```
```
string (ID дизайна электронной карты (уточняется у тех.поддержки))
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
403 Access Forbidden
```
500 Internal Server Error (ошибка на стороне API)
```
phone
required
design_id
required
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
27 of 81 4/27/26, 9:23 PM
Request samples
Payload
Response samples
200 400 403 500
POST /card-get-info
application/json
"phone": "79001234567"
"design_id": "eb7d4dce-6c40-4f85-8875-974ae2b836f2"
application/json
"success": true
"result":-
"phone": "79001234567"
"gpay_link": null
"gpay_jwt": null
"wallet_link": "https://cards.premiumbonus.su/api/cards/get-wallet?did=3458dkga-9915
"applications": …+
"logger": "Aa1aA1aa"
buyer-bonus
Content type
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
28 of 81 4/27/26, 9:23 PM
Бонусные пакеты покупателя
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Бонусные пакеты покупателя
```
string (Телефонный номер) ^7\d{10}$
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
Response samples
phone
required
POST /buyer-bonus
application/json
"phone": "79251234567"
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
29 of 81 4/27/26, 9:23 PM
200 400 429 500
application/json
"success": true
"data":-
…+
"logger": "Aa1aA1aa"
buyer-groups
Получение списка групп пользователей
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Отправка кода подтверждения регистрации
```
string (ID точки продаж)
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
sale_point_id
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
30 of 81 4/27/26, 9:23 PM
Request samples
Payload
Response samples
200 400 429 500
POST /buyer-groups
application/json
"sale_point_id": "3f04c71b-fbd7-4310-a84b-6fd34f0bd8ff"
application/json
"success": true
"list":-
…+
present-bonus
Подарить бонусы другу
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Content type
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
31 of 81 4/27/26, 9:23 PM
Редактирование покупателя
```
string (Телефонный номер покупателя) ^7\d{10}$
```
```
string (Телефонный номер друга, которому дарим бонусы) ^7\d{10}$
```
```
number <double> (Сколько бонусов дарить)
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
Response samples
phone
target_phone
bonus_amount
POST /present-bonus
application/json
"phone": "79251234567"
"target_phone": "79251234567"
"bonus_amount": 100
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
32 of 81 4/27/26, 9:23 PM
Покупка
Методы работы с покупками
200 400 429 500
application/json
"success": true
"logger": "Aa1aA1aa"
write-off-request
```
Получение максимальной доступной выгоды(скидки+бонусы)
```
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
```
Получение максимальной доступной выгоды(скидки+бонусы)
```
```
string (Телефонный номер) ^7\d{10}$
```
```
string <uuid> (ID точки продаж (не обязательно, если используется токен с
```
```
привязанной точкой продаж))
```
```
string (Промокод, применённый в заказе)
```
```
string (ID точки продаж (не обязательно, если используется токен с
```
```
привязанной точкой продаж))
```
phone
required
sale_point_id
promocode
sale_point
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
33 of 81 4/27/26, 9:23 PM
```
string (Канал продаж (не обязателен))
```
```
number <double> (Сумма внешней скидки на чек)
```
```
Array of objects (Items)
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
sale_channel
discount
items
required
POST /write-off-request
application/json
"phone": "79251234567"
"sale_point_id": "3f04c71b-fbd7-4310-a84b-6fd34f0bd8ff"
"promocode": "Pizza"
"sale_point": "Точка1"
"sale_channel": "Наличные"
"discount": 100
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
34 of 81 4/27/26, 9:23 PM
Response samples
200 400 429 500
"items":-
…+
application/json
"balance": 1000.25
"write_off_available": 100.5
"total_discount_external": 400.1
"total_discount_premiumbonus": 400.1
"items":-
…+
"print_on_precheck": "Можно списать 100 бон."
"logger": "Aa1aA1aa"
purchase-dry-run
Эмуляция проведения покупки
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Эмуляция проведения покупки
```
string (Телефонный номер) ^7\d{10}$phonerequired
```
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
35 of 81 4/27/26, 9:23 PM
```
string <uuid> (ID точки продаж(не обязательно, если используется токен с
```
```
привязанной точкой продаж))
```
```
string (ID точки продаж (не обязательно, если используется токен с
```
```
привязанной точкой продаж))
```
```
string (Канал продаж (не обязателен))
```
```
string (Промокод, применённый в заказе)
```
```
string (ID покупки во внешней системе)
```
```
string (Имя кассира)
```
```
Array of strings (Фамилия Имя официанта)
```
```
number <double> (Сумма внешней скидки на чек(воспринимается как
```
```
дополнение к скидкам переданным в элементах покупки)
```
```
number <double> (Количество списываемых бонусов)
```
```
number <double> (Количество часов для резерва бонусов на покупку)
```
```
number <double> (Сумма к оплате банковской картой привязанной к
```
```
PremiumBonus из приложения разработанного PremiumBonus)
```
```
Array of objects (Items)
```
Array of strings
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
sale_point_id
sale_point
sale_channel
promocode
external_purchase_id
cashier_name
waiters_names
discount
write_off_bonus
reserve_hours
card_payment_amount
items
required
include
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
36 of 81 4/27/26, 9:23 PM
Request samples
Payload
Response samples
200 400 429 500
POST /purchase-dry-run
application/json
"phone": "79251234567"
"sale_point_id": "3f04c71b-fbd7-4310-a84b-6fd34f0bd8ff"
"sale_point": "Точка1"
"sale_channel": "Наличные"
"promocode": "Pizza"
"external_purchase_id": "1234567890"
"cashier_name": "Иван Иванов"
"waiters_names":-
"Иванов Иван",
"Официант 2"
"discount": 100
"write_off_bonus": 100
"reserve_hours": 2
"card_payment_amount": 5000
"items":-
…+
"include":-
"items_write_on_bonus"
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
37 of 81 4/27/26, 9:23 PM
application/json
"success": true
"external_purchase_id": "1234567890"
"purchase_amount": 5500
"payment_amount": 5300
"total_write_off_bonus": 100
"total_write_on_bonus": 215
"total_discount_external": 100
"total_discount_premiumbonus": 0
"balance": 900
"items":-
…+
"print_on_check": "Спасибо за покупку!"
"logger": "Aa1aA1aa"
purchase-request
```
информации о покупателе + максимальной доступной Получение >- выгоды(скидки+бонусы)
```
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
```
Получение информации о покупателе + максимальной доступной выгоды(скидки+бонусы)
```
```
string (Может принимать номер телефона, email, номер физической или
```
```
электронной карты, код заказа из SMS или МП)
```
```
string <uuid> (ID точки продаж(не обязательно, если используется токен с
```
```
привязанной точкой продаж))
```
```
string (ID точки продаж (не обязательно, если используется токен с
```
```
привязанной точкой продаж))
```
identificator
required
sale_point_id
sale_point
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
38 of 81 4/27/26, 9:23 PM
```
string (Промокод, применённый в заказе)
```
```
string (ID канала продаж)
```
```
number <double> (Сумма внешней скидки на чек)
```
```
Array of objects (Items)
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
promocode
sale_channel
discount
items
required
POST /purchase-request
application/json
"identificator": "79251234567"
"sale_point_id": "3f04c71b-fbd7-4310-a84b-6fd34f0bd8ff"
"sale_point": "Точка1"
"promocode": "Pizza"
"sale_channel": "mobile_app"
"discount": 100
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
39 of 81 4/27/26, 9:23 PM
Response samples
200 400 429 500
"items":-
…+
application/json
"success": true
"is_registered": true
"client_id": "123456789"
"blocked": false
"phone": "79251234567"
"card_number": "123456"
"surname": "Иванов"
"name": "Иван"
"middle_name": "Иванович"
"birth_date": "2000-05-06"
"gender": "male"
"email": "buyer@mail.ru"
"child1_birth_date": "2000-05-06"
"child1_name": "Иван"
"child1_gender": "male"
"child2_birth_date": "2000-05-06"
"child2_name": "Иван"
"child2_gender": "male"
"child3_birth_date": "2000-05-06"
"child3_name": "Иван"
"child3_gender": "male"
"child4_birth_date": "2000-05-06"
"child4_name": "Иван"
"child4_gender": "male"
"group_id": "3f04c71b-fbd7-4310-a84b-6fd34f0bd8ff"
"group_name": "Стандартная группа 10%"
"balance": 1000.25
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
40 of 81 4/27/26, 9:23 PM
"balance_bonus_accumulated": 100
"balance_bonus_present": 100
"balance_bonus_action": 100
"bonus_inactive": 420.65
"bonus_next_activation_text": "30.45 бон. через 3 дней 5 часов"
"phone_checked": true
"is_refused_receive_messages": false
"is_refused_receive_emails": false
"is_agreed_receive_electronic_receipt": false
"additional_info": ""
"init_purchase_count": 10
"init_payment_amount": 1000
"external_id": "1234567"
"identificator_type": "phone"
"registration_confirmation_required": true
"write_off_confirmation_required": true
"is_allowed_change_card": false
"write_off_available": 100.5
"card_payment_available": 3600
"total_discount_external": 400.1
"total_discount_premiumbonus": 400.1
"items":-
…+
"print_on_precheck": "Можно списать 100 бон."
"logger": "Aa1aA1aa"
purchase
Добавление покупки
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Добавление покупки
```
string (Телефонный номер) ^7\d{10}$phone
```
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
41 of 81 4/27/26, 9:23 PM
boolean
```
string (Может принимать номер телефона, email, номер физической или
```
```
электронной карты, код заказа из SMS или МП)
```
```
string <uuid> (ID точки продаж(не обязательно, если используется токен с
```
```
привязанной точкой продаж))
```
```
string (ID точки продаж (не обязательно, если используется токен с
```
```
привязанной точкой продаж))
```
```
string (Канал продаж (не обязателен))
```
```
string (Промокод, применённый в заказе)
```
```
string (ID покупки во внешней системе)
```
```
string (Имя кассира)
```
```
Array of strings (Фамилия Имя официанта)
```
```
number <double> (Сумма внешней скидки на чек(воспринимается как
```
```
дополнение к скидкам переданным в элементах покупки)
```
```
number <double> (Количество списываемых бонусов)
```
```
Array of objects (Items)
```
```
string (Статус покупки)
```
```
Enum: "approved" "not_approved"
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
offline
identificator
sale_point_id
sale_point
sale_channel
promocode
external_purchase_id
cashier_name
waiters_names
discount
write_off_bonus
items
required
purchase_status
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
42 of 81 4/27/26, 9:23 PM
Request samples
Payload
Response samples
200 400 429 500
POST /purchase
application/json
"phone": "79251234567"
"offline": true
"identificator": "79251234567"
"sale_point_id": "3f04c71b-fbd7-4310-a84b-6fd34f0bd8ff"
"sale_point": "Точка1"
"sale_channel": "Наличные"
"promocode": "Pizza"
"external_purchase_id": "1234567890"
"cashier_name": "Иван Иванов"
"waiters_names":-
"Иванов Иван",
"Официант 2"
"discount": 100
"write_off_bonus": 100
"items":-
…+
"purchase_status": "approved"
application/json
Content type
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
43 of 81 4/27/26, 9:23 PM
"success": true
"purchase_id": "3f04c71b-fbd7-4310-a84b-6fd34f0bd8ff"
"external_purchase_id": "1234567890"
"purchase_amount": 5500
"payment_amount": 5300
"total_write_off_bonus": 100
"total_write_on_bonus": 215
"total_discount_external": 100
"total_discount_premiumbonus": 0
"balance": 900
"items":-
…+
"print_on_check": "Спасибо за покупку!"
"purchase_status": "approved"
"logger": "Aa1aA1aa"
purchase-set-external-id
Добавление или изменение внешнего ID покупки
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Добавление или изменение внешнего ID покупки
```
string (ID покупки)
```
```
string (ID покупки во внешней системе)
```
Responses
purchase_id
external_purchase_id
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
44 of 81 4/27/26, 9:23 PM
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
Response samples
200 400 429 500
POST /purchase-set-external-id
application/json
"purchase_id": "e298e2a3-bf7f-6f35-3cec-958b8724d0f2"
"external_purchase_id": "111"
application/json
"success": true
"logger": "Aa1aA1aa"
Content type
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
45 of 81 4/27/26, 9:23 PM
edit-purchase
Редактирование покупки
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Редактирование покупки
```
string (ID покупки в PremiumBonus)
```
```
string (ID покупки во внешней системе)
```
```
number <double> (Сумма внешней скидки на чек)
```
```
number <double> (Количество списываемых бонусов)
```
```
number <double> (Сумма к оплате банковской картой привязанной к
```
```
PremiumBonus из приложения разработанного PremiumBonus)
```
```
string (Имя кассира)
```
```
Array of strings (Фамилия Имя официанта)
```
```
string (Статус покупки(не рекомендуется переводит из "not_approved" в
```
```
"approved")
```
```
Enum: "approved" "not_approved"
```
```
Array of objects (Items)
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
purchase_id
external_purchase_id
required
discount
write_off_bonus
card_payment_amount
cashier_name
waiters_names
purchase_status
items
required
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
46 of 81 4/27/26, 9:23 PM
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
Response samples
200 400 429 500
POST /edit-purchase
application/json
"purchase_id": "3f04c71b-fbd7-4310-a84b-6fd34f0bd8ff"
"external_purchase_id": "1234567890"
"discount": 100
"write_off_bonus": 100
"card_payment_amount": 5000
"cashier_name": "Иван Иванов"
"waiters_names":-
"Иванов Иван",
"Официант 2"
"purchase_status": "approved"
"items":-
…+
application/json
Content type
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
47 of 81 4/27/26, 9:23 PM
"success": true
"purchase_id": "3f04c71b-fbd7-4310-a84b-6fd34f0bd8ff"
"external_purchase_id": "1234567890"
"purchase_amount": 100.5
"payment_amount": 100.5
"total_write_off_bonus": 100.5
"total_write_on_bonus": 90.4
"balance": 1000.25
"items":-
…+
"total_discount_external": 400.1
"total_discount_premiumbonus": 400.1
"logger": "Aa1aA1aa"
cancel-purchase
Отмена покупки
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Отмена покупки
```
string (ID покупки в PremiumBonus)
```
```
string (ID покупки во внешней системе)
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
purchase_id
external_purchase_id
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
48 of 81 4/27/26, 9:23 PM
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
Response samples
200 400 429 500
POST /cancel-purchase
application/json
"purchase_id": "3f04c71b-fbd7-4310-a84b-6fd34f0bd8ff"
"external_purchase_id": "1234567890"
application/json
"success": true
"logger": "Aa1aA1aa"
change-purchase-status
Content type
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
49 of 81 4/27/26, 9:23 PM
Изменение статуса покупки
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Изменение статуса покупки
```
string (ID покупки в PremiumBonus)
```
```
string (ID покупки во внешней системе)
```
```
string (Статус покупки)
```
```
Enum: "approved" "not_approved"
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
purchase_id
external_purchase_id
purchase_status
POST /change-purchase-status
application/json
"purchase_id": "3f04c71b-fbd7-4310-a84b-6fd34f0bd8ff"
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
50 of 81 4/27/26, 9:23 PM
Response samples
200 400 429 500
"external_purchase_id": "1234567890"
"purchase_status": "approved"
application/json
"success": true
"logger": "Aa1aA1aa"
reserve-info
Информация по резерву
```
AUTHORIZATIONS:ApiToken
```
HEADER PARAMETERS
any
```
Example: application/json
```
REQUEST BODY SCHEMA: application/json
Информация по резерву
```
string (ID покупки во внешней системе)
```
Responses
Content-Type
required
external_purchase_id
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
51 of 81 4/27/26, 9:23 PM
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
52 of 81 4/27/26, 9:23 PM
Request samples
Payload
Response samples
200 400 429 500
POST /reserve-info
application/json
"external_purchase_id": "1234567890"
application/json
"success": true
"external_purchase_id": "1234567890"
"reserve_bonus": 100.5
"reserve_expire_at": "2015-01-01 12:00:00+00"
"logger": "Aa1aA1aa"
purchase-info
Информация о покупке
```
AUTHORIZATIONS:ApiToken
```
Content type
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
53 of 81 4/27/26, 9:23 PM
REQUEST BODY SCHEMA: application/json
Информация о покупке
```
string (ID покупки во внешней системе)
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
Response samples
200 400 429 500
external_purchase_id
POST /purchase-info
application/json
"external_purchase_id": "1234567890"
application/json
Content type
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
54 of 81 4/27/26, 9:23 PM
Коды подтверждения
Методы для кодов подтверждения
"success": true
"external_purchase_id": "2214451"
"status": "approved"
"buyer":-
"phone": "79251234567"
"surname": "Иванов"
"name": "Иван"
"middle_name": "Иванович"
"group_id": "3f04c71b-fbd7-4310-a84b-6fd34f0bd8ff"
"group_name": "Стандартная группа 10%"
"items":-
…+
"logger": "Aa1aA1aa"
send-register-code
Отправка кода подтверждения регистрации
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Отправка кода подтверждения регистрации
```
string (Телефонный номер) ^7\d{10}$phonerequired
```
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
55 of 81 4/27/26, 9:23 PM
Responses
200 OK
RESPONSE SCHEMA: application/json
```
boolean (Успешность операции)
```
```
string (ID запроса в системе логирования)
```
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
Response samples
200 400 429 500
success
logger
POST /send-register-code
application/json
"phone": "79251234567"
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
56 of 81 4/27/26, 9:23 PM
application/json
"success": true
"logger": "Aa1aA1aa"
send-write-off-confirmation-code
Отправка кода подтверждения списания
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Отправка кода подтверждения списания
```
string (Телефонный номер) ^7\d{10}$
```
```
number <double> (Сумма покупки)
```
```
number <double> (Количество бонусов для списания)
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
phone
required
purchase_amount
write_off_bonus
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
57 of 81 4/27/26, 9:23 PM
Request samples
Payload
Response samples
200 400 429 500
POST /send-write-off-confirmation-code
application/json
"phone": "79251234567"
"purchase_amount": 415.55
"write_off_bonus": 41
application/json
"success": true
"logger": "Aa1aA1aa"
verify-confirmation-code
Проверка кода подтверждения регистрации или списания
```
AUTHORIZATIONS:ApiToken
```
Content type
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
58 of 81 4/27/26, 9:23 PM
REQUEST BODY SCHEMA: application/json
Проверка кода подтверждения регистрации или списания
```
string (Телефонный номер) ^7\d{10}$
```
```
string (Код подтверждения)
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
Response samples
phone
required
code
POST /verify-confirmation-code
application/json
"phone": "79251234567"
"code": "123"
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
59 of 81 4/27/26, 9:23 PM
200 400 429 500
application/json
"success": true
"logger": "Aa1aA1aa"
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
60 of 81 4/27/26, 9:23 PM
send-custom-code
Отправка кастомного кода подтверждения
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Отправка кастомного кода подтверждения
```
string (Телефонный номер) ^7\d{10}$
```
```
string (Текст смс, в котором поддерживается переменная {{code}}, которая
```
```
будет заменена системой на генерируемый код)
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
phone
required
text
POST /send-custom-code
application/json
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
61 of 81 4/27/26, 9:23 PM
Response samples
200 400 429 500
"phone": "79251234567"
```
"text": "Код подтверждения: {{code}}"
```
application/json
"success": true
"logger": "Aa1aA1aa"
verify-custom-code
Проверка кастомного кода подтверждения
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Проверка кастомного кода подтверждения
```
string (Телефонный номер) ^7\d{10}$
```
```
string (Код подтверждения)
```
Responses
200 OK
phone
required
code
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
62 of 81 4/27/26, 9:23 PM
Мобильное PremiumBonus
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
Response samples
200 400 429 500
POST /verify-custom-code
application/json
"phone": "79251234567"
"code": "123"
application/json
"success": true
"logger": "Aa1aA1aa"
Content type
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
63 of 81 4/27/26, 9:23 PM
Методы работы с МП Premium Bonus
get-orders
Получение списка заказов
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Получение списка заказов
```
string (Может принимать номер телефона, email, номер физической или
```
```
электронной карты, код заказа из SMS или МП)
```
```
string (Дата начала периода)
```
```
string (Дата окончания периода)
```
```
string (Статус заказа, где: 1 - Не подтверждено / 2 - Подтверждено / 3 -
```
```
Удалено / 4 - Черновик)
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
identificator
period_from
period_to
status
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
64 of 81 4/27/26, 9:23 PM
Request samples
Payload
Response samples
200 400 429 500
POST /get-orders
application/json
"identificator": "79251234567"
"period_from": "2015-01-01 12:00:00+03"
"period_to": "2015-10-01 12:00:00+03"
"status": "1"
application/json
"success": true
"info":-
…+
"list":-
…+
change-order-status
Content type
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
65 of 81 4/27/26, 9:23 PM
Изменение внешнего статуса заказа
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Изменение внешнего статуса заказа
```
string (Номер заказа в МП)
```
```
string (Статус заказа)
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
order_code
external_status
POST /change-order-status
application/json
"order_code": "123456"
"external_status": "В пути"
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
66 of 81 4/27/26, 9:23 PM
Response samples
200 400 429 500
application/json
"success": true
"logger": "Aa1aA1aa"
send-push
Отправка PUSH уведомления гостю в Мобильное приложение
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Отправка PUSH уведомления гостю в Мобильное приложение
```
string (Телефонный номер)
```
```
string (Заголовок PUSH уведомления)
```
```
string (Текст PUSH уведомления)
```
```
string (Ссылка на картинку, которую необходимо добавить в PUSH (картинка
```
```
будет отображаться только в мобильном приложении))
```
Responses
200 OK
phone
required
title
message
image
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
67 of 81 4/27/26, 9:23 PM
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
Response samples
200 400 429 500
POST /send-push
application/json
"phone": "79251234567"
"title": "Заголовок"
"message": "Тестовый пуш"
"image": "https://i.ytimg.com/vi/ud0532926I/8kkb930avse.jpg"
application/json
"success": true
"logger": "Lf83Avk2"
Content type
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
68 of 81 4/27/26, 9:23 PM
Методы работы с подарочными сертификатами
info
Получение информации о сертификате
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Получение информации о сертификате
```
string (Номер сертификата)
```
```
Array of any (Показать массив транзакций в ответе)
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
barcode
show_transaction
POST /info
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
69 of 81 4/27/26, 9:23 PM
Payload
Response samples
200 400 429 500
application/json
"barcode": "9990009990080240091"
"show_transaction":-
"true"
application/json
"success": true
"status": 2
"status_name": "Карта заблокирована"
"balance": 0
"created_at": "2020-03-09 12:17:02+00"
"activated_at": "2019-12-30 10:23:00+00"
"last_operation_at": "2020-03-10 13:36:31+00"
"expire_at": "2020-03-10 13:36:31+00"
"nominal": 1000
"title": "Подарок 1000"
"transaction":-
…+
Content type
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
70 of 81 4/27/26, 9:23 PM
pin-check
Проверка PIN кода
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Проверка PIN кода
```
string (Номер сертификата)
```
```
string (Пин-код)
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
barcode
pincode
POST /pin-check
application/json
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
71 of 81 4/27/26, 9:23 PM
Response samples
200 400 429 500
"barcode": "9990009990080240091"
"pincode": "224"
application/json
"success": true
"logger": "Aa1aA1aa"
debit
```
Покупка по сертификату (списание)
```
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
```
Покупка по сертификату (списание)
```
```
string (Номер сертификата)
```
```
string (Пин-код)
```
```
number <double> (Сумма покупки по сертификату)
```
```
Array of any (Показать массив транзакций в ответе)
```
Responses
barcode
pincode
payment_amount
show_transaction
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
72 of 81 4/27/26, 9:23 PM
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
Response samples
200 400 429 500
POST /debit
application/json
"barcode": "9990009990080240091"
"pincode": "224"
"payment_amount": 100.5
"show_transaction":-
"true"
application/json
"success": true
Content type
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
73 of 81 4/27/26, 9:23 PM
"balance": 889.5
"payment_amount": 100.5
"activated_at": "2020-03-10 13:36:31+00"
"last_operation_at": "2020-03-10 13:36:31+00"
"expire_at": "2020-03-10 13:36:31+00"
"transaction":-
…+
active
```
Покупка сертификата (активация)
```
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
```
Покупка сертификата (активация)
```
```
string (Номер сертификата)
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
barcode
POST /active
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
74 of 81 4/27/26, 9:23 PM
Дополнительно
Дополнительные методы
Request samples
Payload
Response samples
200 400 429 500
application/json
"barcode": "9990009990080240091"
application/json
"success": true
"balance": 1000
"activated_at": "2020-03-10 13:36:31+00"
"last_operation_at": "2020-03-10 13:36:31+00"
"expire_at": "2020-03-10 13:36:31+00"
trigger
Content type
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
75 of 81 4/27/26, 9:23 PM
Активация триггера
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
```
Запуск действия настроенного в сценариях PremiumBonus для покупателя(когда требуется
```
срабатываие по событию не предусмотренного шаблонами PremiumBonus, примеры действий -
начисление бонусов/установка метки покупателя/отправка маркетингового сообщения
```
string (Телефонный номер) ^7\d{10}$
```
```
string (Электронная почта покупателя, если не указан телефон)
```
```
string (Название события)
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
phone
email
event_name
POST /trigger
application/json
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
76 of 81 4/27/26, 9:23 PM
Response samples
200 400 429 500
"phone": "79251234567"
"email": "buyer@mail.ru"
"event_name": "event1"
application/json
"success": true
"logger": "Aa1aA1aa"
cashbox-list
Получение списка точек продаж
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Получение списка точек продаж
```
string (Имя кассира)
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
cashier_name
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
77 of 81 4/27/26, 9:23 PM
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
Response samples
200 400 429 500
POST /cashbox-list
application/json
"cashier_name": "Иван Иванов"
application/json
"success": true
"list":-
…+
Content type
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
78 of 81 4/27/26, 9:23 PM
city-list
Получение информации о городах и их ID
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Запрос выполняется без "Body"
```
object (CityList)
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
Request samples
Payload
Response samples
POST /city-list
application/json
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
79 of 81 4/27/26, 9:23 PM
200 400 429 500
application/json
"id": "152ed6ac-8bd4-b7aa-88ff-33571ba99c2a"
"name": "Москва"
activate-promocode
Активация промокода для покупателя
```
AUTHORIZATIONS:ApiToken
```
REQUEST BODY SCHEMA: application/json
Активация промокода для покупателя
```
string (Номер телефона)
```
```
string (промокод)
```
Responses
200 OK
```
400 Bad Request (неверный формат запроса)
```
```
429 Too Many Requests (превышение лимита запросов)
```
```
500 Internal Server Error (ошибка на стороне API)
```
phone
code
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
80 of 81 4/27/26, 9:23 PM
Request samples
Payload
Response samples
200 400 429 500
POST /promocode/activate-promocode
application/json
"phone": 79001234567
"code": "промокод"
application/json
"success": true
"logger": "AbCDef"
Content type
Content type
PremiumBonus API https://doc.premiumbonus.ru/pb/#tag/Pokupatel
81 of 81 4/27/26, 9:23 PM