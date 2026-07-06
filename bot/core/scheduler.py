# bot/core/scheduler.py
"""
Планировщик для бота Флаттершай.
Отправка утреннего приветствия в 9:00 и рассказа о животном в 11:00.

Автор: MADAO81
Версия: 2.0
"""

import logging
import sqlite3
import random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot.config import Config
from bot.services.recipe_service import RecipeService

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

DB_PATH = Config.DATA_DIR / "animals.db"


def _get_connection():
    return sqlite3.connect(DB_PATH)


def _init_db():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            chat_id INTEGER PRIMARY KEY,
            subscribed_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def add_chat(chat_id: int):
    _init_db()
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO subscriptions (chat_id) VALUES (?)", (chat_id,))
    conn.commit()
    conn.close()
    logger.info(f"📋 Чат {chat_id} добавлен для рассылки")


def remove_chat(chat_id: int):
    _init_db()
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subscriptions WHERE chat_id = ?", (chat_id,))
    conn.commit()
    conn.close()
    logger.info(f"📋 Чат {chat_id} удалён из рассылки")


def get_active_chats():
    _init_db()
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM subscriptions")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]


async def send_morning_greeting(app):
    """Отправляет утреннее приветствие в 9:00."""
    active_chats = get_active_chats()
    if not active_chats:
        logger.info("📭 Нет активных чатов для утреннего приветствия")
        return

    logger.info(f"🌅 Отправка утреннего приветствия в {len(active_chats)} чатов...")

    greetings = [
        "🌸 *Доброе утро!* Пусть этот день будет наполнен теплом, уютом и маленькими радостями. Помни: ты — замечательная(ый), и я верю в тебя! 🦋",
        "🌼 *С добрым утром!* Я надеюсь, что сегодня у тебя будет много поводов для улыбки. А если что-то пойдёт не так — я всегда рядом, чтобы поддержать тебя. 💕",
        "🌻 *Привет!* Сегодня новый день, а значит — новые возможности. Ты справишься со всем, что бы ни случилось. Я в тебя верю! 🐇",
        "🦋 *Доброе утро!* Пусть солнечный свет согревает тебя, а моя мысль о тебе дарит уют. Береги себя и своё сердце. 🌸",
    ]

    greeting = random.choice(greetings)

    for chat_id in active_chats:
        try:
            await app.bot.send_message(
                chat_id=chat_id,
                text=greeting,
                parse_mode="Markdown"
            )
            logger.info(f"✅ Утреннее приветствие отправлено в чат {chat_id}")
        except Exception as e:
            logger.error(f"❌ Ошибка отправки в чат {chat_id}: {e}")
            if "bot was blocked" in str(e) or "chat not found" in str(e):
                remove_chat(chat_id)


async def send_daily_animal(app):
    """Отправляет рассказ о животном в 11:00."""
    active_chats = get_active_chats()
    if not active_chats:
        logger.info("📭 Нет активных чатов для рассказа о животном")
        return

    logger.info(f"🐾 Отправка рассказа о животном в {len(active_chats)} чатов...")

    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, scientific_name, habitat, diet, fun_fact, description FROM animals ORDER BY RANDOM() LIMIT 1")
        animal = cursor.fetchone()
        conn.close()

        if not animal:
            logger.warning("⚠️ Нет животных в базе данных")
            return

        name, scientific_name, habitat, diet, fun_fact, description = animal

        message = (
            f"🐾 *Сегодня я расскажу тебе о {name}*\n\n"
            f"*Научное название:* {scientific_name or 'неизвестно'}\n"
            f"*Среда обитания:* {habitat}\n"
            f"*Питание:* {diet}\n"
            f"*Интересный факт:* {fun_fact}\n\n"
            f"📖 *Подробнее:*\n{description}\n\n"
            f"🌸 Надеюсь, тебе было интересно! У каждого животного есть своя удивительная история. 💕"
        )

        for chat_id in active_chats:
            try:
                await app.bot.send_message(
                    chat_id=chat_id,
                    text=message,
                    parse_mode="Markdown"
                )
                logger.info(f"✅ Рассказ о животном отправлен в чат {chat_id}")
            except Exception as e:
                logger.error(f"❌ Ошибка отправки в чат {chat_id}: {e}")
                if "bot was blocked" in str(e) or "chat not found" in str(e):
                    remove_chat(chat_id)

    except Exception as e:
        logger.error(f"❌ Ошибка при отправке рассказа о животном: {e}")


def start_scheduler(app):
    """Запускает планировщик."""
    try:
        _init_db()

        # Утреннее приветствие в 9:00
        scheduler.add_job(
            send_morning_greeting,
            CronTrigger(hour=9, minute=0),
            args=[app],
            id='morning_greeting',
            replace_existing=True
        )

        # Рассказ о животном в 11:00
        scheduler.add_job(
            send_daily_animal,
            CronTrigger(hour=11, minute=0),
            args=[app],
            id='daily_animal',
            replace_existing=True
        )

        scheduler.start()
        logger.info("✅ Планировщик запущен. Утреннее приветствие в 9:00, рассказ о животном в 11:00")

    except Exception as e:
        logger.error(f"❌ Ошибка при запуске планировщика: {e}")


def stop_scheduler():
    """Останавливает планировщик."""
    try:
        scheduler.shutdown()
        logger.info("⏹️ Планировщик остановлен")
    except Exception as e:
        logger.error(f"❌ Ошибка при остановке планировщика: {e}")