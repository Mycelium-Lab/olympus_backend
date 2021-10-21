from web3 import Web3
from threading import Thread
import time
import requests
import asyncio

def getTokenName(token):
    if token == "0x6B175474E89094C44Da98b954EedeAC495271d0F".lower() or token == "0x6B175474E89094C44Da98b954EedeAC495271d0F":
        return "DAI"
    elif token == "0x853d955aCEf822Db058eb8505911ED77F175b99e".lower() or token == "0x853d955aCEf822Db058eb8505911ED77F175b99e":
        return "FRAX"
    elif token == "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2".lower() or token == "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2":
        return "wETH"
    elif token == "0x5f98805A4E8be255a32880FDeC7F6728C6568bA0".lower() or token == "0x5f98805A4E8be255a32880FDeC7F6728C6568bA0":
        return "LUSD"
    else:
        return str(token)


def handle_event(event):
    if event['event'] == "Transfer":
        i = event['args']
        tx = event['transactionHash'].hex()
        amount = float(float(i['value'])/1000000000)
        print(amount)
        if (i['from'] == "0x245cc372C84B3645Bf0Ffe6538620B04a217988B"):
            requests.get(f"https://977c-62-84-119-83.ngrok.io/transfer_dao?amount={amount}&to={i['to']}&froms={i['from']}&tx={tx}")
        elif (i['from'] == "0xfd31c7d00ca47653c6ce64af53c1571f9c36566a") or (i['from'] == "0xFd31c7d00Ca47653c6Ce64Af53c1571f9C36566a"):
            requests.get(f"https://977c-62-84-119-83.ngrok.io/unstake?amount={amount}&to={i['to']}&id={tx}")
        else:
            requests.get(f"https://977c-62-84-119-83.ngrok.io/transfer?amount={amount}&to={i['to']}&froms={i['from']}&tx={tx}")
    elif event['event']=="ChangeQueued":
        role = ""
        if event['args']['managing']==0:
            role = "RESERVEDEPOSITOR"
            print("RESERVEDEPOSITOR "+event['args']['queued'])
        elif event['args']['managing']==1:
            role = "RESERVESPENDER"
            print("RESERVESPENDER "+event['args']['queued'])
        elif event['args']['managing']==2:
            role = "RESERVETOKEN"
            print("RESERVETOKEN "+event['args']['queued'])
        elif event['args']['managing']==3:
            role = "RESERVEMANAGER"
            print("RESERVEMANAGER "+event['args']['queued'])
        elif event['args']['managing']==4:
            role = "LIQUIDITYDEPOSITOR"
            print("LIQUIDITYDEPOSITOR "+event['args']['queued'])
        elif event['args']['managing']==5:
            role = "LIQUIDITYTOKEN"
            print("LIQUIDITYTOKEN "+event['args']['queued'])
        elif event['args']['managing']==6:
            role = "LIQUIDITYMANAGER"
            print("LIQUIDITYMANAGER "+event['args']['queued'])
        elif event['args']['managing']==7:
            role = "DEBTOR"
            print("DEBTOR "+event['args']['queued'])
        elif event['args']['managing']==8:
            role = "REWARDMANAGER"
            print("REWARDMANAGER "+event['args']['queued'])
        elif event['args']['managing']==9:
            role = "SOHM"
            print("SOHM "+event['args']['queued'])
        requests.get(f"https://977c-62-84-119-83.ngrok.io/change_role?role={role}&address={event['args']['queued'].hex()}")
    elif event['event']=="ChangeActivated":
        role = ""
        if event['args']['managing']==0:
            role = "RESERVEDEPOSITOR"
            print("RESERVEDEPOSITOR "+event['args']['activated']+" "+str(event['args']['result']))
        elif event['args']['managing']==1:
            role = "RESERVESPENDER"
            print("RESERVESPENDER "+event['args']['activated']+" "+str(event['args']['result']))
        elif event['args']['managing']==2:
            role = "RESERVETOKEN"
            print("RESERVETOKEN "+event['args']['activated']+" "+str(event['args']['result']))
        elif event['args']['managing']==3:
            role = "RESERVEMANAGER"
            print("RESERVEMANAGER "+event['args']['activated']+" "+str(event['args']['result']))
        elif event['args']['managing']==4:
            role = "LIQUIDITYDEPOSITOR"
            print("LIQUIDITYDEPOSITOR "+event['args']['activated']+" "+str(event['args']['result']))
        elif event['args']['managing']==5:
            role = "LIQUIDITYTOKEN"
            print("LIQUIDITYTOKEN "+event['args']['activated']+" "+str(event['args']['result']))
        elif event['args']['managing']==6:
            role = "LIQUIDITYMANAGER"
            print("LIQUIDITYMANAGER "+event['args']['activated']+" "+str(event['args']['result']))
        elif event['args']['managing']==7:
            role = "DEBTOR"
            print("DEBTOR "+event['args']['activated'])
        elif event['args']['managing']==8:
            role = "REWARDMANAGER"
            print("REWARDMANAGER "+event['args']['activated']+" "+str(event['args']['result']))
        elif event['args']['managing']==9:
            role = "SOHM"
            print("SOHM "+event['args']['activated']+" "+str(event['args']['result']))
        requests.get(f"https://977c-62-84-119-83.ngrok.io/activate_role?role={role}&address={event['args']['activated'].hex()}&activated={str(event['args']['result'])}")
    elif event['event']=="ReservesManaged":
        print("ReservesManaged "+str(event['args']['amount']*(10**-18))+" "+(event['args']['token']))
        token = getTokenName(event['args']['token'])
        requests.get(f"https://977c-62-84-119-83.ngrok.io/reserves_managed?amount={event['args']['amount']*(10**-18)}&token={token}")
    else:
        print(event)



def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        time.sleep(poll_interval)

def main():
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/f050447a7af0410cad5d685137851dba'))
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
        time.sleep(10)


if __name__ == '__main__':
    main()