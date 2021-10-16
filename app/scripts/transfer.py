from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from datetime import datetime

transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/deltax2016/olympus-wallets")
client = Client(transport=transport, fetch_schema_from_transport=True)

async def getTransfer(timestamp_start, period):

    day_start = datetime.fromtimestamp(timestamp_start).timetuple().tm_yday
    timestamp_end = timestamp_start + 86400*period

    queryString = f"""query getTransfer {{
      t_from1:transfers(orderBy: timestamp, first: 1000, where: {{from: "0x9272B16e278051Ed961886E67bF31b45e2D8CB66"}}) {{
        to
        amount
        timestamp
      }}
      t_from2:transfers(orderBy: timestamp, skip: 1000, first: 1000, where: {{from: "0x9272B16e278051Ed961886E67bF31b45e2D8CB66"}}) {{
        to
        amount
        timestamp
      }}
      t_from3:transfers(orderBy: timestamp, skip:1000, first: 1000, where: {{from: "0x9272B16e278051Ed961886E67bF31b45e2D8CB66"}}) {{
        to
        amount
        timestamp
      }}
}}
    """
    # balance before listing
    
    query = gql(queryString)

    result = await client.execute_async(query)
    
    days = {}

    for res in result:
        for day in result[res]:
            real_day = datetime.fromtimestamp(int(day['timestamp'])).timetuple().tm_yday
            if not (real_day in days):
                days[real_day] = {}
                days[real_day]['timestamp'] = 1609459200 + 86400*int(real_day)
                days[real_day]['amount'] = day['amount']
            else:
                days[real_day]['timestamp'] = 1609459200 + 86400*int(real_day)
                days[real_day]['amount'] = day['amount']

    array = []
    real_day = datetime.fromtimestamp(int(timestamp_start)).timetuple().tm_yday
    for i in range(1, real_day+period):
        if i in days:
            array.append(days[i])
        else:
            tempTransfer = {}
            tempTransfer['timestamp'] = 1609459200 + 86400*int(i)
            tempTransfer['amount'] = "0"
            array.append(tempTransfer)




    '''    
    days_array = []
    for i in days:
        days_array.append(days[i])
        print(days)
    '''

    return array[real_day:real_day+period]

timestamp_start = 1631779135
days = 30
amount = 10000

if __name__ == "__main__":
    res = getTransfer(timestamp_start, days)
    print(res)

