from aiogram import Dispatcher, Bot, types

TOKEN = "2006547998:AAFvcPVaPciAfCbjKQrFk2UwFsUkse_Yok8"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    file_db = open('./notifications/fake_db.py')
    db = eval(file_db.read())
    file_db.close()
    db[message.from_user.id] = {"notifications": "all"}
    file_db = open('./notifications/fake_db.py','w')
    file_db.write(str(db))
    await message.answer(f"Notifications started")

@dp.message_handler(commands="stop")
async def stop(message: types.Message):
    file_db = open('./notifications/fake_db.py')
    db = eval(file_db.read())
    file_db.close()
    db[message.from_user.id] = {"notifications": "no"}
    file_db = open('./notifications/fake_db.py','w')
    file_db.write(str(db))
    await message.answer(f"Notifications stopped")

async def change_unstake(amount):
    file_db = open('./notifications/fake_db.py')
    db = eval(file_db.read())
    file_db.close()
    for i in db:
        await bot.send_message(i, f"Notifications set to Unstakes larger than {amount}")
    return "ok"

async def change_transfer(amount):
    file_db = open('./notifications/fake_db.py')
    db = eval(file_db.read())
    file_db.close()
    for i in db:
        await bot.send_message(i, f"Notifications set to Transfers larger than {amount}")
    return "ok"

async def change_dao(amount):
    file_db = open('./notifications/fake_db.py')
    db = eval(file_db.read())
    file_db.close()
    for i in db:
        await bot.send_message(i, f"Notifications set to DAO Transfers larger than {amount}")
    return "ok"

async def unstake(amount,to,tx):
    file_db = open('./notifications/fake_db.py')
    db = eval(file_db.read())
    file_db.close()
    for i in db:
        await bot.send_message(i, f'🟨 Warning: Big unstake {amount} OHM to <a href="https://ethplorer.io/ru/address/{to}">{to}</a> \n\nTransaction: <a href="https://ethplorer.io/ru/tx/{tx}">{tx}</a>', parse_mode="HTML")
    return "ok"

async def transfer(amount,froms,to,tx):
    file_db = open('./notifications/fake_db.py')
    db = eval(file_db.read())
    file_db.close()
    for i in db:
        await bot.send_message(i, f'🟦 Info: Big transfer {amount} OHM from <a href="https://ethplorer.io/ru/address/{froms}">{froms}</a> to <a href="https://ethplorer.io/ru/address/{to}">{to}</a> \n\nTransaction: <a href="https://ethplorer.io/ru/tx/{tx}">{tx}</a>', parse_mode="HTML")
    return "ok"

async def transfer_dao(amount,froms,to,tx):
    file_db = open('./notifications/fake_db.py')
    db = eval(file_db.read())
    file_db.close()
    for i in db:
        await bot.send_message(i, f'🟥 Danger: Big transfer {amount} OHM from DAO to <a href="https://ethplorer.io/ru/address/{to}">{to}</a> \n\nTransaction: <a href="https://ethplorer.io/ru/tx/{tx}">{tx}</a>', parse_mode="HTML")
    return "ok"

async def minter(address):
    file_db = open('./notifications/fake_db.py')
    db = eval(file_db.read())
    file_db.close()
    for i in db:
        await bot.send_message(i, f"🟥 MINTER CHANGED to {address}")
    return "ok"