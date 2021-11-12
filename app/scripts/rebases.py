import requests
from datetime import datetime

def getLogRebases(start, end):

	queryString = f"""query getLogRebases {{
		logRebases(orderBy: timestamp, first:1000, where:{{timestamp_gte: {start}, timestamp_lte: {end}}}){{
		    timestamp
		}}
	}}
	"""

	request = requests.post('https://api.thegraph.com/subgraphs/name/deltax2016/olympus-sohm', json={'query': queryString})
	result = request.json()

	return result


async def rebaseTimestamps(start, end):

	print(getLogRebases(start, end))

	rebases = getLogRebases(start, end)['data']['logRebases']
	result = []

	for i in rebases:
		result.append(int(i['timestamp']))

	return result
