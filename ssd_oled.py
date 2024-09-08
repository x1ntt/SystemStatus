import threading
import time
import json

from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont

from status import status

line_height = 8
margin_x = 3
font_default = ImageFont.truetype("/home/pi/luma.examples/examples/fonts/DejaVuSansMono.ttf", 10)
font_s = ImageFont.truetype("/home/pi/luma.examples/examples/fonts/DejaVuSansMono.ttf", 9)

def draw_text(draw, line_num, x, text, font=font_default):
	draw.text((x, line_num*line_height), text, fill="white", font=font)

def draw_bar(draw, line_num, percent, x_1, x_2):
	bar_width = x_2 - x_1
	bar_height = line_height-4
	y_1 = line_num*line_height+4
	draw.rectangle((x_1, y_1, x_2, y_1 + bar_height), outline="white")             
	draw.rectangle((x_1, y_1, x_1 + bar_width * percent / 100, y_1 + bar_height), fill="white")

class OledDisplay(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.running = True
		serial = i2c(port=1, address=0x3C)
		self.device = ssd1306(serial)
		self.active = True
		self.tasks = [
			{"time": [23,0,0], "active": False}, 
			{"time": [7,0,0], "active": True}
		]

	def switch_active(self, active):
		if active != self.active:
			self.active = active
			print (f"切换屏幕状态: {active}")
	
	def voiddisplay(self, draw):
		draw.rectangle(self.device.bounding_box, outline="white", fill="black")
		draw_text(draw, 0, margin_x, "Not Data")

	def disable_display(self, draw):
		print ("disable_display")

	def display(self, draw, node, cur_index, node_count):
		draw.rectangle(self.device.bounding_box, outline="white", fill="black")
		draw_text(draw, 0, margin_x-2, f"{node['ip']},{cur_index+1}/{node_count}")

		#draw_text(draw, 1, margin_x, f"Cpu:       {node['cpu']}%")
		draw_text(draw, 1, margin_x, f"Cpu:")
		draw_bar(draw, 1, node['cpu'], margin_x+25, 128-5)

		#draw_text(draw, 2, margin_x, f"Mem:       {node['mem']}%")
		draw_text(draw, 2, margin_x, f"Mem:")
		draw_bar(draw, 2, node['mem'], margin_x+25, 128-5)

		draw_text(draw, 3, margin_x, f"Disk: ")
		cnt = 0
		for disk in node['disk']:
			draw_text(draw, 4+cnt, margin_x+4, f"{disk['path']}", font_s)
			draw_bar(draw, 4+cnt, disk['percent'], margin_x+45, 128-5)
			cnt += 1

	def stop(self):
		self.running = False

	def check_task(self):
		t = time.localtime()
		for v in self.tasks:
			if v['time'][0] == t.tm_hour and v['time'][1] == t.tm_min and v['time'][2] == t.tm_sec:
				self.switch_active(v['active'])

	def run(self):
		cnt = 0
		cur_index = 0
		while self.running:
			s_ts = time.time()
			self.check_task()
			nodes = list(status.getall_node().values())
			with canvas(self.device) as draw:
				if self.active:
					node_count = len(nodes)
					if node_count != 0:
						if cnt > 6:
							cnt = 0
							cur_index += 1
						if cur_index >= node_count:	cur_index = 0
						self.display(draw, nodes[cur_index], cur_index, node_count)
						cnt += 1
					else:
						self.voiddisplay(draw)
				else:
					self.disable_display(draw);
			time.sleep(0.5)
			print (f"time: {time.time() - s_ts}")

oled_display = OledDisplay()

if __name__ == "__main__":
	oled_display.start()
	oled_display.join()
