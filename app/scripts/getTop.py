from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from datetime import datetime
import requests

transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/deltax2016/olympus-wallets")
client = Client(transport=transport, fetch_schema_from_transport=True)

async def getTopBalances(timestamp_start, period, balance_gt):

    balance_gt = balance_gt*1000000000
    day_start = datetime.fromtimestamp(timestamp_start).timetuple().tm_yday - 3
    timestamp_end = timestamp_start + 86400*period
    ts_array = []

    queryString = "query getTopBalances {"
    for i in range(day_start, day_start+period+2):
        queryString +=  f"""t{i}:dailyBalances(first:1000,orderBy: timestamp, where: {{day_gt:{i},day_lt:{i+2},address_not_in:["0xfd31c7d00ca47653c6ce64af53c1571f9c36566a","0x0822f3c03dcc24d200aff33493dc08d0e1f274a2", "0xbe731507810c8747c3e01e62c676b1ca6f93242f","0x245cc372c84b3645bf0ffe6538620b04a217988b"]}}) {{
                ohmBalance
                address
                day
            }}"""
    queryString += '}'
    
    request = requests.post('https://api.thegraph.com/subgraphs/name/deltax2016/olympus-wallets', json={'query': queryString})
    result = request.json()
    
    days = {}

    for res in result['data']:
        for day in result['data'][str(res)]:
            if not (int(day['day']) in days):
                if int(day['ohmBalance']) >= balance_gt:
                    days[int(day['day'])] = {}
                    days[int(day['day'])]['timestamp'] = 1609459200 + 86400*int(day['day'])
                    days[int(day['day'])]['balance'] = int(day['ohmBalance']) / 1000000000
                    days[int(day['day'])]['holders'] = 1
            else:
                if int(day['ohmBalance']) >= balance_gt:
                    days[int(day['day'])]['timestamp'] = 1609459200 + 86400*int(day['day'])
                    temp = days[int(day['day'])]['balance']
                    temp += (int(day['ohmBalance'])/ 1000000000)
                    days[int(day['day'])]['balance'] = temp
                    days[int(day['day'])]['holders'] +=1

    days_array = []
    real_day = datetime.fromtimestamp(int(timestamp_start)).timetuple().tm_yday
    for i in range(0, real_day+period):
        if i in days:
            days_array.append(days[i])
        else:
            tempDay = {}
            tempDay['timestamp'] = 1609459200 + 86400*int(i)
            if i!= 0:
                tempDay['balance'] = days_array[i-1]['balance']
            else:
                tempDay['balance'] = "0"
            days_array.append(tempDay)


    return days_array[real_day-1:real_day+period]

timestamp_start = 1617291702
days = 10
amount = 10000
res = getTopBalances(timestamp_start, days, amount)

print(res)





