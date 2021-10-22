from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from notifications.bot import dp, bot, TOKEN, change_unstake, change_dao, change_transfer, transfer_dao, change_reserves, change_mint

router = APIRouter()

class Item(BaseModel):
    amount: int = 1

class Amounts(BaseModel):
    amount_dai: int = -1
    amount_frax: int = -1
    amount_weth: int = -1
    amount_lusd: int = -1

class Roles(BaseModel):
	RESERVEDEPOSITOR:int = 2,
	RESERVESPENDER:int = 2,
	RESERVETOKEN:int = 2,
	RESERVEMANAGER:int = 2,
	LIQUIDITYDEPOSITOR:int = 2,
	LIQUIDITYTOKEN:int = 1,
	LIQUIDITYMANAGER:int = 1,
	DEBTOR:int = 1,
	REWARDMANAGER:int = 1,
	SOHM:int = 1


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

    if item.amount_dai != -1:
    	fake_db["reserves_dai"] = item.amount_dai
    if item.amount_frax != -1:
    	fake_db["reserves_frax"] = item.amount_frax
    if item.amount_lusd != -1:
    	fake_db["reserves_lusd"] = item.amount_lusd
    if item.amount_weth != -1:
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

'''
'change_queued':{
		'RESERVEDEPOSITOR':1,
		'RESERVESPENDER':1,
		'RESERVETOKEN':1,
		'RESERVEMANAGER':1,
		'LIQUIDITYDEPOSITOR':1,
		'LIQUIDITYTOKEN':1,
		'LIQUIDITYMANAGER':1,
		'DEBTOR':1,
		'REWARDMANAGER':1,
		'SOHM':1
	}
	'change_activated':{
		'RESERVEDEPOSITOR':1,
		'RESERVESPENDER':1,
		'RESERVETOKEN':1,
		'RESERVEMANAGER':1,
		'LIQUIDITYDEPOSITOR':1,
		'LIQUIDITYTOKEN':1,
		'LIQUIDITYMANAGER':1,
		'DEBTOR':1,
		'REWARDMANAGER':1,
		'SOHM':1
	}
'''