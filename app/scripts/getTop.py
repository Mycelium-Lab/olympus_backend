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
        queryString +=  f"""t{i}:dailyBalances(first:1000,orderBy: timestamp, where: {{ohmBalance_gt: "{balance_gt}", day_gt:{i},day_lt:{i+2},address_not:"0xFd31c7d00Ca47653c6Ce64Af53c1571f9C36566a"}}) {{
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
                days[int(day['day'])] = {}
                days[int(day['day'])]['timestamp'] = 1609459200 + 86400*int(day['day'])
                days[int(day['day'])]['balance'] = int(day['ohmBalance']) / 1000000000
                days[int(day['day'])]['holders'] = 1
            else:
                days[int(day['day'])]['timestamp'] = 1609459200 + 86400*int(day['day'])
                temp = days[int(day['day'])]['balance']
                temp += (int(day['ohmBalance'])/ 1000000000)
                days[int(day['day'])]['balance'] = temp
                days[int(day['day'])]['holders'] +=1

    days_array = []
    real_day = datetime.fromtimestamp(int(timestamp_start)).timetuple().tm_yday
    for i in range(0, real_day+period+2):
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


    return days_array[real_day-1:real_day+period+2]

timestamp_start = 1617291702
days = 10
amount = 10000
res = getTopBalances(timestamp_start, days, amount)

print(res)





