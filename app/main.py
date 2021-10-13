from fastapi import FastAPI
from app.scripts.getTop import getTopBalances
from app.scripts.getBalance import getBalances
from app.scripts.firstN import getFirstWallets

app = FastAPI()


@app.get("/api/get_top_days/")
async def get_top_days(start: int = 1617291702, days: int = 1, amount: int = 10000):

    response  = await getTopBalances(start, days, amount)
    return {"data":response}

@app.get("/api/get_dao_days/")
async def get_dao_days(start: int = 1617291702, days: int = 1):
    wallet = "0x245cc372C84B3645Bf0Ffe6538620B04a217988B"
    response  = await getBalances(start, days, wallet)
    return {"data":response}

@app.get("/api/get_first_n/")
async def get_first_n(start: int = 1617291702, days: int = 1, count: int = 1):
    response  = await getFirstWallets(start, days, count)
    return {"data":response}