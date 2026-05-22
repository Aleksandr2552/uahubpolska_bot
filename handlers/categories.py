from aiogram import Router
from aiogram import F

from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from states.forms import AdForm
from handlers.start import main_keyboard

router = Router()

# =========================
# FSM МОДЕРАЦІЇ
# =========================

class ModerationState(StatesGroup):

    reject_reason = State()

    ban_reason = State()

# =========================
# БАН ЛИСТ
# =========================

    banned_users = {}

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

    await state.clear()

    if message.from_user.id in banned_users:

        await message.answer(
            "🚫 Ви забанені"
        )

        return

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
👤 ID: {message.from_user.id}

🇵🇱 @UAhubPolska
"""

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="✅ Опублікувати",
                    callback_data="publish"
                ),

                InlineKeyboardButton(
                    text="❌ Відхилити",
                    callback_data="reject"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🚫 Забанити",
                    callback_data=f"ban_{message.from_user.id}"
                )
            ]
        ]
    )

    await message.bot.send_message(
        1561352771,
        post_text,
        reply_markup=keyboard
    )

    await state.clear()

    await message.answer(
        "✅ Оголошення створено та відправлено на модерацію",
        reply_markup=main_keyboard
    )

    await message.answer(
    "🏠 Головне меню",
    reply_markup=main_keyboard
)
# =========================
# ПУБЛІКАЦІЯ
# =========================

@router.callback_query(F.data == "publish")
async def publish_post(
    callback: CallbackQuery
):

    text = callback.message.text

    await callback.bot.send_message(
        "@UAhubPolska",
        text
    )

    await callback.message.edit_text(
        text + "\n\n✅ ОПУБЛІКОВАНО"
    )

# =========================
# ВІДХИЛЕННЯ
# =========================

@router.callback_query(F.data == "reject")
async def reject_post(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.update_data(
        reject_message=callback.message.text
    )

    await state.set_state(
        ModerationState.reject_reason
    )

    await callback.message.answer(
        "✍️ Напишіть причину відхилення"
    )

@router.message(ModerationState.reject_reason)
async def reject_reason(
    message: Message,
    state: FSMContext
):

    data = await state.get_data()

    text = data["reject_message"]

    user_id = int(
        text.split("👤 ID: ")[1].split("\n")[0]
    )

    new_text = (
        text +
        f"\n\n❌ ВІДХИЛЕНО\n\n📌 Причина:\n{message.text}"
    )

    await message.bot.send_message(
        user_id,
        f"❌ Ваше оголошення відхилено\n\n📌 Причина:\n{message.text}"
    )

    await message.answer(
        "✅ Користувачу відправлено причину"
    )

    await message.bot.send_message(
        1561352771,
        new_text
    )

    await state.clear()

# =========================
# БАН
# =========================

@router.callback_query(F.data.startswith("ban_"))
async def ban_user(
    callback: CallbackQuery,
    state: FSMContext
):

    user_id = int(
        callback.data.split("_")[1]
    )

    await state.update_data(
        ban_user=user_id,
        ban_message=callback.message.text
    )

    await state.set_state(
        ModerationState.ban_reason
    )

    await callback.message.answer(
        "🚫 Напишіть причину бану"
    )

@router.message(ModerationState.ban_reason)
async def ban_reason(
    message: Message,
    state: FSMContext
):

    data = await state.get_data()

    user_id = data["ban_user"]

    banned_users[user_id] = message.text

    await message.bot.send_message(
        user_id,
        f"🚫 Вас забанено\n\n📌 Причина:\n{message.text}"
    )

    await message.answer(
        "✅ Користувача забанено"
    )

    await state.clear()

# =========================
# СПИСОК БАНІВ
# =========================

@router.message(F.text == "/bans")
async def show_bans(
    message: Message
):

    if message.from_user.id != 1561352771:
        return

    if not banned_users:

        await message.answer(
            "✅ Список банів порожній"
        )

        return

    text = "🚫 СПИСОК ЗАБАНЕНИХ\n\n"

    for user_id, reason in banned_users.items():

        text += (
            f"👤 ID: {user_id}\n"
            f"📌 Причина: {reason}\n"
            f"🔓 /unban_{user_id}\n\n"
        )

    await message.answer(text)

# =========================
# РОЗБАН
# =========================

@router.message(F.text.startswith("/unban_"))
async def unban_user(
    message: Message
):

    if message.from_user.id != 1561352771:
        return

    try:

        user_id = int(
            message.text.replace(
                "/unban_",
                ""
            )
        )

    except:

        await message.answer(
            "❌ Невірний ID"
        )

        return

    if user_id not in banned_users:

        await message.answer(
            "❌ Користувач не забанений"
        )

        return

    del banned_users[user_id]

    await message.answer(
        f"✅ Користувача {user_id} розбанено"
    )

    try:

        await message.bot.send_message(
            user_id,
            "✅ Вас розбанено"
        )

    except:
        pass