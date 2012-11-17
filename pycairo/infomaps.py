import math
import cairo
from contextlib import contextmanager

from gi.repository import Gtk

def lambert(lambd, phi, lambda0 = 0):
  return (lambd, phi)

def read_mapdata():
    country_coords = dict()
    for l in open('../asymptote/mapdata1.csv').readlines():
        values = l.split("\t")
        code1, code2, name, num_parts, parts = values[0], values[1], values[2], int(values[3]), values[4:]
        # print(code1)
        # print("%d == %d?" % (num_parts, len(parts)))
        # assert(num_parts == len(parts))
        coords = []
        for p in parts[:num_parts]:
            part_coords = [xy.split(",") for xy in p.split(";")]
            part_coords = [lambert(math.radians(float(xy[0])), math.radians(float(xy[1]))) for xy in part_coords]
            coords.append(part_coords)

        country_coords[name] = coords
    return country_coords

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

def draw_country(cr, country_coords):
    cr.set_line_width(1/100)
    # cr.move_to(0,0)
    # cr.line_to(10, 10)
    # cr.line_to(10, 50)
    # cr.line_to(100, 50)
    # cr.stroke()
    cr.scale(100, 100)
    cr.translate(1.5, 1.5)
    for coords in country_coords['Germany']:
        cr.move_to(coords[0][0], coords[0][1])
        for c in coords[1:]:
            print(c[0], c[1])
            cr.line_to(c[0], c[1])
        cr.stroke()

class MyWindow(Gtk.Window):
    def __init__(self, country_coords):
        super(MyWindow, self).__init__()
        self.init_ui()
        self.country_coords = country_coords
        
    def init_ui(self):    
        darea = Gtk.DrawingArea()
        darea.connect("draw", self.on_draw)
        self.add(darea)
        self.set_title("GTK window")
        self.resize(2800, 2040)
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
        # paint_tree(cr)
        draw_country(cr, self.country_coords)

def main():
    app = MyWindow(read_mapdata())
    Gtk.main()


if __name__ == "__main__":
    main()
