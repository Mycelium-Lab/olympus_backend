import json
import requests
import threading
import time

StartTime=time.time()

INTERVAL_IN_SECONDS = 60

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


def getMinterChanges(timestamp):
    query = """
    {
      minters(where:{timestamp_gt: %d}) {
        id
        address
      }
    }
    """ % (timestamp)
    try:
        request = requests.post('https://api.thegraph.com/subgraphs/name/deltax2016/olympus-wallets', json={'query': query})
        request.raise_for_status()
        return request.json()
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
        return {'data':{'transfers':[]}}
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        return {'data':{'transfers':[]}}
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        return {'data':{'transfers':[]}}
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt) 
        return {'data':{'transfers':[]}}

def action():
    timestamp = time.time() - INTERVAL_IN_SECONDS - 20
    transfers_data = getMinterChanges(timestamp)
    transfers_data = transfers_data['data']['minters']
    
    if transfers_data:
        print(transfers_data[0]['address'])
        for i in transfers_data:
            requests.get(f"https://977c-62-84-119-83.ngrok.io/minter?address={i['address']}")



if __name__== "__main__":
    action()
    inter = setInterval(INTERVAL_IN_SECONDS, action)
