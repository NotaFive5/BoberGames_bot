import requests
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import asyncio

TOKEN = "7216390191:AAFGcbaHrJtZgpF1UQuJwBFTIovIgPmnZv8"  # Вставь сюда токен от @BotFather
SERVER_URL = "https://flappybobr-production.up.railway.app/"  # URL сервера

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()  # Создаем Router (новый метод в aiogram v3.x)

@router.message(Command("start"))  # Используем Command() вместо старого commands=[]
async def start_command(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🎮 Играть")]],  # Теперь `keyboard` передаем явно
        resize_keyboard=True
    )
    await message.answer("Привет! Нажми кнопку, чтобы играть:", reply_markup=keyboard)

@router.message(Command("score"))
async def send_score(message: Message):
    user_id = str(message.from_user.id)
    response = requests.get(f"{SERVER_URL}/api/user_score/{user_id}")
    data = response.json()

    best_score = data.get("best_score", 0)
    await message.answer(f"🏆 Ваш лучший результат: {best_score} очков")

@router.message(Command("top"))
async def send_leaderboard(message: Message):
    response = requests.get(f"{SERVER_URL}/api/leaderboard")
    leaderboard = response.json()

    text = "🏆 ТОП 10 игроков:\n"
    for i, (u, s) in enumerate(leaderboard[:10]):
        text += f"{i+1}. ID {u}: {s} очков\n"

    await message.answer(text)

async def main():
    dp.include_router(router)  # Подключаем Router к Dispatcher
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
