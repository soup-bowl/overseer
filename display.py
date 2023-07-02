from pysnmp.hlapi import *
from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from inky.auto import auto

class Display():
	def __init__(self, title):
		self.line = 1
		self.inky_display = auto(ask_user=True)
		self.inky_display.set_border(self.inky_display.BLACK)
		self.img = Image.new("P", self.inky_display.resolution)
		self.draw = ImageDraw.Draw(self.img)

		self.scale_size = 1.30
		self.hanken_bold_font = ImageFont.truetype(HankenGroteskBold, int(13 * self.scale_size))
		self.hanken_medium_font = ImageFont.truetype(HankenGroteskBold, int(13 * self.scale_size))

		self.y_top = int(self.inky_display.height * (5.0 / 10.0))
		self.y_bottom = self.y_top + int(self.inky_display.height * (4.0 / 10.0))
		self.x_barrier = 60
		self.y_spacer = 13

		for y in range(0, self.inky_display.height):
			for x in range(0, self.inky_display.width):
				self.img.putpixel((x, y), self.inky_display.BLACK)

		self.draw.text((2, 0), title, self.inky_display.RED, font=self.hanken_bold_font)
	
	def write_line(self, title = None, text = None, color = False):
		self.draw.text(
			(2, (self.line * self.y_spacer)),
			f"{title}:" if title is not None else "",
			self.inky_display.WHITE, 
			font=self.hanken_medium_font
		)
		
		self.draw.text(
			(self.x_barrier, (self.line * self.y_spacer)),
			text if text is not None else "",
			self.inky_display.RED if color else self.inky_display.WHITE,
			font=self.hanken_medium_font
		)

		self.line = self.line + 1

	def done(self):
		self.inky_display.set_image(self.img)
		self.inky_display.show()
