#https://github.com/prjoh/NodeEditor

SPAWN_X = 100
SPAWN_Y = 100

class Node:
  def __init__(self, canvas, x=SPAWN_X, y=SPAWN_Y, width=140, height=90, label="New Node", **kwargs):
    self.canvas = canvas
    self.x = x
    self.y = y
    posX = self.x - width/2 + 12
    posY = self.y - height/2 - 4 + 15
    self.geometry = self.canvas.create_round_rect(self.x, self.y, width, height, fill='#444444', outline='black')
    self.label = self.canvas.create_text((posX, posY), text=label, fill='white')
    self.input = []

    # Node

    in_circle = {'object': self.canvas.create_circle(self.x, self.y+(height/4), 5, fill='#E57373', activefill='#D3382F'), 'connected': False, 'ID': label, 'linked': None, 'bezier': None}
    self.input.append(in_circle) # selected color: #1E6DBA


  def inbounds(self, event):
    node_bbox = self.canvas.bbox(self.geometry)
    if (node_bbox[0] < event.x and event.x < node_bbox[2] and
        node_bbox[1] < event.y and event.y < node_bbox[3]):
      return True
    return False

  def io_interaction(self, event):
    for io in self.input:
      io_bbox = self.canvas.bbox(io['object'])
      if (io_bbox[0] < event.x and event.x < io_bbox[2] and
          io_bbox[1] < event.y and event.y < io_bbox[3]):
        return io
    return None
