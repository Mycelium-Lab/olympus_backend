from fastapi import FastAPI, APIRouter
from notifications.bot import dp, bot, TOKEN, unstake, transfer, minter, change_unstake, change_dao, change_transfer, transfer_dao
from pydantic import BaseModel

router = APIRouter()

@router.get("/unstake")
async def handle_unstake(amount: float = 100.0, to: str = "",id: str =""):
    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()

    if float(fake_db['unstake']) <= amount:
        await unstake(amount,to,id)
    return "ok"

@router.get("/transfer")
async def handle_transfer(amount: float = 100.0, to: str = "", tx: str = "", froms: str = ""):
    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()

    if float(fake_db['transfer']) <= amount:
        await transfer(amount,froms,to,tx)
    return "ok"

@router.get("/transfer_dao")
async def handle_transfer_dao(amount: float = 100.0, to: str = "", tx: str = "",froms: str = ""):
    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()

    if float(fake_db['dao_transfer']) <= amount:
        await transfer_dao(amount,froms, to,tx)
    return "ok"

@router.get("/minter")
async def handle_transfer(address: str):
    await minter(address)
    return "ok"



