from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from datetime import datetime

transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/id/QmThQWLEohGNnWzKpozLxdDq5XHpWupyrJixWACbKSVMPM")
client = Client(transport=transport, fetch_schema_from_transport=True)

async def getFirstWallets(timestamp_start, period, cnt=None):
    
    day_start = datetime.fromtimestamp(timestamp_start).timetuple().tm_yday
    timestamp_end = timestamp_start + 86400*period

    queryString = f"""query balancesByWallet {{
        wallets(orderBy: birth, first: {cnt}) {{ 
            id
            dailyBalance(orderBy: timestamp) {{
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
                if not (str(day['day']) in days):
                    days[str(day['day'])] = {}
                    days[str(day['day'])]['timestamp'] = 1609459200 + 86400*int(day['day'])
                    days[str(day['day'])]['balance'] = int(day['ohmBalance']) / 1000000000
                else:
                    days[str(day['day'])]['timestamp'] = 1609459200 + 86400*int(day['day'])
                    temp = days[str(day['day'])]['balance']
                    temp += (int(day['ohmBalance'])/ 1000000000)
                    days[str(day['day'])]['balance'] = temp

    days_array = []
    for i in days:
        days_array.append(days[i])

    return days_array

N = 10
timestamp_start = 1617291702
days = 15
#wallet = "0x0822f3c03dcc24d200aff33493dc08d0e1f274a2"
res = getFirstWallets(timestamp_start, days, N)

print(res)






