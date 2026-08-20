import asyncio
import logging
import threading
import aiohttp
from http.server import HTTPServer, BaseHTTPRequestHandler

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

# ==========================================
# 0. ОБМАНКА ДЛЯ RENDER (ЧТОБЫ НЕ ВЫКЛЮЧАЛ БОТА)
# ==========================================
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is running!')

def run_fake_server():
    server_address = ('', 10000)
    httpd = HTTPServer(server_address, Handler)
    httpd.serve_forever()

threading.Thread(target=run_fake_server, daemon=True).start()

# ==========================================
# 1. НАСТРОЙКИ БОТА
# ==========================================
TOKEN = "8341288415:AAGJRA1gPGobFNkaF9kfkmfPx7DxLH0BdPo"
AUTHOR_CONTACT = "@erohon"

# Твой токен от @CryptoPayBot (уже вставлен)
API_TOKEN = "624233:AAUlGsPd2QWYytXARxRXP2LxyjxrWZ6l5Rk"

# ==========================================
# 2. ЗАПУСК БОТА
# ==========================================
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ==========================================
# 3. СТАРТОВОЕ МЕНЮ
# ==========================================
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

# ==========================================
# 4. ОПИСАНИЯ ТОВАРОВ И КНОПКА ССЫЛКИ
# ==========================================
@dp.callback_query(lambda c: c.data == "night")
async def night(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Получить ссылку на оплату", callback_data="pay_night")]
    ])
    await callback.message.answer(
        "🌙 *Ночной прорыв*\n\n"
        "Поможет тебе отключить внутренний диалог и провалиться в глубокий сон.\n\n"
        "📦 *В наборе:*\n"
        "• Аудиодорожка для засыпания (25 мин)\n"
        "• Текстовая практика 'Дыхание 4-7-8'\n"
        "• Чек-лист вечерней рутины\n\n"
        "💰 *Цена:* 149 ₽\n\n"
        "Нажми кнопку ниже, чтобы получить ссылку для оплаты ⬇️",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "thoughts")
async def thoughts(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Получить ссылку на оплату", callback_data="pay_thoughts")]
    ])
    await callback.message.answer(
        "🧠 *Мысли в порядок*\n\n"
        "Гайд для тех, у кого в голове «каша», и сложно сосредоточиться.\n\n"
        "📦 *В наборе:*\n"
        "• Техника «Пустой лист»\n"
        "• Аудио для фокуса (15 мин)\n"
        "• Чек-лист продуктивного утра\n\n"
        "💰 *Цена:* 299 ₽\n\n"
        "Нажми кнопку ниже, чтобы получить ссылку для оплаты ⬇️",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "vip")
async def vip(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Получить ссылку на оплату", callback_data="pay_vip")]
    ])
    await callback.message.answer(
        "💎 *VIP-доступ*\n\n"
        "Полный пакет всех гайдов + закрытый клуб.\n\n"
        "📦 *В наборе:*\n"
        "• Все гайды (Ночной прорыв, Мысли в порядок)\n"
        "• Ежемесячные новые практики\n"
        "• Закрытый чат с автором\n\n"
        "💰 *Цена:* 799 ₽\n\n"
        "Нажми кнопку ниже, чтобы получить ссылку для оплаты ⬇️",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "help")
async def help_info(callback: types.CallbackQuery):
    await callback.message.answer(
        "📖 *Как это работает:*\n\n"
        "1️⃣ Нажми на понравившийся гайд в меню.\n"
        "2️⃣ Ознакомься с описанием.\n"
        "3️⃣ Нажми «Получить ссылку на оплату».\n"
        "4️⃣ Перейди по ссылке и оплати картой.\n"
        "5️⃣ После оплаты товар придет тебе в этот чат.\n\n"
        "✅ Всё просто и честно!",
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "contact")
async def contact(callback: types.CallbackQuery):
    await callback.message.answer(
        f"📞 *Связаться со мной:*\n\n"
        f"Если у тебя возникли вопросы, пиши:\n"
        f"{AUTHOR_CONTACT}\n\n"
        f"Отвечаю в течение 10 минут!",
        parse_mode="Markdown"
    )
    await callback.answer()

# ==========================================
# 5. ГЕНЕРАЦИЯ ССЫЛКИ НА ОПЛАТУ В РУБЛЯХ
# ==========================================
async def create_crypto_pay_invoice(amount, description):
    url = "https://pay.crypt.bot/api/createInvoice"
    headers = {"Crypto-Pay-API-Token": API_TOKEN}
    data = {
        "asset": "RUB",               # ЗАПРАШИВАЕМ РУБЛИ
        "amount": amount,             # СУММА В РУБЛЯХ
        "description": description,
        "hidden_message": "Оплата гайда",
        "callback_url": "https://mybot-7-0osj.onrender.com"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as resp:
            if resp.status == 200:
                result = await resp.json()
                if result.get("ok"):
                    return result["result"]["pay_url"]
    return None

@dp.callback_query(lambda c: c.data.startswith("pay_"))
async def send_payment_link(callback: types.CallbackQuery):
    await callback.message.answer("⏳ Генерирую ссылку на оплату...")
    
    amount = 0
    desc = ""
    if callback.data == "pay_night":
        amount = 149
        desc = "Ночной прорыв"
    elif callback.data == "pay_thoughts":
        amount = 299
        desc = "Мысли в порядок"
    elif callback.data == "pay_vip":
        amount = 799
        desc = "VIP-доступ"
        
    link = await create_crypto_pay_invoice(amount, desc)
    
    if link:
        await callback.message.answer(
            f"✅ Ссылка на оплату готова!\n\n"
            f"Товар: {desc}\n"
            f"Сумма: {amount} ₽\n\n"
            f"👉 [Перейти к оплате картой]({link})",
            parse_mode="Markdown"
        )
    else:
        await callback.message.answer("❌ Ошибка при создании ссылки. Проверь, есть ли описание у магазина в Crypto Pay.")
    await callback.answer()

# ==========================================
# 6. ЗАПУСК
# ==========================================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
