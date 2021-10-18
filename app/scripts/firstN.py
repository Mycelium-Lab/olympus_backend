from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from datetime import datetime

transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/deltax2016/olympus-wallets")
client = Client(transport=transport, fetch_schema_from_transport=True)

async def getFirstWallets(timestamp_start, period, cnt=None):
    
    day_start = datetime.fromtimestamp(timestamp_start).timetuple().tm_yday
    timestamp_end = timestamp_start + 86400*period

    queryString = f"""query balancesByWallet {{
        wallets(first:1000,orderBy: birth, first: {cnt}) {{
            id
            dailyBalance(orderBy: timestamp, first: 1000) {{
                ohmBalance
                day
            }}
        }}
    }}
    """
    # balance before listing
    

    query = gql(queryString)

    result = await client.execute_async(query)
    
    days = {}

    for res in result['wallets']:
        for day in res['dailyBalance']:
            if (int(day['day']) >= day_start and int(day['day']) <= (day_start+period)):
                if not (int(day['day']) in days):
                    days[int(day['day'])] = {}
                    days[int(day['day'])]['timestamp'] = 1609459200 + 86400*int(day['day'])
                    days[int(day['day'])]['balance'] = int(day['ohmBalance']) / 1000000000
                else:
                    days[int(day['day'])]['timestamp'] = 1609459200 + 86400*int(day['day'])
                    temp = days[int(day['day'])]['balance']
                    temp += (int(day['ohmBalance'])/ 1000000000)
                    days[int(day['day'])]['balance'] = temp

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


    return days_array[real_day:real_day+period]

N = 10
timestamp_start = 1617291702
days = 15
#wallet = "0x0822f3c03dcc24d200aff33493dc08d0e1f274a2"
res = getFirstWallets(timestamp_start, days, N)

print(res)






