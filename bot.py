import asyncio
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

# ==========================================
# 0. ОБМАНКА ДЛЯ RENDER (ЧТОБЫ НЕ ВЫКЛЮЧАЛ)
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

# Твой ID кошелька ЮMoney (уже вставлен с твоего скриншота)
YOOMONEY_ID = "4100119606524632" 

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
# 4. ТОВАРЫ И ССЫЛКИ НА ОПЛАТУ
# ==========================================
def get_yoomoney_link(amount, product_name):
    # Генерируем ссылку на оплату (СБП, Сбер, Т-Банк, карта)
    return f"https://yoomoney.ru/quickpay/confirm?receiver={YOOMONEY_ID}&quickpay-form=shop&targets={product_name}&sum={amount}"

@dp.callback_query(lambda c: c.data == "night")
async def night(callback: types.CallbackQuery):
    pay_link = get_yoomoney_link(149, "Ночной прорыв")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить 149 ₽", url=pay_link)]
    ])
    await callback.message.answer(
        "🌙 *Ночной прорыв*\n\n"
        "Поможет тебе отключить внутренний диалог и провалиться в глубокий сон.\n\n"
        "📦 *В наборе:*\n"
        "• Аудиодорожка для засыпания (25 мин)\n"
        "• Текстовая практика 'Дыхание 4-7-8'\n"
        "• Чек-лист вечерней рутины\n\n"
        "💰 *Цена:* 149 ₽\n\n"
        "Нажми кнопку ниже, чтобы перейти к оплате ⬇️",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "thoughts")
async def thoughts(callback: types.CallbackQuery):
    pay_link = get_yoomoney_link(299, "Мысли в порядок")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить 299 ₽", url=pay_link)]
    ])
    await callback.message.answer(
        "🧠 *Мысли в порядок*\n\n"
        "Гайд для тех, у кого в голове «каша», и сложно сосредоточиться.\n\n"
        "📦 *В наборе:*\n"
        "• Техника «Пустой лист»\n"
        "• Аудио для фокуса (15 мин)\n"
        "• Чек-лист продуктивного утра\n\n"
        "💰 *Цена:* 299 ₽\n\n"
        "Нажми кнопку ниже, чтобы перейти к оплате ⬇️",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "vip")
async def vip(callback: types.CallbackQuery):
    pay_link = get_yoomoney_link(799, "VIP-доступ")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить 799 ₽", url=pay_link)]
    ])
    await callback.message.answer(
        "💎 *VIP-доступ*\n\n"
        "Полный пакет всех гайдов + закрытый клуб.\n\n"
        "📦 *В наборе:*\n"
        "• Все гайды (Ночной прорыв, Мысли в порядок)\n"
        "• Ежемесячные новые практики\n"
        "• Закрытый чат с автором\n\n"
        "💰 *Цена:* 799 ₽\n\n"
        "Нажми кнопку ниже, чтобы перейти к оплате ⬇️",
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
        "4️⃣ Оплати через СБП или карту.\n"
        "5️⃣ После оплаты напиши автору, чтобы получить гайд.\n\n"
        "✅ Всё просто и честно!",
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "contact")
async def contact(callback: types.CallbackQuery):
    await callback.message.answer(
        f"📞 *Связаться со мной:*\n\n"
        f"Если у тебя возникли вопросы или после оплаты — пиши:\n"
        f"{AUTHOR_CONTACT}\n\n"
        f"Отвечаю в течение 10 минут!",
        parse_mode="Markdown"
    )
    await callback.answer()

# ==========================================
# 5. ЗАПУСК БОТА
# ==========================================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
