from fastapi import FastAPI
from aiogram import types, Dispatcher, Bot
from notifications.bot import dp, bot, TOKEN, change_unstake, change_dao, change_transfer, transfer_dao, change_reserves, change_mint
from pydantic import BaseModel
from app.scripts.getTop import getTopBalances
from app.scripts.getBalance import getBalances
from app.scripts.firstN import getFirstWallets, getFirstWalletsNDays, getFirstWalletsNHours, getFirstLegacy
from app.scripts.indexes import parseNDays, parseNHours, parseNMinutes
from app.scripts.general import parseGANDays, parseGANHours, parseGANMinutes
from app.scripts.rebases import rebaseTimestamps
from app.scripts.getTotal import totalWallets, totalBalances
from fastapi.middleware.cors import CORSMiddleware
from app.scripts.transfer import getTransfer
from app.scripts.transfer_to import getTransferTo
from app.task import log_loop
from pydantic import BaseModel
from app.routes import events
from app.routes import notifications
import requests
import asyncio
from web3 import Web3
from threading import Thread
import time

'''
class BackgroundRunner:

    async def main(self):
        w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/f7b4f0c651b84c2e93b45e1a398f4f6b'))
        abi = open("ohm.json").read()
        abi_tres = open("treasury.json").read()
        address = '0x383518188c0c6d7730d91b2c03a03c837814a899'
        contract_instance = w3.eth.contract(address=Web3.toChecksumAddress(address), abi=abi)
        transfer_filter = contract_instance.events.Transfer.createFilter(fromBlock=12525281)
        address_tres = '0x31F8Cc382c9898b273eff4e0b7626a6987C846E8'
        contract_tres = w3.eth.contract(address=address_tres, abi=abi_tres)
        change_queued_filter = contract_tres.events.ChangeQueued.createFilter(fromBlock=12525281) #12525281 for get_all_entries
        reserves_managed_filter = contract_tres.events.ReservesManaged.createFilter(fromBlock=12525281) #12525281
        #rewards_minted_filter = contract_tres.events.RewardsMinted.createFilter(fromBlock=12525281) #12525281
        change_activated_filter = contract_tres.events.ChangeActivated.createFilter(fromBlock=12525281) #12525281
        #deposit_filter = contract_tres.events.ReservesUpdated.createFilter(fromBlock=12525281) #12525281

        worker = [Thread(target=log_loop, args=(transfer_filter, 1), daemon=True),
        Thread(target=log_loop, args=(change_activated_filter, 1), daemon=True),
        Thread(target=log_loop, args=(change_queued_filter, 1), daemon=True),
        Thread(target=log_loop, args=(reserves_managed_filter, 1), daemon=True)]

        for item in worker:
            item.start()
       
        while True:
            time.sleep(20)


runner = BackgroundRunner()

'''

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
    #asyncio.create_task(runner.main())


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
async def get_indexes_n_days(start: int = 1617291702, end: int = 1636458860, n: int = 1):
    response  = await parseNDays(start, end, n)
    return {"data":response}

@app.get("/api/get_index_n_hours")
async def get_index_n_hours(start: int = 1623700800, end: int = 1623906000, n: int = 1):
    response  = await parseNHours(start, end, n)
    return {"data":response}

@app.get("/api/get_ga_n_minutes")
async def get_index_n_minutes(start: int = 1623702000, end: int = 1623907200, n: int = 1, types: str = 'marketCapacity'):
    response  = await parseGANMinutes(start, end, n, types)
    return {"data":response}

@app.get("/api/get_ga_n_days")
async def get_indexes_n_days(start: int = 1617291702, end: int = 1636458860, n: int = 1, types: str = 'marketCapacity'):
    response  = await parseGANDays(start, end, n, types)
    return {"data":response}

@app.get("/api/get_ga_n_hours")
async def get_index_n_hours(start: int = 1623700800, end: int = 1623906000, n: int = 1, types: str = 'marketCapacity'):
    response  = await parseGANHours(start, end, n, types)
    return {"data":response}

@app.get("/api/get_index_n_minutes")
async def get_index_n_minutes(start: int = 1623702000, end: int = 1623907200, n: int = 1):
    response  = await parseNMinutes(start, end, n)
    return {"data":response}

@app.get("/api/get_rebase_timestamps")
async def get_rebase_timestamps(start: int = 1617291702, end: int = 1636458860):
    response  = await rebaseTimestamps(start, end)
    return {"data":response}

@app.get("/api/get_first_n/")
async def get_first_n(start: int = 1617291702, days: int = 1, count: int = 1):
    response  = await getFirstLegacy(start, days, count)
    return {"data":response}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)

    #https://api.telegram.org/bot2006547998:AAFvcPVaPciAfCbjKQrFk2UwFsUkse_Yok8/setWebhook?url=https://535b-62-84-117-55.ngrok.io/