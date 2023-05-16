import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

import sys
import cairo
import random

USAGE = """\
Visual representation of Perceptron learning process for Logic gates.

{} <gate> <rand>
  <gate> - Logic gate (OR, AND, XOR or NAND).
  <rand> - Number of random noisy additional samples per input.\
"""

X_OR = [(0, 0), (0, 1), (1, 0), (1, 1)]
Y_OR = [0, 1, 1, 1]
X_AND = [(0, 0), (0, 1), (1, 0), (1, 1)]
Y_AND = [0, 0, 0, 1]
X_XOR = [(0, 0), (0, 1), (1, 0), (1, 1)]
Y_XOR = [0, 1, 1, 0]
X_NAND = [(0, 0), (0, 1), (1, 0), (1, 1)]
Y_NAND = [1, 1, 1, 0]

X = [X_OR, X_AND, X_XOR, X_NAND]
Y = [Y_OR, Y_AND, Y_XOR, Y_NAND]
I = {"OR": 0, "AND": 1, "XOR": 2, "NAND": 3}

def f_step(value):
    """
    """
    if value > 0:
        return 1.0
    return 0.0

def f_rand():
    """
    """
    return 2 * random.random() - 1

class Perceptron2D:
    """
    """
    def __init__(self, X, Y, learning_rate=0.01, bias=1.0):
        """
        """
        self.training_set = X
        self.desired_set = Y
        self.set_size = len(self.training_set)
        self.bias = bias
        self.weights = [-0.5, 0.0, 1.0]
        self.f_activation = f_step
        self.learning_rate = learning_rate
        self.count = 0
        self.change = 1.0

    def rand_weights(self):
        """
        """
        self.change = 1.0
        self.weights = [f_rand(), f_rand(), f_rand()]

    def learn(self):
        """
        """
        w0, w1, w2 = self.weights
 
        order = random.sample(list(range(self.set_size)), self.set_size)
        self.change = 0.0
        for i in order:
            x1, x2 = self.training_set[i]
            d = self.desired_set[i]
 
            y = self.f_activation((w0 * self.bias) + (x1 * w1) + (x2 * w2))
 
            if d != y:
                self.change = 1.0
 
            w0 = w0 + self.learning_rate * (d - y) * self.bias
            w1 = w1 + self.learning_rate * (d - y) * x1
            w2 = w2 + self.learning_rate * (d - y) * x2

        self.weights = [w0, w1, w2]
        self.count = self.count + 1

class Plot2DBoundary(Gtk.Window):
    """
    """
    def __init__(self, neuron, write_to_file=False, width=256, height=256):
        """
        """
        Gtk.Window.__init__(self)

        self.neuron = neuron
        self.width = width
        self.height = height
        self.refresh_rate = 1000 / 60
        self.write_to_file = write_to_file
        self.set_title("Perceptron")
        self.connect('destroy', Gtk.main_quit)
        self.set_default_size(self.width, self.height)

        # Create a DrawingArea, add it to the window, and connect it to the
        # `on_draw` function
        self.drawing_area = Gtk.DrawingArea()
        self.add(self.drawing_area)
        self.drawing_area.connect('draw', self.on_draw)

        # Add a button pressed event, and connect it to the `on_mouse_pressed`
        # callback
        self.drawing_area.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.drawing_area.connect('button-press-event', self.on_mouse_pressed)
 
        # Tell the drawing area to render
        self.drawing_area.queue_draw()
        GLib.timeout_add(self.refresh_rate, self.refresh_screen)
 
        # Show the window
        self.show_all()
        Gtk.main()
 
    def refresh_screen(self):
        """
        """
        if self.neuron.change == 1.0:
            self.neuron.learn()
            if self.write_to_file:
                self.save_drawing_to_file("%05d" % (self.neuron.count))
        self.drawing_area.queue_draw()
        GLib.timeout_add(self.refresh_rate, self.refresh_screen)

    def draw(self, context, width, height):
        """
        This is the draw function, that will be called every time `queue_draw`
        is called on the drawing area. Currently, this is setup to be every
        frame, 60 times per second.
        
        Ported from the first example here, with minimal changes:
        https://www.cairographics.org/samples/
        context - cairo.Context
        """
        w0, w1, w2 = self.neuron.weights
    
        context.set_source_rgb(0.6, 0.6, 0.6)
        context.rectangle(0, 0, 256, 256)
        context.fill()
    
        context.set_source_rgb(1.0, 1.0, 1.0)
        context.rectangle(28, 28, 200, 200)
        context.fill()
    
        for i in range(self.neuron.set_size):
            x1, x2 = self.neuron.training_set[i]
            d = self.neuron.desired_set[i]
            context.set_source_rgb(d, 0.0, 0.0)
            context.rectangle(28 + 200 * x1 - 5, 28 + 200 * x2 - 5, 10, 10)
            context.fill()
    
        slope = -(w1 / w2)
        delta = -(w0 / w2) * self.neuron.bias
    
        context.set_source_rgb(self.neuron.change, 1.0, 0.0)
        xo, yo = 28 - 1 * 200, 28 + 200 * (-1 * slope + delta)
        xd, yd = 28 + 2 * 200, 28 + 200 * (2 * slope + delta)
        context.move_to(xo, yo)
        context.line_to(xd, yd)
        context.stroke()
    
    def on_draw(self, drawing_area, context):
        """
        A callback called every time `drawing_area.queue_draw` is called.
        area - Gtk.DrawingArea
        context - cairo.Context
        """
        allocation = drawing_area.get_allocation()
        width = allocation.width
        height = allocation.height
    
        self.draw(context, width, height)
    
    def on_mouse_pressed(self, drawing_area, event, *data):
        """
        This is called when the mouse is pressed
        """
        self.neuron.rand_weights()

    def save_drawing_to_file(self, file_name):
        """
        """
        allocation = self.drawing_area.get_allocation()

        self.drawing_area.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                                       allocation.width,
                                                       allocation.height)

        context = cairo.Context(self.drawing_area.surface)

        context.rectangle(0, 0, allocation.width, allocation.height)
        context.set_source_rgb(1.0, 1.0, 1.0)
        context.fill()

        self.draw(context, allocation.width, allocation.height)

        self.drawing_area.surface.write_to_png(file_name + ".png")

        self.drawing_area.surface.flush()
        self.drawing_area.surface.finish()

if __name__ == '__main__':
    """
    """
    if len(sys.argv) == 3:
        gate = sys.argv[1]
        rand = int(sys.argv[2])
        xset = X[I[gate]]
        yset = Y[I[gate]]
        while rand > 0:
            for i in range(4):
                x1, x2 = xset[i]
                x1 = x1 + f_rand() / 3.6
                x2 = x2 + f_rand() / 3.6
                xset.append((x1, x2))
                yset.append(yset[i])
            rand = rand - 1
        neuron = Perceptron2D(xset, yset)
        window = Plot2DBoundary(neuron)
    else:
        print(USAGE.format(sys.argv[0]))
