# 🦋 Fluttershy Bot

> 🌸 Добрый и заботливый бот Флаттершай из Понивилля в Telegram

![Python Version](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Telegram-blue)
![AI](https://img.shields.io/badge/AI-OpenAI%20GPT--4--turbo-orange)

> **Статус:** ✅ **Активная разработка**
>
> 👨‍💻 *Автор: MADAO81*

---

## 📖 О проекте

Флаттершай — это интерактивный бот, который:

- 🦋 Общается мягко, нежно и с добротой
- 🐾 Даёт советы по уходу за питомцами
- 🕊️ Помогает успокоиться и обрести внутренний покой
- 📖 Рассказывает вдохновляющие истории о животных и доброте
- 💕 Дарит комплименты и ободрение
- 🌤️ Показывает погоду
- 🐾 Ежедневные рассказы о животных в 11:00
- 🌸 Ежедневное утреннее приветствие в 9:00
- ⏰ Работает в установленные часы (9:00–20:00)
- 💾 Хранит историю диалогов (30 дней) с возможностью очистки
- 🔒 Прозрачное уведомление о хранении данных и команда `/cleardata`

---

## 🛠️ Технологии

| Компонент | Технология |
|-----------|------------|
| Платформа | **Telegram** |
| ИИ-провайдер | **OpenAI GPT-4-turbo** |
| Распознавание голоса | **OpenAI Whisper** |
| Анализ изображений | **OpenAI Vision API** |
| Погода | **Open-Meteo** (бесплатно, без ключа) |
| База животных | **SQLite** (200+ животных) |
| Язык | Python 3.11+ |
| БД | SQLite |
| Деплой | SprintBox (systemd) |
| Мониторинг | Cron + watchdog (автоперезапуск) |

---

## 📋 Команды

| Команда | Описание |
|---------|----------|
| `/start` | Приветствие |
| `/help` | Справка |
| `/weather` | Погода |
| `/petcare` | Совет по уходу за питомцем 🐾 |
| `/calm` | Упражнение для спокойствия 🕊️ |
| `/story` | Вдохновляющая история 📖 |
| `/kindness` | Комплимент или ободрение 💕 |
| `/subscribe` | Подписаться на ежедневные рассказы о животных 🐾 |
| `/unsubscribe` | Отписаться от рассказов 😢 |
| `/cleardata` | Удалить историю диалога 🗑️ |

---

## 🚀 Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/MADAO81/Fluttershy_Bot_Telegram_Rus.git
cd Fluttershy_Bot_Telegram_Rus
```

### 2. Создайте виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Настройте переменные окружения

Скопируйте `.env.example` в `.env` и заполните:

```env
# Telegram
TELEGRAM_TOKEN=ваш_токен_бота

# OpenAI
OPENAI_API_KEY=ваш_ключ
OPENAI_MODEL=gpt-4-turbo

# Координаты Ворсино
DEFAULT_LAT=55.0965
DEFAULT_LON=36.6355

# Настройки
WORK_START_HOUR=9
WORK_END_HOUR=20
SAD_PROBABILITY=0.2
CONTEXT_EXPIRE_DAYS=30

# Администратор
ADMIN_ID=ваш_telegram_id

# Режим отладки
DEBUG_MODE=false
```

### 5. Создайте базу данных животных

```bash
python bot/scripts/create_animals_db.py
python bot/scripts/fill_animals_db.py
```

### 6. Запустите бота

```bash
python run.py
```

---

## 📁 Структура проекта

```text
Fluttershy_Bot_Telegram_Rus/
├── .env                      # Переменные окружения (НЕ ПУШИТЬ!)
├── .env.example              # Пример переменных окружения
├── .gitignore                # Git ignore
├── README.md                 # Описание проекта
├── requirements.txt          # Зависимости
├── run.py                    # Точка входа
│
├── bot/
│   ├── __init__.py
│   ├── config.py             # Конфигурация
│   ├── main.py               # Запуск
│   │
│   ├── core/                 # Ядро
│   │   ├── __init__.py
│   │   ├── constants.py      # Системный промпт
│   │   ├── mood_system.py    # Настроение
│   │   ├── context_manager.py # История
│   │   └── scheduler.py      # Расписание (9:00 и 11:00)
│   │
│   ├── handlers/             # Обработчики
│   │   ├── __init__.py
│   │   ├── commands.py       # Команды
│   │   ├── admin.py          # Админ-команды
│   │   ├── messages.py       # Текстовые сообщения
│   │   ├── photos.py         # Фото
│   │   └── voice.py          # Голосовые
│   │
│   ├── scripts/              # Скрипты для БД
│   │   ├── create_animals_db.py
│   │   └── fill_animals_db.py
│   │
│   ├── services/             # Сервисы
│   │   ├── __init__.py
│   │   ├── ai_service.py     # OpenAI
│   │   ├── weather_service.py # Погода
│   │   └── recipe_service.py # Рецепты (опционально)
│   │
│   └── utils/                # Утилиты
│       ├── __init__.py
│       ├── time_utils.py
│       ├── text_utils.py
│       └── file_utils.py
│
├── data/                     # Данные
│   ├── conversations.db      # История
│   └── animals.db            # База животных
│
├── logs/                     # Логи
└── tests/                    # Тесты
```

---

## 📝 Ежедневные рассылки

* **9:00** — утреннее приветствие с пожеланием доброго дня.
* **11:00** — рассказ о случайном животном из базы (200+ видов).

> 🔔 Подписка оформляется через команду `/subscribe`.

---

## 🚀 Деплой на сервер

```bash
# Управление через systemd
systemctl start fluttershy-bot
systemctl enable fluttershy-bot

# Настройка автоперезапуска (watchdog)
crontab -e
*/5 * * * * /root/check_fluttershy.sh
```

---

## 📄 Лицензия

[MIT License](LICENSE) — свободное использование с указанием авторства.

---

## 👨‍💻 Автор

**MADAO81** — разработка и поддержка проекта.

_🦋 Сделано с добротой и заботой._
