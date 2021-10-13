from fastapi import FastAPI
from scripts.getTop import getTopBalances

app = FastAPI()


@app.get("/api/get_top")
async def get_top(start: int = 1609459200, days: int = 1, amount: int = 10000):

    response  = await getTopBalances(start, days, amount)
    return {"data":response}