import cairo
from contextlib import contextmanager

from gi.repository import Gtk

@contextmanager
def saved(cr):
    cr.save()
    try:
        yield cr
    finally:
        cr.restore()

def Tree(cr, angle):
    cr.move_to(0, 0)
    cr.translate(0, -65)
    cr.line_to(0, 0)
    cr.stroke()
    cr.scale(0.72, 0.72)
    if angle > 0.12:
        for a in [-angle, angle]:
            with saved(cr):
                cr.rotate(a)
                Tree(cr, angle * 0.75)

def paint_tree(cr):
    # surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 280, 204)
    # cr = cairo.Context(surf)
    cr.translate(140, 203)
    cr.set_line_width(5)
    Tree(cr, 0.75)
    # surf.write_to_png('fractal-tree.png')

class MyWindow(Gtk.Window):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.init_ui()
        
    def init_ui(self):    
        darea = Gtk.DrawingArea()
        darea.connect("draw", self.on_draw)
        self.add(darea)
        self.set_title("GTK window")
        self.resize(280, 204)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def on_draw(self, wid, cr):
        # cr.set_source_rgb(0, 0, 0)
        # cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL,
        #     cairo.FONT_WEIGHT_NORMAL)
        # cr.set_font_size(40)
        # 
        # cr.move_to(10, 50)
        # cr.show_text("Disziplin ist Macht.")
        paint_tree(cr)

def main():
    app = MyWindow()
    Gtk.main()

if __name__ == "__main__":
    main()
