#!/usr/bin/env python3

import subprocess, requests, yaml, time, paramiko

from pysnmp.hlapi import *
from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from inky.auto import auto

def read_config():
	with open('configuration.yml', 'r') as file:
		try:
			data = yaml.safe_load(file)
			return data
		except yaml.YAMLError as e:
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
	except requests.HTTPError as http_err:
		return None
	except Exception as err:
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
	except requests.HTTPError as http_err:
		return None
	except Exception as err:
		return None

	return response.json()

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

config = read_config()

inky_display = auto(ask_user=True)
inky_display.set_border(inky_display.BLACK)

# Create a new canvas to draw on
img = Image.new("P", inky_display.resolution)
draw = ImageDraw.Draw(img)

scale_size = 1.30
hanken_bold_font = ImageFont.truetype(HankenGroteskBold, int(13 * scale_size))
hanken_medium_font = ImageFont.truetype(HankenGroteskBold, int(13 * scale_size))

# Define parameters for boundaries and distances
y_top = int(inky_display.height * (5.0 / 10.0))
y_bottom = y_top + int(inky_display.height * (4.0 / 10.0))
x_barrier = 60
y_spacer = 13

# Make the background black
for y in range(0, inky_display.height):
	for x in range(0, inky_display.width):
		img.putpixel((x, y), inky_display.BLACK)

draw.text((2, 0), config['name'], inky_display.RED, font=hanken_bold_font)

y_placement = 1
for stage in config['stages']:
	if stage['type'] == 'ssh':
		data = get_ssh(stage['address'], stage['user'], stage['auth'], stage['command'])
		draw.text((2, (y_placement * y_spacer)), f"{stage['label']}:", inky_display.WHITE, font=hanken_medium_font)
		if data is not None:
			text   = data.replace("\n", "")
			prefix = stage['prefix'] if 'prefix' in stage else ''
			suffix = stage['suffix'] if 'suffix' in stage else ''
			draw.text(
				(x_barrier, (y_placement * y_spacer)),
				f"{prefix}{text}{suffix}",
				inky_display.WHITE,
				font=hanken_medium_font
			)
		else:
			draw.text((x_barrier, (y_placement * y_spacer)), "ERROR", inky_display.RED, font=hanken_medium_font)
		y_placement = y_placement + 1
	if stage['type'] == 'pihole':
		pidata = get_pihole(stage['address'], stage['auth'])
		draw.text((2, (y_placement * y_spacer)), f"{stage['label']}:", inky_display.WHITE, font=hanken_medium_font)
		if pidata is not None:
			draw.text(
				(x_barrier, (y_placement * y_spacer)),
				f"Block {format_number(pidata.get('ads_blocked_today'))}/{format_number(pidata.get('dns_queries_today'))}",
				inky_display.WHITE,
				font=hanken_medium_font
			)
			draw.text(
				(x_barrier, ((y_placement + 1) * y_spacer)),
				f"{pidata.get('ads_percentage_today')}% blocked",
				inky_display.WHITE,
				font=hanken_medium_font
			)
			y_placement = y_placement + 2
		else:
			draw.text((x_barrier, (y_placement * y_spacer)), "OFFLINE", inky_display.RED, font=hanken_medium_font)
			y_placement = y_placement + 1
	elif stage['type'] == 'linode':
		lindata = get_linode(stage['address'], stage['auth'])

		draw.text((2, (y_placement * y_spacer)), f"{stage['label']}:", inky_display.WHITE, font=hanken_medium_font)
		if lindata is not None:
			current   = time.time() * 1000
			timeframe = current - (7 * 60 * 60 * 1000) # 7 hours ago

			cpu_times  = [timestamp for timestamp, _ in lindata['data']['cpu'] if timestamp >= timeframe]
			cpu_totals = sum(value for timestamp, value in lindata['data']['cpu'] if timestamp >= timeframe)
			cpu_avg    = cpu_totals / len(cpu_times)

			io_times  = [timestamp for timestamp, _ in lindata['data']['io']['io'] if timestamp >= timeframe]
			io_totals = sum(value for timestamp, value in lindata['data']['io']['io'] if timestamp >= timeframe)
			io_avg    = io_totals / len(io_times)

			net_times  = [timestamp for timestamp, _ in lindata['data']['netv4']['out'] if timestamp >= timeframe]
			net_totals = sum(value for timestamp, value in lindata['data']['netv4']['out'] if timestamp >= timeframe)
			net_avg    = (net_totals / len(net_times)) / 1000

			draw.text(
				(x_barrier, (y_placement * y_spacer)),
				f"c{cpu_avg:.2f}% d{io_avg:.2f} n{net_avg:.2f}K/s",
				inky_display.WHITE,
				font=hanken_medium_font
			)
		else:
			draw.text((x_barrier, (y_placement * y_spacer)), "OFFLINE", inky_display.RED, font=hanken_medium_font)
		y_placement = y_placement + 1
	elif stage['type'] == 'isup':
		draw.text((2, (y_placement * y_spacer)), f"{stage['label']}:", inky_display.WHITE, font=hanken_medium_font)
		if is_device_online(stage['address']):
			draw.text((x_barrier, (y_placement * y_spacer)), "ONLINE", inky_display.WHITE, font=hanken_medium_font)
		else:
			draw.text((x_barrier, (y_placement * y_spacer)), "OFFLINE", inky_display.RED, font=hanken_medium_font)
		y_placement = y_placement + 1

inky_display.set_image(img)
inky_display.show()
