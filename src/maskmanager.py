# Module Mask Manager
from matplotlib.patches import Circle
import matplotlib.artist as artist
import matplotlib.pyplot as plt

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

    def make_circle(self):
        """Create circle gui object"""
        print(self.image.shape)
        print(self.image.shape[0])
        print(self.image.shape[1])
        self.circle = Circle((self.image.shape[0]/2, self.image.shape[1]/2), self.image.shape[0]/6, fill=True)
        self.axis.add_artist(self.circle)
        self.axis.figure.canvas.draw()
        return artist.Artist.get_gid(self.circle), self.axis

class MaskEditor(object):

    def __init__(self, rect):
        self.rect = rect
        self.press = None
        print('cest entre')

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.rect.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.rect.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.rect.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.rect.axes: return

        contains, attrd = self.rect.contains(event)
        if not contains: return
        print('event contains', self.rect.xy)
        x0, y0 = self.rect.xy
        self.press = x0, y0, event.xdata, event.ydata

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if self.press is None: return
        if event.inaxes != self.rect.axes: return
        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        #print('x0=%f, xpress=%f, event.xdata=%f, dx=%f, x0+dx=%f' %
        #      (x0, xpress, event.xdata, dx, x0+dx))
        self.rect.set_x(x0+dx)
        self.rect.set_y(y0+dy)

        self.rect.figure.canvas.draw()


    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.rect.figure.canvas.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)
