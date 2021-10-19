from fastapi import FastAPI
from aiogram import types, Dispatcher, Bot
from notifications.bot import dp, bot, TOKEN, unstake, transfer, minter, change_unstake, change_dao, change_transfer, transfer_dao
from pydantic import BaseModel
from app.scripts.getTop import getTopBalances
from app.scripts.getBalance import getBalances
from app.scripts.firstN import getFirstWallets
from app.scripts.getTotal import totalWallets, totalBalances
from fastapi.middleware.cors import CORSMiddleware
from app.scripts.transfer import getTransfer
from app.scripts.transfer_to import getTransferTo
from pydantic import BaseModel

class Item(BaseModel):
    amount: int = 1

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


WEBHOOK_PATH = f"/bot/{TOKEN}"
WEBHOOK_URL = "https://977c-62-84-119-83.ngrok.io" + WEBHOOK_PATH


@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )

@app.get("/unstake")
async def handle_unstake(amount: float = 100.0, to: str = "",id: str =""):
    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()

    if float(fake_db['unstake']) <= amount:
        await unstake(amount,to,id)
    return "ok"

@app.get("/transfer")
async def handle_transfer(amount: float = 100.0, to: str = "", tx: str = "", froms: str = ""):
    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()

    if float(fake_db['transfer']) <= amount:
        await transfer(amount,froms,to,tx)
    return "ok"

@app.get("/transfer_dao")
async def handle_transfer_dao(amount: float = 100.0, to: str = "", tx: str = "",froms: str = ""):
    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()

    if float(fake_db['dao_transfer']) <= amount:
        await transfer_dao(amount,froms, to,tx)
    return "ok"

@app.get("/minter")
async def handle_transfer(address: str):
    await minter(address)
    return "ok"

@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)

@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()

@app.post("/api/change_unstake")
async def handle_change_unstake(item: Item):

    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()

    fake_db["unstake"] = item.amount

    f = open("notifications.txt",'w')
    f.write(str(fake_db))
    f.close()
    await change_unstake(item.amount)

    return {"data":fake_db}

@app.post("/api/change_dao_transfer")
async def handle_change_dao(item: Item):

    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()

    fake_db["dao_transfer"] = item.amount

    f = open("notifications.txt",'w')
    f.write(str(fake_db))
    f.close()
    await change_dao(item.amount)

    return {"data":fake_db}

@app.post("/api/change_large_transfer")
async def handle_change_transfer(item: Item):

    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()

    fake_db["transfer"] = item.amount

    f = open("notifications.txt",'w')
    f.write(str(fake_db))
    f.close()

    await change_transfer(item.amount)

    return {"data":fake_db}

@app.get("/api/notifications_states")
async def states():
    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()

    return {"data":fake_db}


@app.get("/api/get_top_days/")
async def get_top_days(start: int = 1617291702, days: int = 1, amount: int = 10000):

    response  = await getTopBalances(start, days, amount)
    return {"data":response}

@app.get("/api/get_transfer_from/")
async def get_transfer_from(start: int = 1617291702, days: int = 1):

    response  = await getTransfer(start, days)
    return {"data":response}

@app.get("/api/get_transfer_to/")
async def get_transfer_to(start: int = 1617291702, days: int = 1):

    response  = await getTransferTo(start, days)
    return {"data":response}


@app.get("/api/get_dao_days/")
async def get_dao_days(start: int = 1617291702, days: int = 1):
    wallet = "0x245cc372C84B3645Bf0Ffe6538620B04a217988B"
    response  = await getBalances(start, days, wallet)
    return {"data":response}

@app.get("/api/get_total_wallets/")
async def get_total_wallets(start: int = 1617291702, days: int = 1):
    response  = await totalWallets(start, days)
    return {"data":response}

@app.get("/api/get_total_balances/")
async def get_total_balances(start: int = 1617291702, days: int = 1):
    response  = await totalBalances(start, days)
    return {"data":response}

@app.get("/api/get_first_n/")
async def get_first_n(start: int = 1617291702, days: int = 1, count: int = 1):
    response  = await getFirstWallets(start, days, count)
    return {"data":response}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)