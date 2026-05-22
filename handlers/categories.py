from aiogram import Router
    await state.set_state(AdForm.contact)

    await message.answer('📞 Контакт')

@router.message(AdForm.contact)
async def contact(message: Message, state: FSMContext):

    await state.update_data(contact=message.text)

    await state.set_state(AdForm.photo)

    await message.answer('📸 Надішліть фото або -')

@router.message(AdForm.photo)
async def finish(message: Message, state: FSMContext):

    data = await state.get_data()

    post = f"""
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

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='✅ Опублікувати',
                    callback_data='publish'
                ),
                InlineKeyboardButton(
                    text='❌ Відхилити',
                    callback_data='decline'
                )
            ]
        ]
    )

    if message.photo:

        await message.bot.send_photo(
            ADMIN_ID,
            photo=message.photo[-1].file_id,
            caption=post,
            reply_markup=keyboard
        )

    else:

        await message.bot.send_message(
            ADMIN_ID,
            post,
            reply_markup=keyboard
        )

    await message.answer(
        '✅ Оголошення відправлено на модерацію'
    )

    await state.clear()