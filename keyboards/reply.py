from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    CopyTextButton
)
from config import CARDS
from aiogram import Router, F

router = Router()

def phone_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Raqam yuborish", request_contact=True)]],
        resize_keyboard=True
    )

def university_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Farg'ona davlat texnika universiteti")],
            [KeyboardButton(text="Boshqa")]
        ],
        resize_keyboard=True
    )



def cards_kb(cards: list):
    keyboard = []

    for card in cards:
        keyboard.append([
            InlineKeyboardButton(
                text=f"💳 {card['number']} — {card['owner']}",  # показываем владельца
                copy_text=CopyTextButton(text=card['number'])  # копируется только номер
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Использование при отправке сообщения
async def send_payment_message(message):
    await message.answer(
        "Akseleratsiya va inkubatsiya jarayonida qatnashish uchun 500 000 so'm to'lovni amalga oshiring.\n\n"
        "Kartani tanlang (bosganda nusxa olinadi):",
        reply_markup=cards_kb(CARDS)
    )


def subscribe_kb(channels: list):
    keyboard = []

    for ch in channels:
        keyboard.append([
            InlineKeyboardButton(
                text=f"📢 {ch}",
                url=f"https://t.me/{ch.replace('@', '')}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            text="✅ Tekshirish",
            callback_data="check_sub"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)