from fastapi import FastAPI
from app.scripts.getTop import getTopBalances
from app.scripts.getBalance import getBalances
from app.scripts.firstN import getFirstWallets
from app.scripts.getTotal import totalWallets, totalBalances
from fastapi.middleware.cors import CORSMiddleware
from app.scripts.transfer import getTransfer
from app.scripts.transfer_to import getTransferTo

app = FastAPI()

origins = [
    "https://modest-bartik-cbbabe.netlify.app",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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