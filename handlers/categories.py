from aiogram import Router
from aiogram import F

from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton
)

from aiogram.fsm.context import FSMContext

from states.forms import AdForm

router = Router()

# =========================
# КНОПКИ
# =========================

choose_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔎 Шукаю"),
            KeyboardButton(text="✅ Пропоную")
        ]
    ],
    resize_keyboard=True
)

# =========================
# ВИБІР КАТЕГОРІЇ
# =========================

@router.message(F.text == "🔥 Робота")
@router.message(F.text == "🏠 Житло")
@router.message(F.text == "🛠 Послуги")
@router.message(F.text == "🚗 Перевезення")
@router.message(F.text == "📄 Документи")
async def category_start(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        category=message.text
    )

    await message.answer(
        "👇 Оберіть тип оголошення",
        reply_markup=choose_keyboard
    )

# =========================
# ШУКАЮ / ПРОПОНУЮ
# =========================

@router.message(F.text == "🔎 Шукаю")
@router.message(F.text == "✅ Пропоную")
async def choose_type(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        ad_type=message.text
    )

    await state.set_state(
        AdForm.city
    )

    await message.answer(
        "📍 Вкажіть місто"
    )

# =========================
# МІСТО
# =========================

@router.message(AdForm.city)
async def city(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        city=message.text
    )

    await state.set_state(
        AdForm.title
    )

    await message.answer(
        "📝 Вкажіть заголовок"
    )

# =========================
# ЗАГОЛОВОК
# =========================

@router.message(AdForm.title)
async def title(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        title=message.text
    )

    await state.set_state(
        AdForm.price
    )

    await message.answer(
        "💰 Вкажіть ціну або зарплату"
    )

# =========================
# ЦІНА
# =========================

@router.message(AdForm.price)
async def price(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        price=message.text
    )

    await state.set_state(
        AdForm.description
    )

    await message.answer(
        "📄 Напишіть опис"
    )

# =========================
# ОПИС
# =========================

@router.message(AdForm.description)
async def description(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        description=message.text
    )

    await state.set_state(
        AdForm.contact
    )

    await message.answer(
        "📞 Вкажіть контакт"
    )

# =========================
# КОНТАКТ
# =========================

@router.message(AdForm.contact)
async def contact(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        contact=message.text
    )

    data = await state.get_data()

    post_text = f"""
{data['category']} 🇵🇱

{data['ad_type']}

📍 Місто: {data['city']}

📝 {data['title']}

💰 {data['price']}

📄 Опис:
{data['description']}

📞 Контакт:
{data['contact']}

━━━━━━━━━━━━━━━
🇵🇱 @UAhubPolska
"""

    # ВІДПРАВКА АДМІНУ

    await message.bot.send_message(
        1561352771,
        post_text
    )

    # ПОВІДОМЛЕННЯ КОРИСТУВАЧУ

    await message.answer(
        "✅ Оголошення створено та відправлено на модерацію",
        reply_markup=main_keyboard
    )

    await state.clear()