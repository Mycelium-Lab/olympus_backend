from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from datetime import datetime

transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/id/QmThQWLEohGNnWzKpozLxdDq5XHpWupyrJixWACbKSVMPM")
client = Client(transport=transport, fetch_schema_from_transport=True)

async def getTopBalances(timestamp_start, period, balance_gt):

    balance_gt = balance_gt*1000000000
    day_start = datetime.fromtimestamp(timestamp_start).timetuple().tm_yday
    timestamp_end = timestamp_start + 86400*period

    queryString = f"""query getTopBalances {{
        t1:dailyBalances(first:1000,orderBy: timestamp, where: {{ohmBalance_gt: "{balance_gt}", timestamp_gt: "{timestamp_start}", timestamp_lt: "{timestamp_end}"}}) {{
            ohmBalance
            address
            day
        }}
        t2:dailyBalances(first:1000, skip: 1000, orderBy: timestamp, where: {{ohmBalance_gt: "{balance_gt}", timestamp_gt: "{timestamp_start}", timestamp_lt: "{timestamp_end}"}}) {{
            ohmBalance
            address
            day
        }}
        t3:dailyBalances(first:1000, skip: 2000, orderBy: timestamp, where: {{ohmBalance_gt: "{balance_gt}", timestamp_gt: "{timestamp_start}", timestamp_lt: "{timestamp_end}"}}) {{
            ohmBalance
            address
            day
        }}
    }}
    """
    # balance before listing
    
    query = gql(queryString)

    result = await client.execute_async(query)
    
    days = {}

    for res in result:
        for day in result[res]:
            if not (str(day['day']) in days):
                days[str(day['day'])] = {}
                days[str(day['day'])]['timestamp'] = 1609459200 + 86400*int(day['day'])
                days[str(day['day'])]['balance'] = int(day['ohmBalance']) / 1000000000
                days[str(day['day'])]['holders'] = 1
            else:
                days[str(day['day'])]['timestamp'] = 1609459200 + 86400*int(day['day'])
                temp = days[str(day['day'])]['balance']
                temp += (int(day['ohmBalance'])/ 1000000000)
                days[str(day['day'])]['balance'] = temp
                days[str(day['day'])]['holders'] +=1

    days_array = []
    for i in days:
        days_array.append(days[i])

    return days_array

timestamp_start = 1617291702
days = 10
amount = 10000
res = getTopBalances(timestamp_start, days, amount)

print(res)





