from fastapi import FastAPI
from aiogram import types, Dispatcher, Bot
from notifications.bot import dp, bot, TOKEN, change_unstake, change_dao, change_transfer, transfer_dao, change_reserves, change_mint
from pydantic import BaseModel
from app.scripts.getTop import getTopBalances
from app.scripts.getBalance import getBalances
from app.scripts.firstN import getFirstWallets, getFirstWalletsNDays, getFirstWalletsNHours, getFirstLegacy
from app.scripts.indexes import parseNDays, parseNHours
from app.scripts.rebases import rebaseTimestamps
from app.scripts.getTotal import totalWallets, totalBalances
from fastapi.middleware.cors import CORSMiddleware
from app.scripts.transfer import getTransfer
from app.scripts.transfer_to import getTransferTo
from pydantic import BaseModel
from app.routes import events
from app.routes import notifications
import requests


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


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)

@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()


@app.get("/twitter/get_id")
async def get_user_id(usernames: str=""):
    headers = {"Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAAAMBVQEAAAAAM53SnmlTm5qvzqacgc2W0aPuyUQ%3D4VjOnXdLv99M3Jx3r6WZn3UtWoTr3CMLGQecA3Irt8sLlpGIkn"}
    response  = requests.get(f"https://api.twitter.com/2/users/by?usernames={usernames}", headers=headers).json()
    return response

@app.get("/twitter/get_tweets")
async def get_user_id(uid: str = ""):
    headers = {"Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAAAMBVQEAAAAAM53SnmlTm5qvzqacgc2W0aPuyUQ%3D4VjOnXdLv99M3Jx3r6WZn3UtWoTr3CMLGQecA3Irt8sLlpGIkn"}
    response  = requests.get(f"https://api.twitter.com/2/users/{uid}/tweets?max_results=25&expansions=author_id&user.fields=username,id,name,created_at,profile_image_url&tweet.fields=id,text,created_at", headers=headers).json()
    return response

app.include_router(events.router)
app.include_router(notifications.router)

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


# NEW CODE
@app.get("/api/get_index_n_days")
async def get_total_balances(start: int = 1617291702, days: int = 1, n: int = 1):
    response  = await parseNDays(start, days, n)
    return {"data":response}

@app.get("/api/get_index_n_hours")
async def get_total_balances(start: int = 1617291702, hours: int = 1, n: int = 1):
    response  = await parseNHours(start, hours, n)
    return {"data":response}

@app.get("/api/get_rebase_timestamps")
async def get_total_balances(start: int = 1617291702, timestamps: int = 1):
    response  = await rebaseTimestamps(start, timestamps)
    return {"data":response}

@app.get("/api/get_first_n/")
async def get_first_n(start: int = 1617291702, days: int = 1, count: int = 1):
    response  = await getFirstLegacy(start, days, count)
    return {"data":response}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)

    #https://api.telegram.org/bot2006547998:AAFvcPVaPciAfCbjKQrFk2UwFsUkse_Yok8/setWebhook?url=https://535b-62-84-117-55.ngrok.io/