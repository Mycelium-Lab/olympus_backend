import json
import requests
import threading
import time

StartTime=time.time()

AMOUNT_MIN = 1
INTERVAL_IN_SECONDS = 40

class setInterval :
    def __init__(self,interval,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()):
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stopEvent.set()


def getTransfers(amount, timestamp):
    query = """
    {
      t1:transfers(orderBy:timestamp, orderDirection:desc, where:{amount_gte: %d, timestamp_gte:%d}){
        id
        from
        to
        amount
        timestamp
      }""" % (amount, timestamp)

    query += """t2:transfers(orderBy:timestamp, orderDirection:desc, where:{timestamp_gte:%d, from:"0x245cc372C84B3645Bf0Ffe6538620B04a217988B", amount_gte:%d}){
        id
        from
        to
        amount
        timestamp
      }
    }
    """ % (amount, timestamp)
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
    dao_data = getTransfers(AMOUNT_MIN, timestamp)
    transfers_data = dao_data['data']['t1']
    dao_data = dao_data['data']['t2']

    print(timestamp)
    if transfers_data:
        print(transfers_data[0]['amount'])
        for i in transfers_data:
            requests.get(f"https://977c-62-84-119-83.ngrok.io/transfer?amount={i['amount']}&to={i['to']}&froms={i['from']}&tx={i['id']}")
    if dao_data:
        print(dao_data[0]['amount'])
        for i in dao_data:
            requests.get(f"https://977c-62-84-119-83.ngrok.io/transfer?amount={i['amount']}&to={i['to']}&froms={i['from']}&tx={i['id']}")


if __name__== "__main__":
    action()
    inter = setInterval(INTERVAL_IN_SECONDS, action)