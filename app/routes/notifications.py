from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

router = APIRouter()

class Item(BaseModel):
    amount: int = 1

class Amounts(BaseModel):
    amount_dai: int = 1
    amount_frax: int = 1
    amount_weth: int = 1
    amount_lusd: int = 1

@router.post("/api/change_unstake")
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

@router.post("/api/change_mint")
async def handle_change_mint(item: Item):

    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()

    fake_db["mint"] = item.amount

    f = open("notifications.txt",'w')
    f.write(str(fake_db))
    f.close()
    await change_mint(item.amount)

    return {"data":fake_db}

@router.post("/api/change_reserves")
async def handle_change_unstake(item: Amounts):

    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()

    fake_db["reserves_dai"] = item.amount_dai
    fake_db["reserves_frax"] = item.amount_frax
    fake_db["reserves_lusd"] = item.amount_lusd
    fake_db["reserves_weth"] = item.amount_weth

    f = open("notifications.txt",'w')
    f.write(str(fake_db))
    f.close()
    await change_reserves(item.amount_dai, item.amount_frax, item.amount_lusd, item.amount_weth)

    return {"data":fake_db}

@router.post("/api/change_dao_transfer")
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

@router.post("/api/change_large_transfer")
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


@router.get("/api/notifications_states")
async def states():
    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()

    return {"data":fake_db}