from fastapi import FastAPI
from aiogram import types, Dispatcher, Bot
from bot import dp, bot, TOKEN, unstake, transfer, minter
from pydantic import BaseModel

class Item(BaseModel):
    amount: int


app = FastAPI()
WEBHOOK_PATH = f"/bot/{TOKEN}"
WEBHOOK_URL = "https://84ea-95-143-218-167.ngrok.io" + WEBHOOK_PATH


@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )

@app.get("/unstake")
async def handle_unstake(amount: int = 100, to: str = ""):
    await unstake(amount,to)
    return "ok"

@app.get("/transfer")
async def handle_transfer(amount: int = 100):
    await transfer(amount)
    return "ok"

@app.get("/minter")
async def handle_transfer(address: str):
    await minter(address)
    return "ok"

@app.post("/change_unstake")
async def handle_change_unstake(item: Item):
    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()

    fake_db["unstake"] = item.amount

    f = open("notifications.txt",'w')
    f.write(str(fake_db))
    f.close()

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