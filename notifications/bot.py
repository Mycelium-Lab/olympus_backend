from aiogram import Dispatcher, Bot, types

TOKEN = "2006547998:AAFvcPVaPciAfCbjKQrFk2UwFsUkse_Yok8"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    file_db = open('fake_db.py')
    db = eval(file_db.read())
    file_db.close()
    db[message.from_user.id] = {"notifications": "all"}
    file_db = open('fake_db.py','w')
    file_db.write(str(db))
    await message.answer(f"Notifications started")

@dp.message_handler(commands="stop")
async def stop(message: types.Message):
    file_db = open('fake_db.py')
    db = eval(file_db.read())
    file_db.close()
    db[message.from_user.id] = {"notifications": "no"}
    file_db = open('fake_db.py','w')
    file_db.write(str(db))
    await message.answer(f"Notifications stopped")

async def unstake(amount,to):
    file_db = open('fake_db.py')
    db = eval(file_db.read())
    file_db.close()
    for i in db:
        await bot.send_message(i, f"🟨 Warning {amount} OHM to {to}")
    return "ok"

async def transfer(amount):
    file_db = open('fake_db.py')
    db = eval(file_db.read())
    file_db.close()
    for i in db:
        await bot.send_message(i, f"🟥 BIG TRANSFER {amount} OHM")
    return "ok"

async def minter(address):
    file_db = open('fake_db.py')
    db = eval(file_db.read())
    file_db.close()
    for i in db:
        await bot.send_message(i, f"🟥 MINTER CHANGED to  {address}")
    return "ok"