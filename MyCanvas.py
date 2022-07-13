import math
from tkinter import *
from tkinter.ttk import *


class MyCanvas(Canvas):
  def __init__(self, *args, **kwargs):
    Canvas.__init__(self, *args, **kwargs)

  # Draws a circle
  #   x,y: Center coordinates
  #   r: Circle radius
  def create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

  # Draws a rectangle
  #   x,y: Center coordinates
  #   w: width
  #   h: height
  def create_rect(self, x, y, w, h, **kwargs):
    return self.create_rectangle(x-(w/2), y-(h/2), x+(w/2), y+(h/2), **kwargs)

  # Draws a rectangle with rounded corners
  #   x,y: Center coordinates
  #   w: width
  #   h: height
  #   r: corner radius
  def create_round_rect(self, x, y, w, h, radius=25, **kwargs):
    x1 = x-(int(w)/2)
    x2 = x+(int(w)/2)
    y1 = y-(int(h)/2)
    y2 = y+(int(h)/2)
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    return self.create_polygon(points, smooth=True, **kwargs)

  def create_bezier(self, c1, c2, c3, c4, **kwargs):
    # Start x and y coordinates, when t = 0
    x_start = c1[0]
    y_start = c1[1]

    p = [c1, c2, c3, c4]

    # loops through
    line_ids = []
    n = 50
    for i in range(50):
      t = i / n
      x = (p[0][0] * (1-t)**3 + p[1][0] * 3 * t * (1-t)**2 + p[2][0] * 3 * t**2 * (1-t) + p[3][0] * t**3)
      y = (p[0][1] * (1-t)**3 + p[1][1] * 3 * t * (1-t)**2 + p[2][1] * 3 * t**2 * (1-t) + p[3][1] * t**3)

      line_ids.append(self.create_line(x, y, x_start, y_start, fill='#90A4AE', width=1.5, smooth=1, **kwargs))
      # updates initial values
      x_start = x
      y_start = y

    return line_ids

  def delete_bezier(self, ids):
    for i in ids:
      self.delete(i)

  # Returns the distance between two points, n=2
  #   x1,y1: Point 1
  #   x2,y2: Point 2
  def get_distance(self, x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)