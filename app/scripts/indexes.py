import requests
from datetime import datetime

def getLogRebases():

	queryString = f"""query getLogRebases {{
		logRebaseDailies(orderBy: timestamp, first:1000) {{
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


async def parseNDays(timestamp_start, period, n):

	days = getLogRebases()['data']['logRebaseDailies']
	result = []
	for i in days:
		if int(i['timestamp']) >= timestamp_start:
			obj = {}
			obj['timestamp'] = int(i['timestamp']) + 86400
			obj['index'] = int(i['index'])

			result.append(obj)

	return result[:period:n]


async def parseNHours(timestamp_start, period, n):

	days = getLogRebases()['data']['logRebaseDailies']
	result = []
	for i in days:
		for j in range(0, 86400, 3600):
			obj = {}
			obj['timestamp'] = int(i['timestamp'])+j+3600

			if obj['timestamp'] >= timestamp_start:
				f = next((item for item in i['hours'] if item["timestamp"] == f"{int(i['timestamp'])+j}"), None)
				if f == None:
					if len(result) == 0:
						obj['index'] = 0
					else:
						obj['index'] = int(result[-1]['index'])
				else:
					obj['index'] = int(f['index'])

				result.append(obj)

	return result[:period*n:n]

async def parseNMinutes(timestamp_start, period, n):

	days = getLogRebases()['data']['logRebaseDailies']
	result = []
	for i in days:
		for j in range(0, 86400, 3600):
			f = next((item for item in i['hours'] if item["timestamp"] == f"{obj['timestamp']}"), None)
			for k in (0, 3600, 60):
				obj = {}
				obj['timestamp'] = int(i['timestamp'])+ j + 3600 + k 
				
				if f == None:
					if len(result) == 0:
						obj['index'] = 0
					else:
						obj['index'] = int(result[-1]['index'])
				else:
					obj['index'] = int(f['index'])

				result.append(obj)

	return result[::n]


