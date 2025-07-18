from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart
import asyncio

# 🔐 Твой токен
BOT_TOKEN = "7440614918:AAEtmd41M4rNpCl5etIFwD7fY9QKIlHznuM"
# 🧑‍💼 Твой Telegram ID
ADMIN_ID = 540311740  # Замени на свой ID, если нужен другой

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 🎛 Кнопки меню
menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🏠 Создать объект", callback_data="new_object")],
    [InlineKeyboardButton(text="📝 Создать заявку (покупка)", callback_data="new_request")],
])

# 📌 Старт
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Выберите тип заявки:", reply_markup=menu_keyboard)

# 🧾 Обработка нажатия кнопок
@dp.callback_query(F.data == "new_object")
async def object_template(callback: CallbackQuery):
    text = (
        "Заполни данные по шаблону:\n\n"
        "Тип: \n"
        "Дольщик (да/нет): \n"
        "Адрес: \n"
        "Цена (в руб.): \n"
        "Кадастр: \n"
        "Комнаты (Студия, 1к, 2к и т.д.): \n"
        "Площадь (м²): \n"
        "Этаж: \n"
        "Подъезд: \n"
        "Ремонт (Без ремонта, Косметический, Евро и т.д.): \n"
        "Фиктивный (да/нет):"
    )
    await callback.message.answer(text)
    await callback.answer()

@dp.callback_query(F.data == "new_request")
async def request_template(callback: CallbackQuery):
    text = (
        "Заполни данные по шаблону:\n\n"
        "Заголовок (необязательно): \n"
        "Тип операции: покупка\n"
        "Телефон клиента: \n"
        "Представитель юр. лица/ИП: да (ФИО и данные) / нет\n"
        "Кто обратился: клиент / агент\n"
        "Вид заявки: обычная / межрегиональная\n"
        "Класс недвижимости: квартиры / гаражи / коммерческая / загородная\n"
        "Новостройка: да / нет\n"
        "Тип объекта: квартира / пансионат / малосемейка / общежитие и т.д.\n"
        "Район: \n"
        "Источник средств на покупку: ипотека / материнский капитал и т.д.\n"
        "Запланированная дата покупки: в течение месяца / 2-х / 3-х месяцев\n"
        "Цена: от ... до ...\n"
        "Общая площадь: от ... до ... м²\n"
        "Ремонт: \n"
        "Количество комнат: \n"
        "Год постройки: от ... до ..."
    )
    await callback.message.answer(text)
    await callback.answer()

# 📨 Обработка любых заполненных шаблонов
@dp.message()
async def handle_filled_template(message: Message):
    lines = message.text.strip().split("\n")
    formatted = ""
    for line in lines:
        if ":" in line:
            formatted += f"{line.strip()}\n"
    if formatted:
        await bot.send_message(ADMIN_ID, f"🆕 Заявка:\n\n{formatted}")
        await message.answer("✅ Заявка отправлена!")
    else:
        await message.answer("⚠️ Не удалось распознать шаблон. Убедись, что каждая строка содержит `ключ: значение`.")

# 🚀 Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())