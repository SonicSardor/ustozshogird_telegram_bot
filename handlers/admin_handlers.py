from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery

from config import ADMINS_LIST, CHANNEL_ID

admin = Router()
ADMINS = ADMINS_LIST
channel_id = CHANNEL_ID


@admin.callback_query(F.from_user.id.in_(ADMINS))
async def start(callback: CallbackQuery, bot: Bot):
    await bot.copy_message(channel_id, callback.from_user.id, int(callback.message.message_id))
    await bot.send_message(callback.from_user.id, 'done', reply_to_message_id=callback.message.message_id)
