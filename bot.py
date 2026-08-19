import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

# ТВОЙ ТОКЕН (уже вставлен)
TOKEN = 8341288415:AAGJRA1gPGobFNkaF9kfkmfPx7DxLH0BdPo

# Включаем логирование (чтобы видеть ошибки)
logging.basicConfig(level=logging.INFO)

# Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# СТАРТОВОЕ СООБЩЕНИЕ
@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌙 Ночной прорыв (149 ₽)", callback_data="night")],
        [InlineKeyboardButton(text="🧠 Мысли в порядок (299 ₽)", callback_data="thoughts")],
        [InlineKeyboardButton(text="💎 VIP-доступ (799 ₽)", callback_data="vip")],
        [InlineKeyboardButton(text="❓ Как это работает", callback_data="help")],
        [InlineKeyboardButton(text="📞 Связаться с автором", callback_data="contact")]
    ])
    await message.answer(
        "🌙 *Привет! Ты не спишь?*\n\n"
        "Я — *ГАЙДЕР*. Помогу тебе успокоиться, уснуть и навести порядок в голове.\n\n"
        "Выбери свой гайд 👇",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# КНОПКА "НОЧНОЙ ПРОРЫВ"
@dp.callback_query(lambda c: c.data == "night")
async def night(callback: types.CallbackQuery):
    await callback.message.answer(
        "🌙 *Ночной прорыв*\n\n"
        "Техника засыпания за 5 минут + аудиодорожка.\n\n"
        "💰 Цена: 149 ₽\n\n"
        "Оплата пока вручную — напиши мне, и я пришлю PDF 🤝",
        parse_mode="Markdown"
    )
    await callback.answer()

# КНОПКА "МЫСЛИ В ПОРЯДОК"
@dp.callback_query(lambda c: c.data == "thoughts")
async def thoughts(callback: types.CallbackQuery):
    await callback.message.answer(
        "🧠 *Мысли в порядок*\n\n"
        "3 техники остановки тревоги + чек-лист 'Утро после'.\n\n"
        "💰 Цена: 299 ₽\n\n"
        "Оплата пока вручную — напиши мне, и я пришлю PDF 🤝",
        parse_mode="Markdown"
    )
    await callback.answer()

# КНОПКА "VIP-ДОСТУП"
@dp.callback_query(lambda c: c.data == "vip")
async def vip(callback: types.CallbackQuery):
    await callback.message.answer(
        "💎 *VIP-доступ*\n\n"
        "Все гайды + ежемесячные обновления + закрытый чат.\n\n"
        "💰 Цена: 799 ₽\n\n"
        "Оплата пока вручную — напиши мне, и я пришлю PDF 🤝",
        parse_mode="Markdown"
    )
    await callback.answer()

# КНОПКА "КАК ЭТО РАБОТАЕТ"
@dp.callback_query(lambda c: c.data == "help")
async def help(callback: types.CallbackQuery):
    await callback.message.answer(
        "📖 *Как это работает:*\n\n"
        "1. Выбери гайд\n"
        "2. Напиши мне\n"
        "3. Я пришлю PDF и реквизиты\n"
        "4. Ты оплачиваешь и получаешь гайд\n\n"
        "✅ Всё просто и честно!",
        parse_mode="Markdown"
    )
    await callback.answer()

# КНОПКА "СВЯЗАТЬСЯ"
@dp.callback_query(lambda c: c.data == "contact")
async def contact(callback: types.CallbackQuery):
    await callback.message.answer(
        "📞 *Связаться со мной:*\n\n"
        "Напиши в личные сообщения:\n"
        "@твой_никнейм (вставь сюда свой Telegram @)\n\n"
        "Отвечаю в течение 10 минут!",
        parse_mode="Markdown"
    )
    await callback.answer()

# ЗАПУСК
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
