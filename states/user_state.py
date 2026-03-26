from aiogram.fsm.state import StatesGroup, State

class RegisterState(StatesGroup):
    full_name = State()
    phone = State()
    username = State()
    university = State()
    faculty = State()
    group = State()
    other_university = State()
    payment_screenshot = State()