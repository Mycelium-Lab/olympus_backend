import requests
from datetime import datetime

def getLogRebases(end):

	queryString = f"""query getLogRebases {{
		logRebaseDailies(orderBy: timestamp, first:1000, where:{{timestamp_lte:"{end}"}}) {{
			timestamp
			index
			hours(orderBy: timestamp, first:24, where:{{timestamp_lte:"{end}"}}) {{
				timestamp
				index
				minutes(orderBy: timestamp, first:60, where:{{timestamp_lte:"{end}"}}) {{
					timestamp
					index
				}}
			}}
		}}
	}}
	"""

	request = requests.post('https://api.thegraph.com/subgraphs/name/deltax2016/olympus-sohm', json={'query': queryString})
	result = request.json()

	return result


async def parseNDays(timestamp_start, end, n):

	timestamp_start -= 86400

	days = getLogRebases(end)['data']['logRebaseDailies']
	result = []
	for i in days:
		if int(i['timestamp']) >= timestamp_start:
			obj = {}
			obj['timestamp'] = int(i['timestamp']) + 86400
			obj['index'] = round(int(i['index']) / 1000000000, 3)

			result.append(obj)

	return result[::n]


def parseDictHours(array, end):

	result = {}

	for i in array:
		for k in i['hours']:
			if int(k['timestamp']) <= end:
				result[int(k['timestamp'])] = k['index']
			else:
				return result

	return result

def parseDictMinutes(array, end):

	result = {}

	for i in array:
		for j in i['hours']:
			for k in j['minutes']:
				if int(k['timestamp']) <= end:
					result[int(k['timestamp'])] = k['index']
				else:
					return result

	return result

def searchNearestHours(start, dicts):
	if start <= 1623700800:
		return 0
	else:
		for i in range(start, 1623700800, -3600):
			if i in dicts:
				return dicts[i]
		return dicts[1623700800]

def searchNearest(start, dicts):
	if start <= 1623702000:
		return 0
	else:
		for i in range(start, 1623702000, -60):
			if i in dicts:
				return dicts[i]
		return dicts[1623702000]

async def parseNHours(timestamp_start, timestamp_end, n):

	minutes = getLogRebases(timestamp_end)['data']['logRebaseDailies']

	start = timestamp_start - (timestamp_start % (3600*n))
	end = timestamp_end - (timestamp_end % (3600*n))

	main_dict = parseDictHours(minutes, end)

	result = []
	cnt = 0

	nearest = searchNearestHours(start, main_dict)

	for i in range(start, end, 3600):
		tempObj = {}
		tempObj['timestamp'] = i
		if i in main_dict:
			tempObj['index'] = round(int(main_dict[i]) / 1000000000, 3)
		else:
			if cnt == 0:
				tempObj['index'] = round(int(nearest) / 1000000000, 3)
			else:
				tempObj['index'] = result[cnt-1]['index']
		cnt += 1
		result.append(tempObj)

	return result[n::n]

async def parseNMinutes(timestamp_start, timestamp_end, n):

	minutes = getLogRebases(timestamp_end)['data']['logRebaseDailies']

	start = timestamp_start - (timestamp_start % (60*n))
	end = timestamp_end - (timestamp_end % (60*n))

	main_dict = parseDictMinutes(minutes, end)

	result = []
	cnt = 0

	nearest = searchNearest(start, main_dict)

	for i in range(start, end, 60):
		tempObj = {}
		tempObj['timestamp'] = i
		if i in main_dict:
			tempObj['index'] = round(int(main_dict[i]) / 1000000000, 3)
		else:
			if cnt == 0:
				tempObj['index'] = round(int(nearest) / 1000000000, 3)
			else:
				tempObj['index'] = result[cnt-1]['index']
		cnt += 1
		result.append(tempObj)

	return result[n::n]




