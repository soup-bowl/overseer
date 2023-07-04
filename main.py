#!/usr/bin/env python3

import subprocess
import requests
import yaml
import time
import paramiko
from display import Display


def read_config():
	with open('configuration.yml', 'r') as file:
		try:
			data = yaml.safe_load(file)
			return data
		except yaml.YAMLError:
			return None


def format_number(num):
	num = num.replace(',', '')
	value = int(num)
	if value >= 1000000:
		return f"{value/1000000:.0f} M"
	elif value >= 1000:
		return f"{value/1000:.0f} K"
	else:
		return str(value)


def is_device_online(ip_address):
	command = ['ping', '-c', '1', ip_address]
	try:
		output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
		if '1 packets transmitted, 1 received' in output:
			return True
	except subprocess.CalledProcessError:
		pass
	return False


def get_pihole(host, key):
	try:
		response = requests.get(f"http://{host}/admin/api.php?auth={key}&summary")
		response.raise_for_status()
	except requests.HTTPError:
		return None
	except Exception:
		return None

	return response.json()


def get_linode(instance, token):
	# https://www.linode.com/docs/api/linode-instances/#linode-statistics-view
	try:
		response = requests.get(f"https://api.linode.com/v4/linode/instances/{instance}/stats", headers={
			"Authorization": f"Bearer {token}",
			"Content-Type": "application/json"
		})
		response.raise_for_status()
	except requests.HTTPError:
		return None
	except Exception:
		return None

	return response.json()


def get_synology_nas(server, user, password):
	try:
		auth_response = requests.get(f"http://{server}/webapi/auth.cgi", {
			'api': 'SYNO.API.Auth',
			'version': 2,
			'method': 'login',
			'account': user,
			'passwd': password,
			'format': 'sid'
		})
		auth_response.raise_for_status()
		auth = auth_response.json()['data']['sid']

		data_response = requests.get(f"http://{server}/webapi/entry.cgi", {
			'api': 'SYNO.Storage.CGI.Storage',
			'version': 1,
			'method': 'load_info',
			'_sid': auth
		})
		data_response.raise_for_status()
	except requests.HTTPError:
		return None
	except Exception:
		return None

	return data_response.json()


def get_ssh(server, user, key, command):
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	try:
		private_key = paramiko.RSAKey.from_private_key_file(key)
		client.connect(server, username=user, pkey=private_key)
		stdin, stdout, stderr = client.exec_command(command)
		return stdout.read().decode()
	except:
		return None
	finally:
		client.close()


def format_bytes(num):
	units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
	i = 0

	while num >= 1024 and i < len(units)-1:
		num /= 1024
		i += 1

	formatted_num = '{:.2f}'.format(num)

	result = f"{formatted_num} {units[i]}"

	return result


config = read_config()
display = Display(config['name'])

for stage in config['stages']:
	if stage['type'] == 'ssh':
		data = get_ssh(stage['address'], stage['user'], stage['auth'], stage['command'])
		if data is not None:
			text = data.replace("\n", "")
			prefix = stage['prefix'] if 'prefix' in stage else ''
			suffix = stage['suffix'] if 'suffix' in stage else ''
			display.write_line(stage['label'], f"{prefix}{text}{suffix}")
		else:
			display.write_line(stage['label'], "ERROR", True)

	elif stage['type'] == 'pihole':
		pidata = get_pihole(stage['address'], stage['auth'])
		if pidata is not None:
			display.write_line(
				stage['label'],
				(
					"Block "
					f"{format_number(pidata.get('ads_blocked_today'))}"
					"/"
					f"{format_number(pidata.get('dns_queries_today'))}"
				)
			)
			display.write_line(None, f"{pidata.get('ads_percentage_today')}% blocked")
		else:
			display.write_line(stage['label'], "OFFLINE", True)

	elif stage['type'] == 'synology':
		data = get_synology_nas(stage['address'], stage['user'], stage['auth'])

		if data is not None:
			total_volume = 0
			used_volume = 0
			for volume in data['data']['volumes']:
				total_volume += int(volume['size']['total'])
				used_volume += int(volume['size']['used'])

			percentage_used = (used_volume / total_volume) * 100

			display.write_line(
				stage['label'],
				f"{format_bytes(used_volume)} / {format_bytes(total_volume)} ({percentage_used:.0f}%)"
			)
		else:
			display.write_line(stage['label'], "OFFLINE", True)

	elif stage['type'] == 'linode':
		lindata = get_linode(stage['address'], stage['auth'])

		if lindata is not None:
			current = time.time() * 1000
			tframe = current - (7 * 60 * 60 * 1000)  # 7 hours ago

			cpu_timers = [timestamp for timestamp, _ in lindata['data']['cpu'] if timestamp >= tframe]
			cpu_totals = sum(value for timestamp, value in lindata['data']['cpu'] if timestamp >= tframe)
			cpu_averge = cpu_totals / len(cpu_timers)

			io_timers = [timestamp for timestamp, _ in lindata['data']['io']['io'] if timestamp >= tframe]
			io_totals = sum(value for timestamp, value in lindata['data']['io']['io'] if timestamp >= tframe)
			io_averge = io_totals / len(io_timers)

			net_timers = [timestamp for timestamp, _ in lindata['data']['netv4']['out'] if timestamp >= tframe]
			net_totals = sum(value for timestamp, value in lindata['data']['netv4']['out'] if timestamp >= tframe)
			net_averge = (net_totals / len(net_timers)) / 1000

			display.write_line(stage['label'], f"c{cpu_averge:.2f}% d{io_averge:.2f} n{net_averge:.2f}K/s")
		else:
			display.write_line(stage['label'], "OFFLINE", True)

	elif stage['type'] == 'isup':
		if is_device_online(stage['address']):
			display.write_line(stage['label'], "ONLINE")
		else:
			display.write_line(stage['label'], "OFFLINE", True)

display.done()
