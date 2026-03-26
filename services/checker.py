from aiogram.client.bot import Bot

async def check_subscription(bot: Bot, user_id: int, channels: list) -> bool:
    """
    Проверяет, подписан ли пользователь на все каналы в списке.
    channels: список username каналов, например ["@fdt_tech", "@inkubatsiya"]
    """
    for ch in channels:
        try:
            member = await bot.get_chat_member(chat_id=ch, user_id=user_id)
            if member.status not in ["member", "creator", "administrator"]:
                return False
        except Exception:
            # если бот не видит пользователя или канал приватный → False
            return False
    return True