import sys,urllib,time

def sendsms(mobile,subject,content):
	""" send sms"""
	log_file = "/data/zabbix_trigger_logs/smslog_"
	type = 'pt'
	values = {'mobile':mobile,'title':subject,'content':content}
	data = urllib.urlencode(values)
	post_url = 'http://10.144.6.38:8080/ump/send/sms'
	try :
		conn = urllib.urlopen(post_url,data)
		print (conn.read())
		txt = conn.read()
	except Exception as e:
		print (e)
	file_current_time = time.strftime('%Y-%m',time.localtime(time.time()))
	current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	log_file = log_file + file_current_time
	#print(log_file)
	body = current_time + " " + mobile + " " + subject + "\n"
	#print(body)
	with open(log_file,'a') as file:
		file.write(body)

mobile = sys.argv[1]
subject = sys.argv[2]
content = sys.argv[3]

sendsms(mobile,subject,content)
