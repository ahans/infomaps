import sys
import math
import cairo
from gi.repository import Gtk
# import pygtk
# pygtk.require('2.0')
# import gtk
from optparse import OptionParser

def lambert(lambd, phi, lambda0 = 0):
  return (lambd, phi)

def read_mapdata(coords_file):
    country_coords = dict()
    code_map = dict()
    for l in open(coords_file).readlines():
        values = l.split("\t")
        code1, code2, name, num_parts, parts = values[0], values[1], values[2], int(values[3]), values[4:]
        coords = []
        for p in parts[:num_parts]:
            part_coords = [xy.split(",") for xy in p.split(";")]
            part_coords = [lambert(math.radians(float(xy[0])), math.radians(float(xy[1]))) for xy in part_coords]
            coords.append(part_coords)
        country_coords[name ] = coords
        code_map[name] = set()
        code_map[name].add(name)
        code_map[name].add(code1)
        code_map[name].add(code2)

    return country_coords, code_map

def read_countrycolors(colors_file):
    countrycolors = dict()
    for l in open(colors_file).readlines():
        v = l.split(";")
        country, r, g, b = v[0], float(v[1]), float(v[2]), float(v[3])
        countrycolors[country] = (r,g,b)
    return countrycolors


class MyWindow(Gtk.Window):
    def __init__(self, country_coords, code_map, country_colors):
        super(MyWindow, self).__init__()
        self.init_ui()
        self.country_coords = country_coords
        self.code_map = code_map
        self.country_colors = country_colors
        self.is_drawn = False
        
    def init_ui(self):    
        darea = Gtk.DrawingArea()
        darea.connect("draw", self.on_draw)
        self.add(darea)
        self.set_title("Choropleth Map")
        self.resize(800, 375)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def on_draw(self, wid, cr):
        width, height = self.get_size()
        if not self.is_drawn or width != self.w or height != self.h:
            self.bg_surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, width, height)
            ctx = cairo.Context(self.bg_surface)
            self.draw_countries(ctx)
            self.is_drawn = True
            self.w, self.h = width, height

        cr.set_source_surface(self.bg_surface, 0, 0)
        cr.paint()

    def on_resize(self, width, height):
        print("resized: %d %d" % (width, height))

    def draw_countries(self, cr):
        width, height = self.get_size()
        cr.rectangle(0, 0, width, height)
        cr.set_source_rgb(0.7, 0.7, 1.0)
        cr.fill()
        cr.set_source_rgb(0, 0, 0)
        cr.set_line_width(0.5)
        cr.translate(width/2, height/2 + height/12.0)
        scaler = width/(2*math.pi)
        for country in self.country_coords.keys():
            r = g = b = 1.0
            codes = self.code_map[country]
            for c in codes:
                if c in self.country_colors.keys():
                    r, g, b = self.country_colors[c]
                    print("found %s" % country)
                    break
            for coords in self.country_coords[country]:
                cr.move_to(coords[0][0]*scaler, -coords[0][1]*scaler)
                for c in coords[1:]:
                    cr.line_to(c[0]*scaler, -c[1]*scaler)
                cr.close_path()
                cr.set_source_rgb(r, g, b)
                cr.fill_preserve()
                cr.set_source_rgb(0,0,0)
                cr.stroke()

def main():
    parser = OptionParser()
    parser.add_option("--coords", dest="coords_file", type="string", help="file containing country coordinates")
    parser.add_option("--colors", dest="colors_file", type="string", help="file containing country colors")
    (options, args) = parser.parse_args()
    if not options.coords_file or not options.colors_file:
        parser.print_help()
        sys.exit(1)
    country_coords, code_map = read_mapdata(options.coords_file)
    app = MyWindow(country_coords, code_map, read_countrycolors(options.colors_file))
    Gtk.main()

if __name__ == "__main__":
    main()
