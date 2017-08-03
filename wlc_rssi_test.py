import csv
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException,NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException
import time
import sys


# these are just simple python formatted files with variables in them
# the WLC IP and credentials are in here
from credentials import *

# first we want to grab all the APs that the WLC knows about

wlc = {
		'device_type': 'cisco_wlc',
		'ip': controller,
		'username': controller_u,
		'password': controller_p,
		'port' : 22,          # optional, defaults to 22
		'secret': secret,     # optional, defaults to ''
		'verbose': False,       # optional, defaults to False
	}

wlc_connect = ConnectHandler(**wlc)

client = sys.argv[1]

print "Client,RSSI,SNR,channel,AP"

try:
	while True:
		command = 'show client detail ' + client
		client_detail = wlc_connect.send_command(command).split("\n")

		for client_detail_line in client_detail:
			if "Radio Signal Strength Indicator" in client_detail_line:
				rssi = client_detail_line.split()[4]
			if "AP Name" in client_detail_line:
				ap_name = client_detail_line.split()[2]
			if "Channel." in client_detail_line:
				channel = client_detail_line.split()[1]
			if "Signal to Noise Ratio" in client_detail_line:
				snr = client_detail_line.split()[4]	
		print client + "," + rssi + "," + snr + "," + channel + "," + ap_name
		time.sleep(2)
except KeyboardInterrupt:
    pass
	
wlc_connect.disconnect()

