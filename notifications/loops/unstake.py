import json
import requests
import threading
import time
import requests

StartTime=time.time()

AMOUNT_MIN = 1
INTERVAL_IN_SECONDS = 30

class setInterval :
    def __init__(self,interval,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stopEvent.set()


def getUnstakes(amount, timestamp):
    query = """
    {
        unstakes(orderBy:timestamp orderDirection: desc, where:{amount_gte:%d, timestamp_gte:%d}){
          id
          amount
          timestamp
          transaction{from to blockHash}
        }
    }
    """ % (amount, timestamp)
    request = requests.post('https://api.thegraph.com/subgraphs/name/drondin/olympus-graph', json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        return {'data':{'unstakes':[]}}

def action():
    timestamp = time.time() - INTERVAL_IN_SECONDS - 20
    unstakes_data = getUnstakes(AMOUNT_MIN, timestamp)
    unstakes_data = unstakes_data['data']['unstakes']
    print(timestamp)
    if unstakes_data:
        print(unstakes_data[0]['amount'])
        for unst in unstakes_data:
            requests.get(f"https://977c-62-84-119-83.ngrok.io/unstake?amount={unst['amount']}&to={unst['transaction']['from']}&id={unst['transaction']['blockHash']}")

if __name__== "__main__":
    action()
    inter = setInterval(INTERVAL_IN_SECONDS, action)
