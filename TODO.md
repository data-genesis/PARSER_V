# TODO: Реализация бота PremiumBonus

- [x] Собрать требования и изучить API
- [x] Согласовать план и структуру с пользователем
- [x] Исправить `.gitignore` (пересоздать из `.gitnore`)
- [x] Создать `requirements.txt`
- [x] Создать `states.py` (FSM состояния)
- [x] Создать `utils/logger.py`
- [x] Создать `api_client.py` (обёртка над PremiumBonus API)
- [x] Исправить `keyboards.py` (Reply-кнопка для контакта)
- [x] Создать `handlers/__init__.py` и хендлеры:
  - [x] `start.py` — /start, согласие, запрос контакта, регистрация
  - [x] `cabinet.py` — Личный кабинет (/lk)
  - [x] `coupon.py` — Активация купона (/cop)
  - [x] `navigation.py` — Кнопки «Назад», /start, универсальные
- [x] Создать `middlewares/__init__.py` и `user_middleware.py`
- [x] Создать `bot.py` (точка входа)
- [x] Создать `.env.example`
- [x] Удалить старый `.gitnore`
- [x] Проверить целостность проекта
