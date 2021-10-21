from fastapi import FastAPI, APIRouter
from notifications.bot import unstake, transfer, minter, transfer_dao, change_role, activate_role
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

@router.get("/change_role")
async def handle_change(role: str = "", address: str = ""):
    await change_role(role,address)
    return "ok"

@router.get("/activate_role")
async def handle_activate(role: str = "", address: str = "", activated: str = ""):
    await activate_role(role,address,activated)
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



