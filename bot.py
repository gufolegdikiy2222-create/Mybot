import asyncio
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice, PreCheckoutQuery
from aiogram.filters import Command

# ==========================================
# 0. ОБМАНКА ДЛЯ RENDER
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
# 1. НАСТРОЙКИ
# ==========================================
TOKEN = "8341288415:AAGJRA1gPGobFNkaF9kfkmfPx7DxLH0BdPo"
PAYMENTS_TOKEN = "624233:AAUlGsPd2QWYytXARxRXP2LxyjxrWZ6l5Rk"
AUTHOR_CONTACT = "@erohon"

# ==========================================
# 2. БОТ
# ==========================================
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ==========================================
# 3. МЕНЮ
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
# 4. ТОВАРЫ
# ==========================================
@dp.callback_query(lambda c: c.data == "night")
async def night(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить 149 ₽", callback_data="pay_night")]
    ])
    await callback.message.answer(
        "🌙 *Ночной прорыв*\n\n"
        "Поможет тебе отключить внутренний диалог и провалиться в глубокий сон.\n\n"
        "📦 *В наборе:*\n"
        "• Аудиодорожка для засыпания (25 мин)\n"
        "• Текстовая практика 'Дыхание 4-7-8'\n"
        "• Чек-лист вечерней рутины\n\n"
        "💰 *Цена:* 149 ₽\n\n"
        "Нажми «Оплатить», чтобы открыть доступ ⬇️",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "thoughts")
async def thoughts(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить 299 ₽", callback_data="pay_thoughts")]
    ])
    await callback.message.answer(
        "🧠 *Мысли в порядок*\n\n"
        "Гайд для тех, у кого в голове «каша», и сложно сосредоточиться.\n\n"
        "📦 *В наборе:*\n"
        "• Техника «Пустой лист»\n"
        "• Аудио для фокуса (15 мин)\n"
        "• Чек-лист продуктивного утра\n\n"
        "💰 *Цена:* 299 ₽\n\n"
        "Нажми «Оплатить», чтобы открыть доступ ⬇️",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "vip")
async def vip(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить 799 ₽", callback_data="pay_vip")]
    ])
    await callback.message.answer(
        "💎 *VIP-доступ*\n\n"
        "Полный пакет всех гайдов + закрытый клуб.\n\n"
        "📦 *В наборе:*\n"
        "• Все гайды (Ночной прорыв, Мысли в порядок)\n"
        "• Ежемесячные новые практики\n"
        "• Закрытый чат с автором\n\n"
        "💰 *Цена:* 799 ₽\n\n"
        "Нажми «Оплатить», чтобы открыть доступ ⬇️",
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
        "3️⃣ Нажми «Оплатить».\n"
        "4️⃣ После успешной оплаты товар придет тебе в этот чат.\n\n"
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
# 5. ОПЛАТА
# ==========================================
@dp.callback_query(lambda c: c.data.startswith("pay_"))
async def process_payment(callback: types.CallbackQuery):
    price = 0
    title = ""
    description = ""
    payload = ""
    
    if callback.data == "pay_night":
        price = 149
        title = "Ночной прорыв"
        description = "Аудио и чек-лист для сна"
        payload = "night_access"
    elif callback.data == "pay_thoughts":
        price = 299
        title = "Мысли в порядок"
        description = "Техники и аудио для фокуса"
        payload = "thoughts_access"
    elif callback.data == "pay_vip":
        price = 799
        title = "VIP-доступ"
        description = "Все гайды и закрытый чат"
        payload = "vip_access"

    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title=title,
        description=description,
        payload=payload,
        provider_token=PAYMENTS_TOKEN,
        currency="RUB",
        prices=[LabeledPrice(label=title, amount=price)]
    )
    await callback.answer()

@dp.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def process_successful_payment(message: types.Message):
    text = "✅ *Оплата прошла успешно! Спасибо за покупку!*\n\n"
    text += "Твой гайд готовится к выдаче и появится здесь в ближайшее время.\n\n"
    text += f"По всем вопросам пиши автору: {AUTHOR_CONTACT}"

    await message.answer(text, parse_mode="Markdown")

# ==========================================
# 6. ЗАПУСК
# ==========================================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
