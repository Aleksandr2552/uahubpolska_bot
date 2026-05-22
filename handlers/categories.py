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
from aiogram.fsm.state import (
    State,
    StatesGroup
)

from states.forms import AdForm
from handlers.start import main_keyboard

router = Router()

# =========================
# FSM MODERATION
# =========================

class ModerationState(StatesGroup):

    reject_reason = State()

    ban_reason = State()

# =========================
# BANNED USERS
# =========================

banned_users = {}

# =========================
# CHOOSE TYPE KEYBOARD
# =========================

choose_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="🔎 Шукаю"
            ),

            KeyboardButton(
                text="✅ Пропоную"
            )
        ]
    ],
    resize_keyboard=True
)

# =========================
# CATEGORY SELECT
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
# CHOOSE TYPE
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
# CITY
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
# TITLE
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
# PRICE
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
# DESCRIPTION
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
# CONTACT
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
        "✅ Оголошення відправлено на модерацію",
        reply_markup=main_keyboard
    )

# =========================
# PUBLISH
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
# REJECT
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

    await message.bot.send_message(
        user_id,
        f"❌ Ваше оголошення відхилено\n\n📌 Причина:\n{message.text}"
    )

    await message.answer(
        "✅ Причину відправлено"
    )

    await state.clear()

# =========================
# BAN
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
        ban_user=user_id
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
# BANS LIST
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

    text = "🚫 СПИСОК БАНІВ\n\n"

    for user_id, reason in banned_users.items():

        text += (
            f"👤 {user_id}\n"
            f"📌 {reason}\n"
            f"🔓 /unban_{user_id}\n\n"
        )

    await message.answer(text)

# =========================
# UNBAN
# =========================

@router.message(F.text.startswith("/unban_"))
async def unban_user(
    message: Message
):

    if message.from_user.id != 1561352771:
        return

    user_id = int(
        message.text.replace(
            "/unban_",
            ""
        )
    )

    if user_id in banned_users:

        del banned_users[user_id]

        await message.answer(
            f"✅ {user_id} розбанено"
        )

        try:

            await message.bot.send_message(
                user_id,
                "✅ Вас розбанено"
            )

        except:
            pass