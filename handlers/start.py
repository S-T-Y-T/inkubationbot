from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from services.checker import check_subscription
from states.user_state import RegisterState
from config import REQUIRED_CHANNELS  # <- берём из config.py

router = Router()

# ======== Кнопки для подписки ========
def subscribe_kb(channels: list) -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-кнопки для каждого канала и отдельную кнопку проверки подписки
    """
    buttons = []
    for ch in channels:
        # кнопка с переходом в канал
        buttons.append(
            [InlineKeyboardButton(text=f"📌 {ch}", url=f"https://t.me/{ch.strip('@')}")]
        )
    # кнопка проверки подписки
    buttons.append([InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# ======== /start ========
@router.message(F.text == "/start")
async def start_handler(message: Message, state: FSMContext):
    await message.answer(
        "Iltimos, quyidagi kanallarga obuna bo‘ling va keyin Tekshirish tugmasini bosing:",
        reply_markup=subscribe_kb(REQUIRED_CHANNELS)
    )

# ======== Проверка подписки ========
@router.callback_query(F.data == "check_sub")
async def check_sub_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    bot = callback.bot

    is_subscribed = await check_subscription(bot, user_id, REQUIRED_CHANNELS)

    if not is_subscribed:
        await callback.answer("❌ Siz hali ham obuna bo‘lmadingiz!", show_alert=True)
        return

    # Если подписан — переходим к регистрации
    await callback.message.answer(
        "✅ Rahmat! Endi ro‘yxatdan o‘ting.\n\nFamiliya Ism Sharifingizni kiriting:"
    )
    await state.set_state(RegisterState.full_name)
    await callback.answer()