#!/usr/bin/env python3

import os, sys, subprocess, requests, json

from dotenv import load_dotenv
from pysnmp.hlapi import *
from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
from inky.auto import auto

def format_number(num):
	num = num.replace(',', '').replace('.', '')
	value = int(num)
	if value >= 1000000:
		return f"{value/1000000:.1f} M"
	elif value >= 1000:
		return f"{value/1000:.1f} K"
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

def get_pihole():
	try:
		response = requests.get(f"http://swan.dharma:54321/admin/api.php?auth={os.getenv('PIHOLE_KEY')}&summary")
		response.raise_for_status()
	except requests.HTTPError as http_err:
		return None
	except Exception as err:
		return None

	return response.json()

def get_snmp_data(host, community, oid):
	error_indication, error_status, error_index, var_binds = next(
		getCmd(SnmpEngine(), CommunityData(community), UdpTransportTarget((host, 161)), ContextData(), ObjectType(ObjectIdentity(oid)))
	)

	if error_indication or error_status:
		return None

	return var_binds[0][1]

load_dotenv()

pidata = get_pihole()

inky_display = auto(ask_user=True)
inky_display.set_border(inky_display.BLACK)

scale_size = 1.30
padding = -5

# Create a new canvas to draw on
img = Image.new("P", inky_display.resolution)
draw = ImageDraw.Draw(img)

hanken_bold_font = ImageFont.truetype(HankenGroteskBold, int(10 * scale_size))
hanken_medium_font = ImageFont.truetype(HankenGroteskMedium, int(10 * scale_size))

y_top = int(inky_display.height * (5.0 / 10.0))
y_bottom = y_top + int(inky_display.height * (4.0 / 10.0))
x_barrier = 50

# Make the background black
for y in range(0, inky_display.height):
	for x in range(0, inky_display.width):
		img.putpixel((x, y), inky_display.BLACK)

draw.text((2, (0 * 12)), "DHARMA NETWORK", inky_display.RED, font=hanken_bold_font)

draw.text((2, (1 * 12)), "Pihole:", inky_display.WHITE, font=hanken_medium_font)
if pidata is not None:
	blockrate = f"Block {format_number(pidata.get('ads_blocked_today'))}/{format_number(pidata.get('dns_queries_today'))}"
	blocknum  = f"{pidata.get('ads_percentage_today')}% block rate"
	draw.text((x_barrier, (1 * 12)), blockrate, inky_display.WHITE, font=hanken_medium_font)
	draw.text((x_barrier, (2 * 12)), blocknum, inky_display.WHITE, font=hanken_medium_font)
else:
	draw.text((x_barrier, (1 * 12)), "OFFLINE", inky_display.RED, font=hanken_medium_font)

servers = ["swan", "pearl", "orchid"]
for y in range(0, 3):
	pos = y + 3
	draw.text((2, (pos * 12)), f"{servers[y]}:", inky_display.WHITE, font=hanken_medium_font)
	if is_device_online(f"{servers[y]}.dharma"):
		draw.text((x_barrier, (pos * 12)), "ONLINE", inky_display.WHITE, font=hanken_medium_font)
	else:
		draw.text((x_barrier, (pos * 12)), "OFFLINE", inky_display.RED, font=hanken_medium_font)

draw.text((2, (6 * 12)), "tower:", inky_display.WHITE, font=hanken_medium_font)
if is_device_online(os.getenv('WATCHTOWER_ADDR')):
	draw.text((x_barrier, (6 * 12)), "ONLINE", inky_display.WHITE, font=hanken_medium_font)
else:
	draw.text((x_barrier, (6 * 12)), "OFFLINE", inky_display.RED, font=hanken_medium_font)

inky_display.set_image(img)
inky_display.show()
