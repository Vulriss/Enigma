import os, math
from tkinter import *
from tkinter.ttk import *
from functools import partial
from MyCanvas import *
from Node import *


CANVAS_WIDTH = 500
CANVAS_HEIGHT = 150

class PlugboardFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.move_pos = ()
        self.nodes = []
        self.draw = False
        self.from_io = None
        self.to_io = None
        self.active_link = []
        self.current_bezier = None

        graph_frame = Frame(self, relief='raise', borderwidth=1)
        graph_frame.pack(side=BOTTOM, fill=BOTH, expand=YES)

        self.canvas = MyCanvas(graph_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='#141414')
        self.canvas.pack()

        front_panel_lab = [['q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o'], ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k'], ['p',
                            'y', 'x', 'c', 'v', 'b', 'n', 'm', 'l']]

        out_chunk_nb, in_chunk_nb = 0, 0
        for chunk in front_panel_lab:
            in_chunk_nb = 0
            if out_chunk_nb == 1:
                for label in chunk:
                    self.nodes.append(Node(self.canvas, x=70 + 50*in_chunk_nb, y=25 + (out_chunk_nb*50), width=40,
                                            height=40, label=label.upper()))
                    in_chunk_nb += 1
            else:
                for label in chunk:
                    self.nodes.append(Node(self.canvas, x=50 + 50*in_chunk_nb, y=25 + (out_chunk_nb*50), width=40,
                                            height=40, label=label.upper()))
                    in_chunk_nb += 1
            out_chunk_nb += 1

        self.canvas.bind('<Button-1>', self.cb_click)
        self.canvas.bind("<ButtonRelease-1>", self.cb_release)

    def cb_click(self, evt):
        # Check for all nodes, if user clicked inside their geometries
        for node in self.nodes:
            io = node.io_interaction(evt) # returns io object, if user clicked inside an io port
            # user clicked inside io port
            if io:
                if not io['connected']:
                    self.draw = True
                    self.from_io = io
                    self.canvas.bind("<B1-Motion>", lambda event, n=node: self.cb_move(event, n))
                break
        # user clicked inside node
        # elif node.inbounds(evt):
        #     self.move_pos = (evt.x, evt.y)
        #     self.canvas.bind("<B1-Motion>", lambda event, n=node: self.cb_move(event, n))
        #     break

    def cb_release(self, event):
        if self.draw:
            for node in self.nodes:
                io = node.io_interaction(event)
                if io and io != self.from_io and not io['connected']:
                    self.from_io['connected'] = True
                    io['connected'] = True
                    # if self.from_io['type'] == 'input':
                    #     self.from_io['out'] = io
                    #     io['in'] = self.from_io
                    # else:
                    self.from_io['in'] = io
                    io['out'] = self.from_io
                    from_coords = self.canvas.coords(self.from_io['object'])
                    to_coords = self.canvas.coords(io['object'])
                    xFrom = from_coords[0]+5
                    yFrom = from_coords[1]+5
                    xTo = to_coords[0]+5
                    yTo = to_coords[1]+5
                    c1 = (xFrom, yFrom)
                    c2 = (xFrom+60, yFrom)
                    c3 = (xTo-60, yTo)
                    c4 = (xTo, yTo)
                    if self.to_io:
                        self.to_io = None
                    final_bezier = self.canvas.create_bezier(c1, c2, c3, c4)
                    self.from_io['bezier'] = final_bezier
                    io['bezier'] = final_bezier
                    # if self.from_io['type'] == 'input':
                    #     self.canvas.itemconfig(self.from_io['object'], fill='#D3382F')
                    # else:
                    #     self.canvas.itemconfig(self.from_io['object'], fill='#1E6DBA')
                    break
            if self.current_bezier:
                self.canvas.delete_bezier(self.current_bezier)
                self.current_bezier = None
            self.draw = False
        self.canvas.unbind("<B1-Motion>")
        self.active_link.append([self.from_io['ID'], self.from_io['in']['ID']])

    def cb_move(self, event, node):
        if self.draw:
            if self.current_bezier:
                self.canvas.delete_bezier(self.current_bezier)
            from_coords = self.canvas.coords(self.from_io['object'])
            xFrom = from_coords[0]+5
            yFrom = from_coords[1]+5
            xTo = event.x
            yTo = event.y
            c1 = (xFrom, yFrom)
            c2 = (xFrom+60, yFrom)
            c3 = (xTo-60, yTo)
            c4 = (xTo, yTo)
            self.current_bezier = self.canvas.create_bezier(c1, c2, c3, c4)
            self.from_io['bezier'] = self.current_bezier
            for n in self.nodes:
                if n == node:
                    continue
                io = n.io_interaction(event)
                # if user hovers over legal io port, we want to fill the port with active color
                if io and io != self.from_io and not io['connected']:
                    # if io['type'] == 'input':
                    #     self.canvas.itemconfig(io['object'], fill='#D3382F')
                    # else:
                    #     self.canvas.itemconfig(io['object'], fill='#1E6DBA')
                    self.to_io = io
                    return
            # if a port was filled due to hovering, but user left the port without releasing button
            if self.to_io:
                # if self.to_io['type'] == 'input':
                #     self.canvas.itemconfig(self.to_io['object'], fill='#E57373')
                # else:
                #     self.canvas.itemconfig(self.to_io['object'], fill='#90CAF9')
                self.to_io = None
        else:
            x = event.x - self.move_pos[0]
            y = event.y - self.move_pos[1]
            # node.move(x, y)
            for io in node.input:
                if io['connected']:
                    # if io['type'] == 'input':
                        # from_io = io['out']
                        # from_coords = self.canvas.coords(from_io['object'])
                        # to_coords = self.canvas.coords(io['object'])
                    # else:
                    from_io = io['in']
                    from_coords = self.canvas.coords(io['object'])
                    to_coords = self.canvas.coords(from_io['object'])
                    xFrom = from_coords[0]+5
                    yFrom = from_coords[1]+5
                    xTo = to_coords[0]+5
                    yTo = to_coords[1]+5
                    c1 = (xFrom, yFrom)
                    c2 = (xFrom+60, yFrom)
                    c3 = (xTo-60, yTo)
                    c4 = (xTo, yTo)
                    self.canvas.delete_bezier(io['bezier'])
                    new_bezier = self.canvas.create_bezier(c1, c2, c3, c4)
                    from_io['bezier'] = new_bezier
                    io['bezier'] = new_bezier
        self.move_pos = (event.x, event.y)

if __name__ == "__main__":
    root = Tk()
    root.iconphoto(False, PhotoImage(file='typewriter.png'))

    LETTER_LST = tuple(chr(x) for x in range(97, 123))
    LETTER_DICO = {x: idx for (idx, x) in enumerate(LETTER_LST)}

    I = [13, 6, 9, 19, 7, 14, 0, 8, 11, 24, 2, 3, 15, 16, 25, 4, 17, 1, 18, 5, 20, 22, 10, 12, 21, 23]
    II = [15, 12, 1, 6, 10, 25, 16, 17, 8, 20, 19, 21, 5, 18, 7, 9, 4, 23, 13, 14, 22, 24, 11, 3, 2, 0]
    III = [7, 6, 0, 11, 18, 12, 3, 15, 19, 8, 9, 23, 25, 22, 10, 14, 4, 5, 24, 16, 1, 20, 13, 17, 21, 2]
    IV = [23, 20, 14, 5, 6, 21, 25, 11, 7, 4, 15, 24, 9, 0, 16, 18, 13, 1, 10, 12, 3, 17, 8, 2, 22, 19]
    V = [13, 0, 12, 21, 25, 8, 11, 2, 5, 7, 16, 18, 4, 17, 14, 20, 23, 19, 22, 6, 1, 15, 10, 24, 9, 3]

    reflector = [20, 25, 14, 5, 16, 3, 19, 24, 18, 17, 11, 10, 22, 23, 2, 21, 4, 9, 8, 6, 0, 15, 12, 13, 7, 1]

    def generate_rev(rotor_list):
        rotor_len = len(rotor_list[0])
        rev_rotor_list = [[255] * rotor_len, [255] * rotor_len, [255] * rotor_len]
        for idx in range(len(rev_rotor_list)):
            for i in range(rotor_len):
                rev_rotor_list[idx][rotor_list[idx][i]] = i
        return rev_rotor_list


    def turn_rotor(rotor, value):
        return rotor[value:] + rotor[0:value]

    ## Machine inital parameters
    rotor_dic = {'I': I, 'II': II, 'III': III, 'IV': IV, 'V': V, '':None}

    def update_rotor():
        global rotor_list
        global rev_rotor_list
        global offset_count

        rotor_list = [rotor_dic[first_rot.get()], rotor_dic[second_rot.get()], rotor_dic[third_rot.get()]]
        offset_count = [first_pos.get(),second_pos.get(), third_pos.get()]
        if (None in rotor_list) or ('' in offset_count):
            return
        else:
            offset_count = [int(x) for x in offset_count]

        for idx in range(len(rotor_list)):
            rotor_list[idx] = turn_rotor(rotor_list[idx], offset_count[idx])

        rev_rotor_list = generate_rev(rotor_list)
        keyboard.config(state='normal')

    rotor_list_txt_ori = ["I", "II", "III", "IV", "V"]
    # rotor_list_txt = rotor_list_txt_ori

    def up_list(type):
        _temp = rotor_list_txt_ori
        try:
            _temp.remove(first_rot.get())
        except ValueError:
            pass
        try:
            _temp.remove(second_rot.get())
        except ValueError:
            pass
        try:
            _temp.remove(third_rot.get())
        except ValueError:
            pass

        type_list = [first_rot['values'], second_rot['values'], third_rot['values']]
        try:
            del type_list[type]

            if type == 0:
                second_rot['values'] = third_rot['values'] = _temp
            elif type == 1:
                first_rot['values'] = third_rot['values'] = _temp
            elif type == 2:
                second_rot['values'] = first_rot['values'] = _temp

            root.focus()
        except IndexError:
            pass

        update_rotor()

    rotor_frame = Frame(root)
    rotor_frame.grid(row=0, column=0, sticky='w')
    first_rot = Combobox(rotor_frame, state="readonly",takefocus=False, width=3, values=rotor_list_txt_ori)
    first_rot.grid(row=0, column=2)
    first_rot.bind("<<ComboboxSelected>>", lambda event, type=0: up_list(type))
    second_rot = Combobox(rotor_frame, state="readonly",takefocus=False, width=3, values=rotor_list_txt_ori)
    second_rot.grid(row=0, column=1)
    second_rot.bind("<<ComboboxSelected>>", lambda event, type=1: up_list(type))
    third_rot = Combobox(rotor_frame, state="readonly",takefocus=False, width=3, values=rotor_list_txt_ori)
    third_rot.grid(row=0, column=0)
    third_rot.bind("<<ComboboxSelected>>", lambda event, type=2: up_list(type))
    first_pos = Entry(rotor_frame, width=4)
    first_pos.grid(row=1, column=2, sticky='w')
    first_pos.bind("<KeyRelease>", lambda event, type=4: up_list(type))
    second_pos = Entry(rotor_frame, width=4)
    second_pos.grid(row=1, column=1, sticky='w')
    second_pos.bind("<KeyRelease>", lambda event, type=4: up_list(type))
    third_pos = Entry(rotor_frame, width=4)
    third_pos.grid(row=1, column=0, sticky='w')
    third_pos.bind("<KeyRelease>", lambda event, type=4: up_list(type))

    # Indicator

    light_panel_frame = Frame(root)
    light_panel_frame.grid(row=1, column=0)
    light_bulb = {}
    light_panel_lab = [['q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o'], ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k'], ['p',
                        'y', 'x', 'c', 'v', 'b', 'n', 'm', 'l']]

    out_chunk_nb, in_chunk_nb = 0, 0
    frame_for_light = [Frame(light_panel_frame), Frame(light_panel_frame), Frame(light_panel_frame)]
    frame_for_light[0].grid(row=0, column=0, sticky='news')
    frame_for_light[1].grid(row=1, column=0)
    frame_for_light[2].grid(row=2, column=0, sticky='news')
    for chunk in light_panel_lab:
        in_chunk_nb = 0
        for label in chunk:
            light_bulb[label] = Label(frame_for_light[out_chunk_nb], text=label.upper(), font=("Courier", 14))
            light_bulb[label].grid(row=out_chunk_nb, column=in_chunk_nb, padx=10)
            in_chunk_nb += 1
        out_chunk_nb += 1

    # light_bulb['a'].config(background="yellow")
    light_bulb['is_on'] = ''

    def txt_var_callback(event):
        global out_msg
        global offset_val
        global offset_count
        global rotor_list
        global rev_rotor_list

        try:
            key = keyboard.get("-1.0", END)[-2]

            _temp = reflector[rotor_list[2][rotor_list[1][rotor_list[0][LETTER_DICO[key]]]]]
            out_chr = rev_rotor_list[0][rev_rotor_list[1][rev_rotor_list[2][_temp]]]
            out_msg.append(LETTER_LST[out_chr])

            offset_count[0] += 1
            offset_val[0] = 1
            if (not offset_count[0] % 25) and (offset_count[0] != 0):
                offset_count[0] = 0
                offset_count[1] += 1
                offset_val[1] = 1
            if (not offset_count[1] % 25) and (offset_count[1] != 0):
                offset_count[1] = 0
                offset_count[2] += 1
                offset_val[2] = 1

            for k in range(3):
                rotor_list[k] = turn_rotor(rotor_list[k], offset_val[k])
                offset_val = [0, 0, 0]

            rev_rotor_list = generate_rev(rotor_list)

            try:
                light_bulb[out_msg[-1]].config(background="yellow")
            except KeyError:
                pass
            try:
                if out_msg[-1] != light_bulb['is_on']:
                    light_bulb[light_bulb['is_on']].config(background="#F0F0F0")
            except KeyError:
                pass
            light_bulb['is_on'] = out_msg[-1]
            position_entry = [first_pos, second_pos, third_pos]
            for idx in range(len(offset_count)):
                position_entry[idx].delete(0, END)
                position_entry[idx].insert(0, str(offset_count[idx]))

            print(''.join(out_msg))
        except IndexError:
            for item in list(light_bulb.keys())[:-1]:
                light_bulb[item].config(background="#F0F0F0")
            out_msg = []

        # print ("{}".format(keyboard.get("1.0", END)[-2]))

    out_msg = []
    offset_val = [0, 0, 0]

    keyboard = Text(root, width=40, height=4)
    keyboard.grid(row=2, column=0)
    keyboard.bind('<KeyRelease>', txt_var_callback)
    keyboard.config(state='disabled')

    plugboard = PlugboardFrame(root)
    plugboard.grid(row=3, column=0)

    root.title('Enigma')
    root.resizable(False, False)
    #root.geometry('800x600')
    root.mainloop()
