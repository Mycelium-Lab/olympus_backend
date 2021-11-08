import requests
from datetime import datetime

async def getFirstLegacy(timestamp_start, period, cnt=None):
    
    day_start = datetime.fromtimestamp(timestamp_start).timetuple().tm_yday
    timestamp_end = timestamp_start + 86400*period

    queryString = "query balancesByWallet {"

    if cnt >= 1000:
        queryString += f"""
            w0:wallets(orderBy: birth, first: 1000, where: {{address_not_in:["0xfd31c7d00ca47653c6ce64af53c1571f9c36566a","0x0822f3c03dcc24d200aff33493dc08d0e1f274a2", "0xbe731507810c8747c3e01e62c676b1ca6f93242f"]}}) {{
                id
                dailyBalance(orderBy: timestamp, first: 1000) {{
                    ohmBalance
                    day
                }}
            }}
        """
    else:
        queryString += f"""
            w0:wallets(orderBy: birth, first: {cnt%1000}, where: {{address_not_in:["0xfd31c7d00ca47653c6ce64af53c1571f9c36566a","0x0822f3c03dcc24d200aff33493dc08d0e1f274a2", "0xbe731507810c8747c3e01e62c676b1ca6f93242f"]}}) {{
                id
                dailyBalance(orderBy: timestamp, first: 1000) {{
                    ohmBalance
                    day
                }}
            }}
        """
    for i in range(1,int(cnt/1000)):
        if i > 5:
            break
        else:
            first = 1000
            if cnt/i < 1000:
                first = cnt % 1000
                print(first)
            queryString += f"""
                w{i}:wallets(orderBy: birth, first: {first}, skip: {1000*i}, where: {{address_not_in:["0xfd31c7d00ca47653c6ce64af53c1571f9c36566a","0x0822f3c03dcc24d200aff33493dc08d0e1f274a2", "0xbe731507810c8747c3e01e62c676b1ca6f93242f"]}}) {{
                    id
                    dailyBalance(orderBy: timestamp, first: 1000) {{
                        ohmBalance
                        day
                    }}
                }}
            """
    queryString += "}"
    # balance before listing
    

    query = gql(queryString)

    result = await client.execute_async(query)
    
    days = {}

    for res in result:
        for wallet in result[str(res)]:
            for day in wallet['dailyBalance']:
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


async def getFirstWallets(timestamp_start, period, cnt=None):
    
    day_start = datetime.fromtimestamp(timestamp_start).timetuple().tm_yday
    timestamp_end = timestamp_start + 86400*period

    queryString = "query balancesByWallet {"


    first = 1000

    if cnt < 1000:
        first = cnt % 1000

    queryString += f"""
        w0:wallets(orderBy: birth, first: {first}, where: {{address_not_in:["0xfd31c7d00ca47653c6ce64af53c1571f9c36566a","0x0822f3c03dcc24d200aff33493dc08d0e1f274a2"]}}) {{
            id
            dailyBalance(orderBy: timestamp, first: 1000) {{
                ohmBalance
                day
                hourBalance(orderBy: timestamp, first: 24) {{
                    ohmBalance
                    hour
                }}
            }}
        }}
    """
    for i in range(1,int(cnt/1000)):
        if i > 5:
            break
        else:
            first = 1000
            if cnt/i < 1000:
                first = cnt % 1000
                print(first)
            queryString += f"""
                w{i}:wallets(orderBy: birth, first: {first}, skip: {1000*i}, where: {{address_not_in:["0xfd31c7d00ca47653c6ce64af53c1571f9c36566a","0x0822f3c03dcc24d200aff33493dc08d0e1f274a2"]}}) {{
                    id
                    dailyBalance(orderBy: timestamp, first: 1000) {{
                        ohmBalance
                        day
                        hourBalance(orderBy: timestamp, first: 24) {{
                            ohmBalance
                            hour
                        }}
                    }}
                }}
            """
    queryString += "}"
    # balance before listing
    request = requests.post('https://api.thegraph.com/subgraphs/name/deltax2016/olympus-wallets', json={'query': queryString})
    result = request.json()
    
    return result


async def getFirstWalletsNDays(timestamp_start, period, cnt=None, days=1):

    result = await getFirstWallets(timestamp_start, period, cnt)
    days_dict = {}

    for res in result['data']:
        for wallet in result['data'][str(res)]:
            for day in wallet['dailyBalance']:
                if not (int(day['day']) in days_dict):
                    days_dict[int(day['day'])] = {}
                    days_dict[int(day['day'])]['timestamp'] = 1609459200 + 86400*int(day['day'])
                    days_dict[int(day['day'])]['balance'] = int(day['ohmBalance']) / 1000000000
                else:
                    days_dict[int(day['day'])]['timestamp'] = 1609459200 + 86400*int(day['day'])
                    temp = days_dict[int(day['day'])]['balance']
                    temp += (int(day['ohmBalance'])/ 1000000000)
                    days_dict[int(day['day'])]['balance'] = temp

    days_array = []
    real_day = datetime.fromtimestamp(int(timestamp_start)).timetuple().tm_yday
    for i in range(0, real_day+period, days):
        if i in days_dict:
            days_array.append(days_dict[i])
        else:
            tempDay = {}
            tempDay['timestamp'] = 1609459200 + 86400*int(i)
            if i!= 0:
                tempDay['balance'] = days_array[i-1]['balance']
            else:
                tempDay['balance'] = "0"
            days_array.append(tempDay)


    return days_array[real_day:real_day+period]


async def getFirstWalletsNHours(timestamp_start, period, cnt=None, hours=1):

    result = await getFirstWallets(timestamp_start, period, cnt)
    hours_dict = {}

    for res in result['data']:
        for wallet in result['data'][str(res)]:
            for day in wallet['dailyBalance']:
                for hour in day['hourBalance']:
                    if not ((int(day['day'])+1)*(int(hour['hour'])+1)) in hours_dict:
                        hours_dict[(int(day['day'])+1)*(int(hour['hour'])+1)] = {}
                        hours_dict[(int(day['day'])+1)*(int(hour['hour'])+1)]['timestamp'] = 1609459200 + 3600*(int(day['day'])+1)*(int(hour['hour'])+1)
                        hours_dict[(int(day['day'])+1)*(int(hour['hour'])+1)]['balance'] = int(hour['ohmBalance']) / 1000000000
                    else:
                        hours_dict[int(day['day'])*int(hour['hour'])]['timestamp'] = 1609459200 + 3600*(int(day['day'])+1)*(int(hour['hour'])+1)
                        temp = hours_dict[(int(day['day'])+1)*(int(hour['hour'])+1)]['balance']
                        temp += (int(hour['ohmBalance'])/ 1000000000)
                        hours_dict[(int(day['day'])+1)*(int(hour['hour'])+1)]['balance'] = temp

    hours_array = []
    real_day = datetime.fromtimestamp(int(timestamp_start)).timetuple().tm_yday
    real_hour = datetime.fromtimestamp(int(timestamp_start)).timetuple().tm_hour
    for i in range(0, (real_day+1)*real_hour+period, hours):
        if i in hours_dict:
            hours_array.append(hours_dict[i])
        else:
            tempHour = {}
            tempHour['timestamp'] = 1609459200 + 3600*int(i)
            if i!= 0:
                tempHour['balance'] = hours_array[i-1]['balance']
            else:
                tempHour['balance'] = "0"
            hours_array.append(tempHour)


    return hours_array[(real_day+1)*(real_hour+1):(real_day+1)*real_hour*(real_hour+1)+period]


