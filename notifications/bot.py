from aiogram import Dispatcher, Bot, types

TOKEN = "2006547998:AAFvcPVaPciAfCbjKQrFk2UwFsUkse_Yok8"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer(f"Hello, {message.from_user.full_name}")