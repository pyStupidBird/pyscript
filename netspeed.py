#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import time
import commands

def main():
	eth =  '''ifconfig | cut -d' ' -f1 | sed '/^$/d'|grep -v lo|cut -d ":" -f1'''
	ethcmd = commands.getstatusoutput(eth)[1]
	f = ethcmd.split('\n')
	speed = []
	
	for i in range(len(f)):
		ethname = f[i]
		try:
			cmd = '''ethtool %s |grep -i speed|cut -d ":" -f 2|cut -d "M" -f 1''' % ethname
			cmdstatus = commands.getstatusoutput(cmd)[1].strip()
			value = int(cmdstatus)
		except:
			value = 0
	
		data = {}
		data['Metric'] = 'net.speed'
		data['Endpoint'] = os.uname()[1]
		data['Timestamp'] = int(time.time())
		data['Value'] = value
		data['CounterType'] = 'GAUGE'
		data['Step'] = 60
		data['TAGS'] = 'iface=%s' %ethname
		speed.append(data)
	print json.dumps(speed)

if __name__ == '__main__':
	main()

