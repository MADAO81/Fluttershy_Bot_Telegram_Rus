# bot/handlers/commands.py
"""
Обработчики команд для бота Флаттершай.
Команды: /start, /help, /weather, /petcare, /calm, /story, /kindness, /subscribe, /unsubscribe, /cleardata

Автор: MADAO81
Версия: 2.0
"""

import logging
import random
from telegram import Update
from telegram.ext import ContextTypes
from bot.core.mood_system import MoodSystem
from bot.services.ai_service import get_pinkie_response  # переименуем позже
from bot.services.weather_service import WeatherService
from bot.utils.time_utils import is_working_hours, get_working_status_message
from bot.core.constants import VERSION
from bot.core.scheduler import add_chat, remove_chat
from bot.core.context_manager import ContextManager

logger = logging.getLogger(__name__)

mood_system = MoodSystem()
weather_service = WeatherService()
context_manager = ContextManager()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /start command."""
    if not is_working_hours():
        if update.message.chat.type == "private":
            await update.message.reply_text(get_working_status_message())
        return

    mood, _ = await mood_system.determine_mood()
    mood_text = mood_system.get_mood_text(mood)
    mood_emoji = mood_system.get_mood_emoji(mood)

    text = (
        f"{mood_emoji} *Привет! Я Флаттершай!*\n\n"
        f"Я рада познакомиться с тобой! 🌸\n\n"
        f"{mood_text}\n\n"
        f"📋 *Вот что я умею:*\n"
        f"/help — список команд 📖\n"
        f"/weather — погода 🌤️\n"
        f"/petcare — совет по уходу за питомцем 🐾\n"
        f"/calm — упражнение для спокойствия 🕊️\n"
        f"/story — вдохновляющая история 📖\n"
        f"/kindness — комплимент или ободрение 💕\n"
        f"/subscribe — подписаться на ежедневные рассказы о животных 🐾\n"
        f"/unsubscribe — отписаться от рассказов 😢\n"
        f"/cleardata — удалить историю диалога 🗑️\n\n"
        f"🔒 *О данных:* Я сохраняю историю разговора только для поддержания беседы. "
        f"Данные не передаются третьим лицам. Напиши /cleardata, чтобы удалить всю историю.\n\n"
        f"Просто напиши мне что-нибудь, и мы поболтаем! 🌸\n\n"
        f"🤖 *Версия:* {VERSION}"
    )

    await update.message.reply_text(text, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /help command."""
    if not is_working_hours():
        if update.message.chat.type == "private":
            await update.message.reply_text(get_working_status_message())
        return

    text = (
        "📖 *Команды Флаттершай:*\n\n"
        "/start — начать общение 🌸\n"
        "/help — эта справка 📖\n"
        "/weather — погода 🌤️\n"
        "/petcare — совет по уходу за питомцем 🐾\n"
        "/calm — упражнение для спокойствия 🕊️\n"
        "/story — вдохновляющая история 📖\n"
        "/kindness — комплимент или ободрение 💕\n"
        "/subscribe — подписаться на ежедневные рассказы о животных 🐾\n"
        "/unsubscribe — отписаться от рассказов 😢\n"
        "/cleardata — удалить историю диалога 🗑️\n\n"
        "🔒 *О данных:* Я сохраняю историю разговора только для поддержания беседы. "
        "Данные не передаются третьим лицам.\n\n"
        "✨ *Особенности:*\n"
        "• Я работаю с 9:00 до 20:00 ежедневно\n"
        "• Если на улице дождь — могу немного погрустить 🌧️\n"
        "• Я обожаю животных и с радостью расскажу о них\n"
        "• Всегда готова поддержать и утешить 💕\n\n"
        "💡 *Совет:* Просто напиши мне что-нибудь, и мы поболтаем!"
    )

    await update.message.reply_text(text, parse_mode="Markdown")


async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /weather command."""
    if not is_working_hours():
        if update.message.chat.type == "private":
            await update.message.reply_text(get_working_status_message())
        return

    args = context.args
    city = " ".join(args) if args else None

    status_message = await update.message.reply_text("🌤️ Смотрю в окно... Сейчас узнаю!")

    try:
        if city:
            weather = await weather_service.get_weather_by_city(city)
            if not weather:
                await status_message.edit_text(
                    f"😅 Не могу найти город '{city}'!\n"
                    "Проверь название или попробуй просто /weather для Ворсино 🌤️"
                )
                return
        else:
            weather = await weather_service.get_weather()

        if weather:
            weather_text = weather_service.get_weather_text(weather)

            details = (
                f"\n\n📊 *Подробнее:*\n"
                f"💧 Влажность: {weather.get('humidity', '?')}%\n"
                f"💨 Ветер: {weather.get('wind_speed', '?')} м/с\n"
                f"📈 Давление: {weather.get('pressure', '?')} мм рт. ст."
            )

            full_text = f"🌤️ *Погода*\n\n{weather_text}{details}"

            if not city:
                mood, _ = await mood_system.determine_mood()
                if mood == "sad":
                    full_text += "\n\n😔 Погодка сегодня грустная... Но мы всегда можем найти уют внутри себя. 🌸"
                else:
                    full_text += "\n\n🌸 Отличная погода для прогулки с животными! 🐾"

            await status_message.delete()
            await update.message.reply_text(full_text, parse_mode="Markdown")
        else:
            await status_message.edit_text(
                "😅 Ой! Не могу узнать погоду!\n"
                "Попробуй позже! 🌧️"
            )

    except Exception as e:
        logger.error(f"❌ Ошибка получения погоды: {e}")
        await status_message.edit_text(
            "😅 Упс! Что-то пошло не так с погодой!\n"
            "Попробуй позже! 🌤️"
        )


async def petcare_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /petcare command."""
    if not is_working_hours():
        if update.message.chat.type == "private":
            await update.message.reply_text(get_working_status_message())
        return

    status_message = await update.message.reply_text("🐾 Дай-ка подумать о твоём питомце...")

    # Получаем запрос пользователя (если есть)
    args = context.args
    query = " ".join(args) if args else "питомец"

    # Генерируем совет через AI
    mood, _ = await mood_system.determine_mood()
    mood_desc = "sad" if mood == "sad" else "happy"

    response = await get_pinkie_response(
        user_message=f"Пользователь спрашивает: {query}. Дай добрый и полезный совет по уходу за этим животным. Говори мягко, с заботой. Используй нежные эмодзи.",
        mood_description=mood_desc
    )

    await status_message.delete()

    if response:
        await update.message.reply_text(f"🐾 *Совет от Флаттершай:*\n\n{response}", parse_mode="Markdown")
    else:
        await update.message.reply_text("😅 Ой! Я не смогла придумать совет... Попробуй ещё раз! 🐾")


async def calm_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /calm command."""
    if not is_working_hours():
        if update.message.chat.type == "private":
            await update.message.reply_text(get_working_status_message())
        return

    status_message = await update.message.reply_text("🕊️ Сейчас я помогу тебе успокоиться...")

    mood, _ = await mood_system.determine_mood()
    mood_desc = "sad" if mood == "sad" else "happy"

    response = await get_pinkie_response(
        user_message="Предложи короткое и мягкое упражнение для дыхания или визуализации, чтобы помочь человеку успокоиться. Говори тихо, нежно, с заботой. Используй образы природы, цветов, света. В конце добавь тёплое ободряющее слово.",
        mood_description=mood_desc
    )

    await status_message.delete()

    if response:
        await update.message.reply_text(f"🕊️ *Упражнение для спокойствия:*\n\n{response}", parse_mode="Markdown")
    else:
        await update.message.reply_text("😅 Ой! Я не смогла придумать упражнение... Попробуй ещё раз! 🕊️")


async def story_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /story command."""
    if not is_working_hours():
        if update.message.chat.type == "private":
            await update.message.reply_text(get_working_status_message())
        return

    status_message = await update.message.reply_text("📖 Сейчас я расскажу тебе одну историю...")

    mood, _ = await mood_system.determine_mood()
    mood_desc = "sad" if mood == "sad" else "happy"

    response = await get_pinkie_response(
        user_message="Расскажи короткую вдохновляющую историю о животных, доброте или дружбе. Пусть она будет тёплой и уютной, как чашка чая. Используй мягкие, нежные слова. В конце добавь вывод или мораль.",
        mood_description=mood_desc
    )

    await status_message.delete()

    if response:
        await update.message.reply_text(f"📖 *История от Флаттершай:*\n\n{response}", parse_mode="Markdown")
    else:
        await update.message.reply_text("😅 Ой! Я не смогла придумать историю... Попробуй ещё раз! 📖")


async def kindness_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /kindness command."""
    if not is_working_hours():
        if update.message.chat.type == "private":
            await update.message.reply_text(get_working_status_message())
        return

    status_message = await update.message.reply_text("💕 Дай-ка я скажу тебе что-то тёплое...")

    mood, _ = await mood_system.determine_mood()
    mood_desc = "sad" if mood == "sad" else "happy"

    response = await get_pinkie_response(
        user_message="Скажи добрый, тёплый комплимент или ободрение. Говори мягко, искренне, как будто разговариваешь с близким другом. Используй нежные слова и эмодзи. Сделай так, чтобы человек почувствовал себя ценным и любимым.",
        mood_description=mood_desc
    )

    await status_message.delete()

    if response:
        await update.message.reply_text(f"💕 *Слова доброты от Флаттершай:*\n\n{response}", parse_mode="Markdown")
    else:
        await update.message.reply_text("😅 Ой! Я не смогла подобрать слова... Попробуй ещё раз! 💕")


async def subscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Подписка на ежедневные рассказы о животных."""
    chat_id = update.message.chat_id
    add_chat(chat_id)
    await update.message.reply_text(
        "🐾 *Ты подписалась на ежедневные рассказы о животных!*\n\n"
        "Каждый день в 11:00 я буду присылать тебе удивительный рассказ о каком-нибудь животном! 🦋\n\n"
        "А в 9:00 я буду желать тебе доброго утра! 🌸\n\n"
        "Чтобы отписаться, напиши /unsubscribe 😢",
        parse_mode="Markdown"
    )


async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отписка от ежедневных рассказов."""
    chat_id = update.message.chat_id
    remove_chat(chat_id)
    await update.message.reply_text(
        "😢 *Ты отписалась от ежедневных рассказов!*\n\n"
        "Если захочешь вернуться — напиши /subscribe 🐾",
        parse_mode="Markdown"
    )


async def clear_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Очистка истории диалога."""
    user_id = update.effective_user.id
    context_manager.clear_context(user_id)
    await update.message.reply_text(
        "🗑️ *Твоя история диалога удалена!*\n\n"
        "Теперь я ничего не помню о нашем разговоре. Но мы всегда можем начать заново! 😊🌸",
        parse_mode="Markdown"
    )