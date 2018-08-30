import os
import datetime
import requests
import xml.etree.ElementTree as ET


LINE_NOTIFY_TOKEN = os.environ['ACCESS_TOKEN']
FORCAST_URL = 'https://www.drk7.jp/weather/xml/13.xml'
LINE_NOTIFY_API = 'https://notify-api.line.me/api/notify'
PERIOD = ['0時から6時までの降水確率：', '6時から12時までの降水確率：',
			'12時から18時までの降水確率：', '18時から24時までの降水確率：']

def get_rainfallchance():
	today = datetime.datetime.today().strftime("%Y/%m/%d")
	forcast = requests.get(FORCAST_URL)

	root = ET.fromstring(forcast.content)
	pref = root.find('pref')

	for area in pref:
		if area.attrib['id'] == '東京地方':
			tokyo = area

	for child in tokyo:
		if child.tag == 'info':
			if child.attrib['date'] == today:
				info = child

	for child in info:
		if child.tag == 'rainfallchance':
			rainfallchance = child

	period = []

	for child in rainfallchance:
		period.append(child.text)

	return period

def lambda_handler(evnet=None, context=None):
	period = get_rainfallchance()
	for i in range(4):
		message = PERIOD[i] + period[i] + '%'
		payload = {'message': message}
		headers = {'Authorization': 'Bearer ' + LINE_NOTIFY_TOKEN}
		line_notify = requests.post(LINE_NOTIFY_API, data=payload, headers=headers)

if __name__ == '__main__':
	lambda_handler()
