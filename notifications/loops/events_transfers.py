from web3 import Web3
from threading import Thread
import time
import asyncio

def handle_event(event):
    if(event['event']=="ChangeQueued"):
        if event['args']['managing']==0:
            print("RESERVEDEPOSITOR "+event['args']['queued'])
        elif event['args']['managing']==1:
            print("RESERVESPENDER "+event['args']['queued'])
        elif event['args']['managing']==2:
            print("RESERVETOKEN "+event['args']['queued'])
        elif event['args']['managing']==3:
            print("RESERVEMANAGER "+event['args']['queued'])
        elif event['args']['managing']==4:
            print("LIQUIDITYDEPOSITOR "+event['args']['queued'])
        elif event['args']['managing']==5:
            print("LIQUIDITYTOKEN "+event['args']['queued'])
        elif event['args']['managing']==6:
            print("LIQUIDITYMANAGER "+event['args']['queued'])
        elif event['args']['managing']==7:
            print("DEBTOR "+event['args']['queued'])
        elif event['args']['managing']==8:
            print("REWARDMANAGER "+event['args']['queued'])
        elif event['args']['managing']==9:
            print("SOHM "+event['args']['queued'])
    elif(event['event']=="ChangeActivated"):
        if event['args']['managing']==0:
            print("RESERVEDEPOSITOR "+event['args']['activated']+" "+str(event['args']['result']))
        elif event['args']['managing']==1:
            print("RESERVESPENDER "+event['args']['activated']+" "+str(event['args']['result']))
        elif event['args']['managing']==2:
            print("RESERVETOKEN "+event['args']['activated']+" "+str(event['args']['result']))
        elif event['args']['managing']==3:
            print("RESERVEMANAGER "+event['args']['activated']+" "+str(event['args']['result']))
        elif event['args']['managing']==4:
            print("LIQUIDITYDEPOSITOR "+event['args']['activated']+" "+str(event['args']['result']))
        elif event['args']['managing']==5:
            print("LIQUIDITYTOKEN "+event['args']['activated']+" "+str(event['args']['result']))
        elif event['args']['managing']==6:
            print("LIQUIDITYMANAGER "+event['args']['activated']+" "+str(event['args']['result']))
        elif event['args']['managing']==7:
            print("DEBTOR "+event['args']['activated'])
        elif event['args']['managing']==8:
            print("REWARDMANAGER "+event['args']['activated']+" "+str(event['args']['result']))
        elif event['args']['managing']==9:
            print("SOHM "+event['args']['activated']+" "+str(event['args']['result']))
    elif(event['event']=="ReservesManaged"):
        print("ReservesManaged "+str(event['args']['amount']*(10**-9))+" "+(event['args']['token']))
    else:
        print(event)



def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        time.sleep(poll_interval)

def main():
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/e51a791200b94e5e9fdcb8bc7a84e7c0'))
    abi = open("ohm.json").read()
    address = '0x383518188c0c6d7730d91b2c03a03c837814a899'
    contract_instance = w3.eth.contract(address=address, abi=abi)
    transfer_filter = contract_instance.events.Transfer.createFilter(fromBlock=12525281)
    worker = [Thread(target=log_loop, args=(transfer_filter, 1), daemon=True)]
    
    for item in worker:
        item.start()
   
    while True:
        time.sleep(10)



if __name__ == '__main__':
    main()