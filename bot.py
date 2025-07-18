from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message, InputFile
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio

# 🔐 Твой токен
BOT_TOKEN = "7440614918:AAEtmd41M4rNpCl5etIFwD7fY9QKIlHznuM"
# 🧑‍💼 Твой Telegram ID
ADMIN_ID = 540311740  # Замени на свой ID, если нужен другой

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 🎯 Состояния опроса
class Form(StatesGroup):
    type = State()
    dolshik = State()
    address = State()
    price = State()
    cadastre = State()
    rooms = State()
    area = State()
    floor = State()
    entrance = State()
    repair = State()
    fake = State()
    photo = State()

# 📌 Старт
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Давай добавим объект недвижимости.\n\n📋 Введи тип недвижимости (например: Квартира, Комната):")
    await state.set_state(Form.type)

@dp.message(Form.type)
async def step_type(message: Message, state: FSMContext):
    await state.update_data(type=message.text)
    await message.answer("🏢 Объект от дольщика? (да/нет):")
    await state.set_state(Form.dolshik)

@dp.message(Form.dolshik)
async def step_dolshik(message: Message, state: FSMContext):
    await state.update_data(dolshik=message.text)
    await message.answer("📍 Введи адрес (Улица, дом, квартира):")
    await state.set_state(Form.address)

@dp.message(Form.address)
async def step_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("💰 Укажи цену в рублях:")
    await state.set_state(Form.price)

@dp.message(Form.price)
async def step_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("🆔 Введи кадастровый номер:")
    await state.set_state(Form.cadastre)

@dp.message(Form.cadastre)
async def step_cadastre(message: Message, state: FSMContext):
    await state.update_data(cadastre=message.text)
    await message.answer("🚪 Сколько комнат? (Студия, 1к, 2к, 3к, 4к+):")
    await state.set_state(Form.rooms)

@dp.message(Form.rooms)
async def step_rooms(message: Message, state: FSMContext):
    await state.update_data(rooms=message.text)
    await message.answer("📐 Общая площадь в м²:")
    await state.set_state(Form.area)

@dp.message(Form.area)
async def step_area(message: Message, state: FSMContext):
    await state.update_data(area=message.text)
    await message.answer("🏢 Этаж:")
    await state.set_state(Form.floor)

@dp.message(Form.floor)
async def step_floor(message: Message, state: FSMContext):
    await state.update_data(floor=message.text)
    await message.answer("🚪 Номер подъезда:")
    await state.set_state(Form.entrance)

@dp.message(Form.entrance)
async def step_entrance(message: Message, state: FSMContext):
    await state.update_data(entrance=message.text)
    await message.answer("🔧 Тип ремонта (Без ремонта, Косметический, Евро, Дизайнерский):")
    await state.set_state(Form.repair)

@dp.message(Form.repair)
async def step_repair(message: Message, state: FSMContext):
    await state.update_data(repair=message.text)
    await message.answer("📦 Это фиктивный объект? (да/нет):")
    await state.set_state(Form.fake)

@dp.message(Form.fake)
async def step_fake(message: Message, state: FSMContext):
    await state.update_data(fake=message.text)
    await message.answer("📸 Отправь фотографию объекта или напиши 'нет':")
    await state.set_state(Form.photo)

@dp.message(Form.photo)
async def step_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    photo_text = "Без фото"

    if message.photo:
        await bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption="📸 Фото объекта")
        photo_text = "Фото отправлено отдельно"
    elif message.text.lower() != "нет":
        photo_text = message.text

    text = (
        f"🆕 Новая заявка:\n\n"
        f"📋 Тип: {data['type']}\n"
        f"👤 От дольщика: {data['dolshik']}\n"
        f"📍 Адрес: {data['address']}\n"
        f"💰 Цена: {data['price']} руб.\n"
        f"🆔 Кадастр: {data['cadastre']}\n"
        f"🚪 Комнаты: {data['rooms']}\n"
        f"📐 Площадь: {data['area']} м²\n"
        f"🏢 Этаж: {data['floor']}\n"
        f"🚪 Подъезд: {data['entrance']}\n"
        f"🔧 Ремонт: {data['repair']}\n"
        f"📦 Фиктивный объект: {data['fake']}\n"
        f"🖼️ Фото: {photo_text}"
    )

    await bot.send_message(ADMIN_ID, text)
    await message.answer("✅ Заявка отправлена! Спасибо.")
    await state.clear()

# 🚀 Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
