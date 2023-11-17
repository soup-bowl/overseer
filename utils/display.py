from utils.nettime import Time
from picographics import PicoGraphics, DISPLAY_INKY_PACK

class Display:
    def __init__(self, dark_mode = False):
        self.display = PicoGraphics(display=DISPLAY_INKY_PACK)
        self.display.set_update_speed(2)
        self.display.set_font("bitmap8")
        self.line = 1
        self.x_barrier = 70
        self.y_spacer = 16
        self.background = 0 if dark_mode else 15
        self.foreground = 15 if dark_mode else 0

    # display.set_pen(15) is white and display.set_pen(0) is black

    def clear(self):
        self.line = 1
        self.display.set_pen(self.background)
        self.display.clear()

    def commit(self):
        self.display.update()

    def inform_loading(self):
        self.display.set_update_speed(3)

        WIDTH, HEIGHT = self.display.get_bounds()

        self.display.set_pen(self.foreground)
        self.display.rectangle(0, HEIGHT - 14, WIDTH, 14)

        self.display.set_pen(self.background)
        self.display.text("Loading", 5, HEIGHT - 9, scale=1)

        self.commit()
        self.display.set_update_speed(2)

    def quick_text(self, text):
        self.clear()
        self.display.set_pen(self.foreground)
        self.display.text(text, 10, 10, 240, 3)
        self.display.update()

    def write_timestamp(self):
        self.display.set_pen(self.foreground)
        self.display.text(Time.get(), 4, 4, scale=1)

    def write_line(self, title, text, color = 15):
        processtext = text if type(text) == list else [text]

        count = 0
        for text_line in processtext:
            self.display.set_pen(self.foreground)
            self.display.text(title if count is 0 else "", 2, (self.line * self.y_spacer), 240, 2, 0, True)
            self.display.set_pen(self.foreground)
            self.display.text(text_line, self.x_barrier, (self.line * self.y_spacer), 240, 2, 0, True)

            self.line += 1
            count += 1
