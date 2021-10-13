from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/id/QmWKyoR5kTzfEe1PagjFicAfCZCkEVruCoNvw2TAykC79D")
client = Client(transport=transport, fetch_schema_from_transport=True)

async def queryTotal(timestamp_start, period):
    timestamp_end = timestamp_start + 86400*period

    queryString = f"""query getTotal {{
        totalSupplies(orderBy: timestamp, where: {{timestamp_gt: "{timestamp_start}", timestamp_lt: "{timestamp_end}"}}) {{
            ohmBalance
            totalWallets
            day
        }}
    }}
    """

    query = gql(queryString)

    result = await client.execute_async(query)

    return result

async def totalWallets(timestamp_start, period):
    
    result = await queryTotal(timestamp_start, period)
    array_balance = []
    for day in result['totalSupplies']:
        tempBalance = {}
        tempBalance['balance'] = int(day['ohmBalance']) / 1000000000
        tempBalance['timestamp'] = 1609459200 + 86400*int(day['day'])
        array_balance.append(tempBalance)

    return array_balance

async def totalBalances(timestamp_start, period):
    
    result = await queryTotal(timestamp_start, period)
    array_balance = []
    for day in result['totalSupplies']:
        tempBalance = {}
        tempBalance['wallets'] = int(day['totalWallets'])
        tempBalance['timestamp'] = 1609459200 + 86400*int(day['day'])
        array_balance.append(tempBalance)

    return array_balance






