from fastapi import FastAPI, APIRouter
from notifications.bot import unstake, transfer, minter, transfer_dao, change_role, activate_role, reserves, mint
from pydantic import BaseModel

router = APIRouter()

@router.get("/unstake")
async def handle_unstake(amount: float = 100.0, to: str = "",id: str =""):
    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()

    if float(fake_db['unstake']) <= amount and int(fake_db['states']['unstake']):
        await unstake(amount,to,id)
    return "ok"

@router.get("/transfer")
async def handle_transfer(amount: float = 100.0, to: str = "", tx: str = "", froms: str = ""):
    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()

    if float(fake_db['transfer']) <= amount and int(fake_db['states']['transfer']):
        await transfer(amount,froms,to,tx)
    return "ok"

@router.get("/change_role")
async def handle_change(role: str = "", address: str = ""):

    if int(fake_db['states']['change_role']):
        await change_role(role,address)
    return "ok"

@router.get("/reserves_managed")
async def handle_reserves(token: str = "", amount: float = ""):
    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()
    index = f"reserves_{token.lower()}"
    if loat(fake_db[index]) <= amount and int(fake_db['states']['treasury_balance']):
        await reserves(amount,token)

    return "ok"

@router.get("/activate_role")
async def handle_activate(role: str = "", address: str = "", activated: str = ""):
    if int(fake_db['states']['change_role']):
        await activate_role(role,address,activated)
    return "ok"

@router.get("/transfer_dao")
async def handle_transfer_dao(amount: float = 100.0, to: str = "", tx: str = "",froms: str = ""):
    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()
    
    if float(fake_db['dao_transfer']) <= amount and int(fake_db['states']['dao_transfer']):
        await transfer_dao(amount,froms, to,tx)
    return "ok"

@router.get("/mint")
async def handle_mint(amount: float = 100.0, to: str = "", tx: str = ""):
    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()

    if float(fake_db['mint']) <= amount and int(fake_db['states']['minting']):
        await mint(amount, to,tx)
    return "ok"

@router.get("/minter")
async def handle_transfer(address: str):
    if int(fake_db['states']['minter_role']):
        await minter(address)
    return "ok"



