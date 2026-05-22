from aiogram.fsm.state import State, StatesGroup

class AdForm(StatesGroup):

    category = State()
    ad_type = State()
    city = State()
    title = State()
    price = State()
    description = State()
    contact = State()
    photo = State()