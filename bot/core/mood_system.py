# bot/core/mood_system.py
"""
Система настроений для бота Флаттершай.
Определяет настроение на основе погоды в Ворсино (Боровский район).

Автор: MADAO81
Версия: 2.0
"""

import random
from typing import Tuple, Optional, Dict
from bot.services.weather_service import WeatherService
from bot.config import Config


class MoodSystem:
    """Управляет настроением Флаттершай на основе погоды."""

    def __init__(self):
        self.weather_service = WeatherService()
        self.sad_probability = Config.SAD_PROBABILITY
        self.current_mood = "happy"
        self.current_weather = None

    async def determine_mood(self) -> Tuple[str, Optional[Dict]]:
        """Определяет настроение на основе текущей погоды."""
        weather = await self.weather_service.get_weather()
        self.current_weather = weather

        if not weather:
            self.current_mood = "happy"
            return "happy", None

        if self.weather_service.is_bad_weather(weather):
            if random.random() < self.sad_probability:
                self.current_mood = "sad"
                return "sad", weather

        self.current_mood = "happy"
        return "happy", weather

    def get_mood_text(self, mood: str) -> str:
        """Возвращает текстовое описание настроения."""
        if mood == "sad":
            return "😔 Сегодня мне немного грустно... Но я всё равно рада видеть тебя! 🌸"
        return "🦋 У меня отличное настроение! Как чудесно, что мы встретились! 💕"

    def get_mood_emoji(self, mood: str) -> str:
        """Возвращает эмодзи для текущего настроения."""
        if mood == "sad":
            return "🌧️"
        return "🦋"

    def should_comment(self) -> bool:
        """Определяет, нужно ли комментировать сообщение (20% вероятности)."""
        return random.random() < 0.2

    def get_current_mood(self) -> str:
        """Возвращает текущее настроение."""
        return self.current_mood

    def get_current_weather(self) -> Optional[Dict]:
        """Возвращает текущие данные о погоде."""
        return self.current_weather
