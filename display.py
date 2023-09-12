from picographics import PicoGraphics, DISPLAY_INKY_PACK

class Display:
    def __init__(self):
        self.display = PicoGraphics(display=DISPLAY_INKY_PACK)
        self.display.set_update_speed(2)
        self.display.set_font("bitmap8")
        self.line = 1
        self.x_barrier = 80
        self.y_spacer = 16
    
    # display.set_pen(15) is white and display.set_pen(0) is black
    
    def clear(self, invert = False):
        self.line = 1
        self.display.set_pen(0 if invert else 15)
        self.display.clear()
    
    def commit(self):
        self.display.update()
    
    def quick_text(self, text):
        self.clear()
        self.display.set_pen(0)
        self.display.text(text, 10, 10, 240, 3)
        self.display.update()

    def write_line(self, title, text):
        self.display.set_pen(15)
        self.display.text(title, 2, (self.line * self.y_spacer), 240, 2, 0, True)
        self.display.text(text, self.x_barrier, (self.line * self.y_spacer), 240, 2, 0, True)
        
        self.line = self.line + 1
    