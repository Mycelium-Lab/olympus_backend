from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from datetime import datetime

transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/deltax2016/olympus-wallets")
client = Client(transport=transport, fetch_schema_from_transport=True)

async def getTopBalances(timestamp_start, period, balance_gt):

    balance_gt = balance_gt*1000000000
    day_start = datetime.fromtimestamp(timestamp_start).timetuple().tm_yday
    timestamp_end = timestamp_start + 86400*period
    print(timestamp_end)

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
        t4:dailyBalances(first:1000, skip: 3000, orderBy: timestamp, where: {{ohmBalance_gt: "{balance_gt}", timestamp_gt: "{timestamp_start}", timestamp_lt: "{timestamp_end}"}}) {{
            ohmBalance
            address
            day
        }}
        t5:dailyBalances(first:1000, skip: 4000, orderBy: timestamp, where: {{ohmBalance_gt: "{balance_gt}", timestamp_gt: "{timestamp_start}", timestamp_lt: "{timestamp_end}"}}) {{
            ohmBalance
            address
            day
        }}
        t6:dailyBalances(first:1000, skip: 5000, orderBy: timestamp, where: {{ohmBalance_gt: "{balance_gt}", timestamp_gt: "{timestamp_start}", timestamp_lt: "{timestamp_end}"}}) {{
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

timestamp_start = 1617291702
days = 10
amount = 10000
res = getTopBalances(timestamp_start, days, amount)

print(res)





