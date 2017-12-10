# Module Mask Manager that is used by GUI
from matplotlib.patches import Circle
import matplotlib.artist as artist
import math


class MaskCreator(object):

    def __init__(self, axis, image):
        self.axis = axis
        self.image = image
        self.circle = None
        self.colored = None
        self.off_center = None

    def make_circle(self, mask_id, colored='r', off_center=(0, 0)):
        self.colored = colored
        self.off_center = off_center
        """Create circle gui object"""
        self.circle = Circle((self.image.shape[0]/2 + self.off_center[0], self.image.shape[1]/2+self.off_center[1]),
                             self.image.shape[0]/6, color=self.colored, fill=True, alpha=0.3, linewidth=3)
        circle_artist = self.axis.add_artist(self.circle)
        circle_artist.set_gid(mask_id)
        self.axis.figure.canvas.draw()
        print(self.circle)
        return Circle.get_gid(self.circle), (self.circle.center, self.circle.radius),


class MaskEditor(object):

    def __init__(self, artist):
        self.artist = artist
        self.press = None
        self.mask_selected = None
        self.circle = None
        self.cidpress = None
        self.cidrelease = None
        self.cidmotion = None

    def connect(self):
        self.cidpress = self.artist.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.artist.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.artist.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.artist.axes:
            return
        contains, attrd = self.artist.contains(event)
        if not contains:
            self.artist.fill = True
            self.artist.figure.canvas.draw()
            self.mask_selected = None
            return
        (x0, y0) = self.artist.center
        self.press = x0, y0, event.xdata, event.ydata
        self.artist.fill = False
        self.artist.figure.canvas.draw()
        print(artist.Artist.get_gid(self.artist))
        self.mask_selected = artist.Artist.get_gid(self.artist)

    def on_motion(self, event):
        if self.press is None:
            return
        if event.inaxes != self.artist.axes:
            return
        if event.button == 1:
            x0, y0, xpress, ypress = self.press
            dx = event.xdata - xpress
            dy = event.ydata - ypress
            self.artist.center = x0 + dx, y0 + dy
        if event.button == 3:
            x0, y0, xpress, ypress = self.press
            r = math.sqrt((event.xdata-x0) ** 2 + (event.ydata-y0) ** 2)
            self.artist.set_radius(r)
        self.artist.figure.canvas.draw()

    def on_release(self, event):
        self.press = None
        self.artist.figure.canvas.draw()

    def disconnect(self):
        self.artist.figure.canvas.mpl_disconnect(self.cidpress)
        self.artist.figure.canvas.mpl_disconnect(self.cidrelease)
        self.artist.figure.canvas.mpl_disconnect(self.cidmotion)

    def disconnect_edit(self):
        self.artist.figure.canvas.mpl_disconnect(self.cidmotion)
