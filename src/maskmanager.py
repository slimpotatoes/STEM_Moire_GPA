# Module Mask Manager
from matplotlib.patches import Circle
import matplotlib.artist as artist
import matplotlib.pyplot as plt
import math

class MaskCreator(object):

    def __init__(self, axis, image):
        """add when needed"""
        self.axis = axis
        self.image = image
        self.circle = None


    def connect(self):
        """connect for future use"""

    def disconnect(self):
        """disconnect for future use"""

    def make_circle(self, colored='r', off_center=(0,0)):
        self.colored = colored
        self.off_center = off_center
        """Create circle gui object"""
        print(self.image.shape)
        print(self.image.shape[0])
        print(self.image.shape[1])
        self.circle = Circle((self.image.shape[0]/2 + self.off_center[0], self.image.shape[1]/2+self.off_center[1]),
                             self.image.shape[0]/6, color=self.colored, fill=False, alpha=0.3)
        self.axis.add_artist(self.circle)
        self.axis.figure.canvas.draw()
        return artist.Artist.get_gid(self.circle), self.axis

class MaskEditor(object):

    def __init__(self, artist):
        self.artist = artist
        self.press = None

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.artist.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.artist.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.artist.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over the artist and store some data'
        if event.inaxes != self.artist.axes: return

        contains, attrd = self.artist.contains(event)
        if not contains:
            self.artist.fill = True
            return
        print('event contains', self.artist.axes)
        (x0, y0) = self.artist.center
        self.press = x0, y0, event.xdata, event.ydata
        self.artist.fill = False
        self.artist.figure.canvas.draw()

    def on_motion(self, event):
        'on motion we will move the artist if the mouse is over us'
        if self.press is None: return
        if event.inaxes != self.artist.axes: return

        if event.button == 1:
            x0, y0, xpress, ypress = self.press
            dx = event.xdata - xpress
            dy = event.ydata - ypress
        #print('x0=%f, xpress=%f, event.xdata=%f, dx=%f, x0+dx=%f' %
        #      (x0, xpress, event.xdata, dx, x0+dx))
            self.artist.center = x0 + dx, y0 + dy

        if event.button == 3:
            x0, y0, xpress, ypress = self.press
            R = math.sqrt((event.xdata-x0) ** 2 + (event.ydata-y0) ** 2)
            print(R)
        #print('x0=%f, xpress=%f, event.xdata=%f, dx=%f, x0+dx=%f' %
        #      (x0, xpress, event.xdata, dx, x0+dx))
            self.artist.set_radius(R)

        self.artist.figure.canvas.draw()


    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.artist.figure.canvas.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.artist.figure.canvas.mpl_disconnect(self.cidpress)
        self.artist.figure.canvas.mpl_disconnect(self.cidrelease)
        self.artist.figure.canvas.mpl_disconnect(self.cidmotion)
