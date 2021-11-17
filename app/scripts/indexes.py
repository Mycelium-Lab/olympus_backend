import requests
from datetime import datetime


#запрос к thegraph
def getLogRebases(end):

	queryString = f"""query getLogRebases {{
		logRebaseDailies(orderBy: timestamp, first:1000, where:{{timestamp_lte:"{end}"}}) {{
			timestamp
			index
			hours(orderBy: timestamp, first:24) {{
				timestamp
				index
				minutes(orderBy: timestamp, first:60) {{
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


#функция парсинга дней
async def parseNDays(timestamp_start, timestamp_end, n):


	if (timestamp_start % (86400)) == 0:

		start = timestamp_start - (timestamp_start % (86400))

	else:

		start = timestamp_start - (timestamp_start % (86400)) + 86400

	print(start)
	end = timestamp_end - (timestamp_end % (86400))

	days = getLogRebases(timestamp_end+(86400*n))['data']['logRebaseDailies']
	result = []

	if days:

		last_timestamp = days[-1]['timestamp']
		first_timestamp = days[0]['timestamp']

		for i in range(start, int(first_timestamp), 86400):
			obj = {}
			obj['timestamp'] = i
			obj['index'] = 0

			result.append(obj)

		for i in days:
			if int(i['timestamp']) >= timestamp_start:
				obj = {}
				obj['timestamp'] = int(i['timestamp'])
				obj['index'] = round(int(i['index']) / 1000000000, 3)

				result.append(obj)

		for i in range(int(last_timestamp)+86400, end, 86400):
			obj = {}
			obj['timestamp'] = i
			obj['index'] = 0

			result.append(obj)
	else:

		for i in range(start, end, 86400):

			obj = {}
			obj['timestamp'] = i
			obj['index'] = 0

			result.append(obj)
		
	new_result = []
	cnt = 0

	if days:

		for i in result:

			if cnt % n == 0:

				obj = {}
				obj['timestamp'] = i['timestamp']
				obj['index'] = i['index']

				new_result.append(obj)

			else:

				if i['timestamp'] <= int(last_timestamp):

					new_result[-1]['index'] = i['index']

			cnt += 1

	else:

		new_result = result[::n]

	return new_result


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

	hours = getLogRebases(timestamp_end+86400)['data']['logRebaseDailies']

	if (timestamp_start % (3600)) == 0:

		start = timestamp_start - (timestamp_start % (3600))

	else:

		start = timestamp_start - (timestamp_start % (3600)) + 3600

	end = timestamp_end - (timestamp_end % (3600))

	hi_end = timestamp_end - (timestamp_end % 3600)

	main_dict = parseDictHours(hours, hi_end)

	result = []
	cnt = 0

	if hours:

		last_timestamp = int(hours[-1]['hours'][-1]['timestamp'])
		first_timestamp = hours[0]['timestamp']

		nearest = searchNearestHours(start, main_dict)

		for i in range(start, end, 3600):

			tempObj = {}
			tempObj['timestamp'] = i

			if (i > int(last_timestamp)) or (i < int(first_timestamp)):

				tempObj['index'] = 0

			else:

				if i in main_dict:

					tempObj['index'] = round(int(main_dict[i]) / 1000000000, 3)

				else:

					if cnt == 0:

						tempObj['index'] = round(int(nearest) / 1000000000, 3)

					else:

						tempObj['index'] = result[cnt-1]['index']
			cnt += 1
			result.append(tempObj)
	else:

		for i in range(start, end, 3600):

			obj = {}
			obj['timestamp'] = i
			obj['index'] = 0

			result.append(obj)

	new_result = []

	cnt = 0

	#print(result[n::])

	if hours:

		for i in result:

			if cnt % n == 0:

				obj = {}
				obj['timestamp'] = i['timestamp']
				obj['index'] = i['index']

				new_result.append(obj)

			else:

				if i['timestamp'] <= int(last_timestamp):

					new_result[-1]['index'] = i['index']

			cnt += 1

	else:

		new_result = result[::n]

	return new_result

async def parseNMinutes(timestamp_start, timestamp_end, n):

	minutes = getLogRebases(timestamp_end+3600*8*n)['data']['logRebaseDailies']

	if (timestamp_start % (60)) == 0:

		start = timestamp_start - (timestamp_start % (60))

	else:

		start = timestamp_start - (timestamp_start % (60)) + 60
		
	end = timestamp_end - (timestamp_end % (60))

	result = []
	cnt = 0

	if minutes:

		last_timestamp = int(minutes[-1]['hours'][-1]['minutes'][-1]['timestamp'])
		first_timestamp = minutes[0]['timestamp']

		main_dict = parseDictMinutes(minutes, end)

		nearest = searchNearest(start, main_dict)

		for i in range(start, end, 60):

			tempObj = {}
			tempObj['timestamp'] = i

			if (i > int(last_timestamp)) or (i < int(first_timestamp)):

				tempObj['index'] = 0

			else:

				if i in main_dict:

					tempObj['index'] = round(int(main_dict[i]) / 1000000000, 3)

				else:

					if cnt == 0:

						tempObj['index'] = round(int(nearest) / 1000000000, 3)

					else:

						tempObj['index'] = result[cnt-1]['index']
			cnt += 1
			result.append(tempObj)

	else:

		for i in range(start, end, 60):

			obj = {}
			obj['timestamp'] = i
			obj['index'] = 0

			result.append(obj)

	new_result = []

	cnt = 0

	if minutes:

		for i in result:

			if cnt % n == 0:

				obj = {}
				obj['timestamp'] = i['timestamp']
				obj['index'] = i['index']

				new_result.append(obj)

			else:

				if i['timestamp'] <= int(last_timestamp):

					new_result[-1]['index'] = i['index']

			cnt += 1

	else:

		new_result = result[::n]


	return new_result




