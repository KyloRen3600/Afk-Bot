import datetime

def log(type, message):
	now = datetime.datetime.now()
	hour = now.hour
	if hour < 10:
		hour = "0{0}".format(hour)
	minute = now.minute
	if minute < 10:
		minute = "0{0}".format(minute)
	second = now.second
	if second < 10:
		second = "0{0}".format(second)
	now = "[{0}:{1}:{2}] [{3}]:".format(hour, minute, second, type)
	print("{0} {1}".format(now, message))