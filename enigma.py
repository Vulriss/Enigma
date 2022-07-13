## CONSTANTS
LETTER_LST = tuple(chr(x) for x in range(97, 123))
LETTER_DICO = {x: idx for (idx, x) in enumerate(LETTER_LST)}

## WIP
# import tkinter as tk
# front_panel_lab = ['q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'p', 'y', 'x',
#                    'c', 'v', 'b', 'n', 'm', 'l']

## You can create your own rotors here
# import random
# letter_list = [x for x in range(26)]
# random.shuffle(letter_list)
# letter_list

# Default ones
I = [13, 6, 9, 19, 7, 14, 0, 8, 11, 24, 2, 3, 15, 16, 25, 4, 17, 1, 18, 5, 20, 22, 10, 12, 21, 23]
II = [15, 12, 1, 6, 10, 25, 16, 17, 8, 20, 19, 21, 5, 18, 7, 9, 4, 23, 13, 14, 22, 24, 11, 3, 2, 0]
III = [7, 6, 0, 11, 18, 12, 3, 15, 19, 8, 9, 23, 25, 22, 10, 14, 4, 5, 24, 16, 1, 20, 13, 17, 21, 2]
IV = [23, 20, 14, 5, 6, 21, 25, 11, 7, 4, 15, 24, 9, 0, 16, 18, 13, 1, 10, 12, 3, 17, 8, 2, 22, 19]
V = [13, 0, 12, 21, 25, 8, 11, 2, 5, 7, 16, 18, 4, 17, 14, 20, 23, 19, 22, 6, 1, 15, 10, 24, 9, 3]

## You can create your own reflector here
# reflector = [255] * len(rotor_1)
# letter_list = [x for x in range(26)]
# random.shuffle(letter_list)
#
# i = 0
# while letter_list:
#     item = letter_list[0]
#
#     if item == i:
#         item = letter_list[1]
#
#     if i not in reflector:
#         reflector[i] = item
#         reflector[item] = i
#         letter_list.remove(i)
#         letter_list.remove(item)
#
#     i += 1
#
# for idx in range(len(reflector)):
#     print(idx, reflector[reflector[idx]])

# Default one
reflector = [20, 25, 14, 5, 16, 3, 19, 24, 18, 17, 11, 10, 22, 23, 2, 21, 4, 9, 8, 6, 0, 15, 12, 13, 7, 1]

## Usefull functions
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
rotor_list = [III, V, I]
init_pos = [12, 23, 4]

for idx in range(len(rotor_list)):
    rotor_list[idx] = turn_rotor(rotor_list[idx], init_pos[idx])

rev_rotor_list = generate_rev(rotor_list)

## Input message
input_msg = 'Hello World'
# input_msg = 'jpjttuubyg'

## Computing
input_msg = list(input_msg.replace(' ', '').lower())
input_msg = [LETTER_DICO[x] for x in input_msg]

out_msg = []
offset_val = [0, 0, 0]
offset_count = [0, 0, 0]

for letter in input_msg:
    _temp = reflector[rotor_list[2][rotor_list[1][rotor_list[0][letter]]]]
    out_chr = rev_rotor_list[0][rev_rotor_list[1][rev_rotor_list[2][_temp]]]
    out_msg.append(out_chr)

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

out_msg = [LETTER_LST[x] for x in out_msg]

## Output message
print(''.join(out_msg))