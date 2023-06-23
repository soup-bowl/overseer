#!/usr/bin/env python3

import sys, subprocess, requests, json

from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
from inky.auto import auto

def format_number(num):
	num = num.replace(',', '')
	value = int(num)
	if value >= 1000000:
		return f"{value/1000000:.1f}M"
	elif value >= 1000:
		return f"{value/1000:.1f}K"
	else:
		return str(value)

def get_pihole():
	try:
		response = requests.get("http://swan.dharma:54321/admin/api.php?auth=831d4b7d3a5ae74f6e17fd8ddf3c8a512e2c46ddd323c473c21d130cedd90d69&summary")
		response.raise_for_status()
	except requests.HTTPError as http_err:
		return None
	except Exception as err:
		return None

	return response.json()


pidata = get_pihole()

inky_display = auto(ask_user=True)
inky_display.set_border(inky_display.BLACK)

scale_size = 1.30
padding = -5

# Create a new canvas to draw on
img = Image.new("P", inky_display.resolution)
draw = ImageDraw.Draw(img)

hanken_bold_font = ImageFont.truetype(HankenGroteskBold, int(12 * scale_size))
hanken_medium_font = ImageFont.truetype(HankenGroteskMedium, int(10 * scale_size))

y_top = int(inky_display.height * (5.0 / 10.0))
y_bottom = y_top + int(inky_display.height * (4.0 / 10.0))

# Make the background black
for y in range(0, inky_display.height):
	for x in range(0, inky_display.width):
		img.putpixel((x, y), inky_display.BLACK)

draw.text(
	(2, (0 * 12)),
	"LP Network Information",
	inky_display.RED,
	font=hanken_medium_font
)

draw.text(
	(2, (1 * 12)),
	f"Pi Firewall:",
	inky_display.WHITE,
	font=hanken_medium_font
)
if pidata is not None:
	draw.text(
		(72, (1 * 12)),
		f"Block {format_number(pidata.get('ads_blocked_today'))}/{format_number(pidata.get('dns_queries_today'))}",
		inky_display.WHITE,
		font=hanken_medium_font
	)

	draw.text(
		(72, (2 * 12)),
		f"{pidata.get('ads_percentage_today')}% block rate",
		inky_display.WHITE,
		font=hanken_medium_font
	)
else:
	draw.text(
		(72, (1 * 12)),
		f"OFFLINE",
		inky_display.RED,
		font=hanken_medium_font
	)

inky_display.set_image(img)
inky_display.show()
