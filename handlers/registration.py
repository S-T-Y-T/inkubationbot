from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.user_state import RegisterState
from keyboards.reply import phone_kb, university_kb, cards_kb
from config import ADMIN_GROUP_ID, FDTU_GROUP_LINK, PAID_GROUP_LINK, CARDS
from aiogram.types import CallbackQuery
from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.reply import cards_kb
from config import CARDS

router = Router()


@router.message(RegisterState.full_name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Telefon raqamingizni yuboring:", reply_markup=phone_kb())
    await state.set_state(RegisterState.phone)

@router.message(RegisterState.phone, F.contact)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await message.answer("Telegram username kiriting:")
    await state.set_state(RegisterState.username)

@router.message(RegisterState.username)
async def get_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("O‘qish joyingizni tanlang:", reply_markup=university_kb())
    await state.set_state(RegisterState.university)

@router.message(RegisterState.university, F.text == "Farg'ona davlat texnika universiteti")
async def fdtu_handler(message: Message, state: FSMContext):
    await state.update_data(university="FDTU")
    await message.answer("Fakultetingizni kiriting:")
    await state.set_state(RegisterState.faculty)

@router.message(RegisterState.faculty)
async def get_faculty(message: Message, state: FSMContext):
    await state.update_data(faculty=message.text)
    await message.answer("Guruhingizni kiriting:")
    await state.set_state(RegisterState.group)

@router.message(RegisterState.group)
async def get_group(message: Message, state: FSMContext, bot):
    data = await state.get_data()
    await state.update_data(group=message.text)

    text = f"""
📥 Yangi foydalanuvchi:

👤 {data['full_name']}
📱 {data['phone']}
🔗 {data['username']}
🏫 FDTU
📚 {data['faculty']}
👥 {message.text}
"""

    await bot.send_message(ADMIN_GROUP_ID, text)
    await message.answer(f"Guruhga qo‘shilish uchun:\n{FDTU_GROUP_LINK}")
    await state.clear()

# ======= BOSHQA =======

@router.message(RegisterState.university, F.text == "Boshqa")
async def other_uni(message: Message, state: FSMContext):
    await message.answer("O‘qish joyingizni yozing:")
    await state.set_state(RegisterState.other_university)

@router.message(RegisterState.other_university)
async def get_other_uni(message: Message, state: FSMContext):
    await state.update_data(university=message.text)

    await message.answer(
        "Akseleratsiya va inkubatsiya jarayonida qatnashish uchun 500 000 so'm to'lovni amalga oshiring.\n\n"
        "Chek yuboring:",
        reply_markup=cards_kb(CARDS)
    )

    await state.set_state(RegisterState.payment_screenshot)

@router.message(RegisterState.payment_screenshot, F.photo)
async def get_payment(message: Message, state: FSMContext, bot):
    data = await state.get_data()

    caption = f"""
💰 TO‘LOV:

👤 {data['full_name']}
📱 {data['phone']}
🔗 {data['username']}
🏫 {data['university']}
"""

    await bot.send_photo(
        ADMIN_GROUP_ID,
        photo=message.photo[-1].file_id,
        caption=caption
    )

    await message.answer(f"Kanalga qo‘shilish uchun:\n{PAID_GROUP_LINK}")
    await state.clear()


