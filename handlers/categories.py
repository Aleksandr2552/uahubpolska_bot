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

choose_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔎 Шукаю"),
            KeyboardButton(text="✅ Пропоную")
        ]
    ],
    resize_keyboard=True
)

@router.message(F.text == "🔥 Робота")
async def work_category(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        category="🔥 Робота"
    )

    await message.answer(
        "👇 Оберіть тип оголошення",
        reply_markup=choose_keyboard
    )

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
        "📝 Заголовок"
    )

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
        "💰 Ціна або зарплата"
    )

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

@router.message(AdForm.contact)
async def contact(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        contact=message.text
    )

    await message.answer(
        "✅ Оголошення створено"
    )

    await state.clear()