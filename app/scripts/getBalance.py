from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/id/QmThQWLEohGNnWzKpozLxdDq5XHpWupyrJixWACbKSVMPM")
client = Client(transport=transport, fetch_schema_from_transport=True)

async def getBalances(timestamp_start, period, address):
    timestamp_end = timestamp_start + 86400*period

    queryString = f"""query getDAO {{
        dailyBalances(orderBy: timestamp, where: {{address: "{address}", timestamp_gt: "{timestamp_start}", timestamp_lt: "{timestamp_end}"}}) {{
            ohmBalance
            day
        }}
    }}
    """

    query = gql(queryString)

    result = await client.execute_async(query)
    
    array_balance = []
    for day in result['dailyBalances']:
        tempBalance = {}
        tempBalance['balance'] = int(day['ohmBalance']) / 1000000000
        tempBalance['timestamp'] = 1609459200 + 86400*int(day['day'])
        array_balance.append(tempBalance)

    

    return array_balance






