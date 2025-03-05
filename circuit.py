#!/usr/bin/env python3
import random
import argparse

# 0: {} => U False => se permiten j con D False (0,2,5,6,10,11,13,14)
# 1: {U,D} => U True => se permiten j con D True (1,3,4,7,8,9,12,15)
# 2: {L,R} => U False => igual que 0

# 3: {L,D} => U False
# 4: {R,D} => U False
# 5: {R,U} => U True
# 6: {L,U} => U True

# 7: {L,R,D} => U False
# 8: {L,U,D} => U True
# 9: {R,U,D} => U True
# 10: {L,R,U} => U True

# 11: {U} => U True
# 12: {D} => U False
# 13: {L} => U False
# 14: {R} => U False

# 15: {U,D,L,R} => U True

allowed_up = [
    [-1, 0, -1, 0, 0, -1, -1, 0, 0, 0, -1, -1, 0, -1, -1, 0],  # 0
    [ 0, 1,  0, 1, 1,  0,  0, 1, 1, 1,  0,  0, 1,  0,  0, 1],  # 1
    [-1, 0, -1, 0, 0, -1, -1, 0, 0, 0, -1, -1, 0, -1, -1, 0],  # 2
    [-1, 0, -1, 0, 0, -1, -1, 0, 0, 0, -1, -1, 0, -1, -1, 0],  # 3
    [-1, 0, -1, 0, 0, -1, -1, 0, 0, 0, -1, -1, 0, -1, -1, 0],  # 4
    [ 0, 1,  0, 1, 1,  0,  0, 1, 1, 1,  0,  0, 1,  0,  0, 1],  # 5
    [ 0, 1,  0, 1, 1,  0,  0, 1, 1, 1,  0,  0, 1,  0,  0, 1],  # 6
    [-1, 0, -1, 0, 0, -1, -1, 0, 0, 0, -1, -1, 0, -1, -1, 0],  # 7
    [ 0, 1,  0, 1, 1,  0,  0, 1, 1, 1,  0,  0, 1,  0,  0, 1],  # 8
    [ 0, 1,  0, 1, 1,  0,  0, 1, 1, 1,  0,  0, 1,  0,  0, 1],  # 9
    [ 0, 1,  0, 1, 1,  0,  0, 1, 1, 1,  0,  0, 1,  0,  0, 1],  # 10
    [ 0, 1,  0, 1, 1,  0,  0, 1, 1, 1,  0,  0, 1,  0,  0, 1],  # 11
    [-1, 0, -1, 0, 0, -1, -1, 0, 0, 0, -1, -1, 0, -1, -1, 0],  # 12
    [-1, 0, -1, 0, 0, -1, -1, 0, 0, 0, -1, -1, 0, -1, -1, 0],  # 13
    [-1, 0, -1, 0, 0, -1, -1, 0, 0, 0, -1, -1, 0, -1, -1, 0],  # 14
    [ 0, 1,  0, 1, 1,  0,  0, 1, 1, 1,  0,  0, 1,  0,  0, 1]   # 15
]

allowed_left = [
    [-1, -1,  0, -1,  0,  0, -1,  0, -1,  0,  0, -1, -1, -1,  0,  0],  # 0
    [-1, -1,  0, -1,  0,  0, -1,  0, -1,  0,  0, -1, -1, -1,  0,  0],  # 1
    [ 0,  0,  1,  0,  1,  1,  0,  1,  0,  1,  1,  0,  0,  0,  1,  1],  # 2
    [ 0,  0,  1,  0,  1,  1,  0,  1,  0,  1,  1,  0,  0,  0,  1,  1],  # 3
    [-1, -1,  0, -1,  0,  0, -1,  0, -1,  0,  0, -1, -1, -1,  0,  0],  # 4
    [-1, -1,  0, -1,  0,  0, -1,  0, -1,  0,  0, -1, -1, -1,  0,  0],  # 5
    [ 0,  0,  1,  0,  1,  1,  0,  1,  0,  1,  1,  0,  0,  0,  1,  1],  # 6
    [ 0,  0,  1,  0,  1,  1,  0,  1,  0,  1,  1,  0,  0,  0,  1,  1],  # 7
    [ 0,  0,  1,  0,  1,  1,  0,  1,  0,  1,  1,  0,  0,  0,  1,  1],  # 8
    [-1, -1,  0, -1,  0,  0, -1,  0, -1,  0,  0, -1, -1, -1,  0,  0],  # 9
    [ 0,  0,  1,  0,  1,  1,  0,  1,  0,  1,  1,  0,  0,  0,  1,  1],  # 10
    [-1, -1,  0, -1,  0,  0, -1,  0, -1,  0,  0, -1, -1, -1,  0,  0],  # 11
    [-1, -1,  0, -1,  0,  0, -1,  0, -1,  0,  0, -1, -1, -1,  0,  0],  # 12
    [ 0,  0,  1,  0,  1,  1,  0,  1,  0,  1,  1,  0,  0,  0,  1,  1],  # 13
    [-1, -1,  0, -1,  0,  0, -1,  0, -1,  0,  0, -1, -1, -1,  0,  0],  # 14
    [ 0,  0,  1,  0,  1,  1,  0,  1,  0,  1,  1,  0,  0,  0,  1,  1]   # 15
]


def possible_values(value, direction):
    arr = []
    if direction == "up":
        for i in range(0, 16):
            if allowed_up[value][i] != 0:
                arr.append(i)

    elif direction == "down":
        for i in range(0, 16):
            if allowed_up[i][value] != 0:
                arr.append(i)

    elif direction == "left":
        for i in range(0, 16):
            if allowed_left[value][i] != 0:
                arr.append(i)

    elif direction == "right":
        for i in range(0, 16):
            if allowed_left[i][value] != 0:
                arr.append(i)

    return(arr)

def new_empty_matrix(cols, rows):
    return [([0] * cols) for i in range(rows)]

def new_check_array(rows, cols):
    checks = [([0] * cols) for i in range(rows)]
    checks[0] = [1] * cols
    checks[len(checks) - 1] = [1] * cols
    for i in range(0, rows):
        checks[i][0] = 1
        checks[i][cols - 1] = 1

    checks[1][1] = 1
    checks[rows - 2][1] = 1
    checks[rows - 2][cols - 2] = 1
    checks[1][cols - 2] = 1
    return checks

def create_matrix(matrix):
    checks = new_check_array(len(matrix), len(matrix[0]))
    for i in range(1, len(matrix) - 1):
        for j in range(1, len(matrix[0]) - 1):
            if checks[i][j] != 1:
                possible_vals = []
                u = matrix[i-1][j]
                d = matrix[i+1][j]
                l = matrix[i][j-1]
                r = matrix[i][j+1]
                if checks[i-1][j] == 1:
                    possible_vals.append(possible_values(u, "down"))
                if checks[i+1][j] == 1:
                    possible_vals.append(possible_values(d, "up"))
                if checks[i][j-1] == 1:
                    possible_vals.append(possible_values(l, "right"))
                if checks[i][j+1] == 1:
                    possible_vals.append(possible_values(r, "left"))

                common_vals = []
                if len(possible_vals) > 1:
                    common_vals = set(possible_vals[0])
                    for s in possible_vals[1:]:
                        common_vals.intersection_update(s)
                    common_vals = list(common_vals)
                else:
                    common_vals = common_vals[0]

                if len(common_vals) > 0:
                    matrix[i][j] = random.choice(common_vals)
                else:
                    matrix[i][j] = random.randint(0, 15)
                
                checks[i][j] = 1
    return(matrix)

def svg_def(x, y):
    svg_header = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>"""
    svg_header += f"<svg width=\"{y*32}\" height=\"{x*32}\" viewBox=\"0 0 {y*32} {x*32}\" version=\"1.1\" id=\"svg1\">"""
    return svg_header

def svg_draw_tile(num, x, y):
    group = f"<g transform=\"translate({y*32},{x*32})\">"
    tile = ""
    stub_square = "<rect style=\"fill:none;stroke-width:6;paint-order:markers fill stroke\" width=\"32\" height=\"32\" x=\"0\" y=\"0\" />"
    match num:
        case 1:
            tile = """<path style="baseline-shift:baseline;display:inline;overflow:visible;vector-effect:none;paint-order:markers fill stroke;enable-background:accumulate;stop-color:#000000;stop-opacity:1" transform="scale(-1)" d="m -19,-32 h 5.999998 V 0 H -19 Z" />"""
        case 2:
            tile = """<path style="baseline-shift:baseline;display:inline;overflow:visible;vector-effect:none;paint-order:markers fill stroke;enable-background:accumulate;stop-color:#000000;stop-opacity:1" transform="rotate(90)" d="m 13.000001,-32 h 5.999998 V 0 h -5.999998 z" />"""
        case 3:
            tile = """<path d="m 0,13 v 6 c 7.2152356,0 13,5.784764 13,13 h 6 C 19,21.542124 10.457876,13 0,13 Z" style="paint-order:markers fill stroke" id="path8" />"""
        case 4:
            tile = """<path d="m 32,13 v 6 C 24.784764,19 19,24.784764 19,32 H 13 C 13,21.542124 21.542124,13 32,13 Z" style="paint-order:markers fill stroke" id="path8" />"""
        case 5:
            tile = """<path d="M 32,19 V 13 C 24.784764,13 19,7.215236 19,0 h -6 c 0,10.457876 8.542124,19 19,19 z" style="paint-order:markers fill stroke" id="path8" />"""
        case 6:
            tile = """<path d="M 19,0 H 13 C 13,7.215236 7.215236,13 0,13 v 6 C 10.457876,19 19,10.457876 19,0 Z" style="paint-order:markers fill stroke" id="path8" />"""
        case 7:
            tile = """<path d="M 32,13 C 25.29599,13 19.38386,16.512054 16,21.787109 12.61605,16.51255 6.7036399,13 -6.8563745e-8,13 v 6 C 7.2152399,19 13,24.784764 13,32 h 6 c 0,-7.215236 5.78477,-13.000001 13,-13 z" style="stroke-width:6;paint-order:markers fill stroke" id="path28" />"""
        case 8:
            tile = """<path d="M 19,32 C 19,25.29599 15.48795,19.38386 10.21289,16 15.48745,12.61605 19,6.7036401 19,2.3286998e-8 H 13 C 13,7.2152401 7.21524,13 0,13 v 6 c 7.21524,0 13,5.78477 13,13 z" style="stroke-width:6;paint-order:markers fill stroke" id="path28" />"""
        case 9:
            tile = """<path d="M 13,32 C 13,25.29599 16.51205,19.38386 21.78711,16 16.51255,12.61605 13,6.7036401 13,2.3286998e-8 h 6 C 19,7.2152401 24.78476,13 32,13 v 6 c -7.21524,0 -13,5.78477 -13,13 z" style="stroke-width:6;paint-order:markers fill stroke"/>"""
        case 10:
            tile = """<path d="M 31.999999,18.999999 C 25.29599,18.999999 19.38386,15.487945 16,10.212891 12.61605,15.487449 6.7036404,18.999999 7.25745e-7,18.999999 V 13 C 7.2152404,13 13,7.2152358 13,9.3148003e-8 h 6 C 19,7.2152358 24.78477,13.000001 31.999999,13 Z" style="stroke-width:6;paint-order:markers fill stroke" id="path28" />"""
        case 11:
            tile = """<path style="stroke-width:6;paint-order:markers fill stroke" d="m 16.00002,28.937495 c -7.1441594,0 -12.9999992,-5.855831 -12.9999992,-12.999999 0,-5.282468 3.2031155,-9.8574682 7.7597652,-11.8847643 l -0.0059,-0.011717 A 3.7752101,3.7752101 0 0 0 13.000021,0.60156256 V -0.0625 h 3 2.999999 v 0.66406256 a 3.7752101,3.7752101 0 0 0 2.246094,3.43945254 l -0.0059,0.011717 c 4.556649,2.0272961 7.759765,6.6022959 7.759765,11.8847639 0,7.144168 -5.85584,12.999999 -13.000001,12.999999 z m 0,-5.999999 c 3.901519,1e-6 6.999999,-3.098472 6.999999,-7 0,-3.901526 -3.09848,-6.999999 -6.999999,-6.999999 -3.90152,0 -6.9999995,3.098473 -6.9999995,6.999999 0,3.901528 3.0984795,7.000001 6.9999995,7 z" />"""
        case 12:
            tile = """<path id="path55" style="stroke-width:6;paint-order:markers fill stroke" d="m 16.000022,2.999998 c -7.1441598,0 -13,5.8558319 -13,13 0,5.282469 3.2031156,9.857469 7.759766,11.884766 l -0.0059,0.01172 a 3.7752104,3.7752104 0 0 1 2.246093,3.439453 V 32 h 3 3 v -0.664061 a 3.7752104,3.7752104 0 0 1 2.246094,-3.439452 l -0.0059,-0.01172 c 4.556647,-2.027299 7.759763,-6.602299 7.759763,-11.884768 0,-7.1441681 -5.85584,-13 -13,-13 z m 0,6.0000001 c 3.90152,-1.2e-6 7,3.0984719 7,6.9999999 0,3.901527 -3.09848,7 -7,7 -3.90152,0 -6.9999999,-3.098473 -6.9999999,-7 0,-3.901528 3.0984799,-7.0000011 6.9999999,-6.9999999 z" />"""
        case 13:
            tile = """<path id="path55" style="stroke-width:6;paint-order:markers fill stroke" d="m 28.999995,16.00002 c 0,-7.1441594 -5.855831,-12.9999991 -12.999999,-12.9999991 -5.282468,0 -9.8574682,3.2031153 -11.8847643,7.7597651 l -0.011717,-0.0059 A 3.7752101,3.7752101 0 0 1 0.66406256,13.000021 H 0 v 3 2.999999 h 0.66406256 a 3.7752101,3.7752101 0 0 1 3.43945254,2.246094 l 0.011717,-0.0059 c 2.0272961,4.556649 6.6022959,7.759765 11.8847639,7.759765 7.144168,0 12.999999,-5.85584 12.999999,-13.000001 z m -5.999999,0 c 1e-6,3.901519 -3.098472,6.999999 -7,6.999999 -3.901526,0 -6.999999,-3.09848 -6.999999,-6.999999 0,-3.90152 3.098473,-6.9999996 6.999999,-6.9999996 3.901528,0 7.000001,3.0984796 7,6.9999996 z" />"""
        case 14:
            tile = """<path id="path55" style="stroke-width:6;paint-order:markers fill stroke" d="m 2.9999966,16.000021 c 0,-7.1441606 5.8558323,-13.0000012 13.0000014,-13.0000012 5.282469,0 9.85747,3.2031159 11.884766,7.7597662 l 0.01172,-0.0059 a 3.7752107,3.7752107 0 0 0 3.439453,2.246094 H 32 v 3 3 h -0.664063 a 3.7752107,3.7752107 0 0 0 -3.439453,2.246094 l -0.01172,-0.0059 c -2.027296,4.55665 -6.602297,7.759766 -11.884766,7.759766 -7.1441691,0 -13.0000014,-5.855841 -13.0000014,-13.000003 z m 6.0000005,0 c -1.1e-6,3.90152 3.0984719,7 7.0000009,7 3.901527,0 7,-3.09848 7,-7 0,-3.901521 -3.098473,-7.0000006 -7,-7.0000006 -3.901529,0 -7.000002,3.0984796 -7.0000009,7.0000006 z" />"""
        case 15:
            tile = """<path id="path28" style="stroke-width:6;paint-order:markers fill stroke" d="M 13,0 C 13,7.2152361 7.2152402,13 0,13 v 6 c 7.2152402,0 13,5.784764 13,13 h 6 C 19,24.784764 24.78477,18.999999 32,19 V 13 C 24.78477,13.000001 19,7.2152361 19,0 Z m 3,10.212891 C 17.48785,12.53228 19.465385,14.51096 21.783203,16 19.465385,17.48904 17.48785,19.46772 16,21.787109 14.511334,19.466728 12.532315,17.489345 10.212891,16 12.532315,14.510655 14.511334,12.533272 16,10.212891 Z" />"""
        case _:
            tile = """"""
    return(group + tile + stub_square + "</g>")

def svg_generate(matrix):
    header = svg_def(len(matrix), len(matrix[0])) + "\n"
    file = ""
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            file = file + "\n" + svg_draw_tile(matrix[i][j], i, j)
    file += "\n"
    return(header + file + "\n" + "</svg>")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a circuit-like pattern.')
    parser.add_argument('-w', '--width')
    parser.add_argument('-t', '--height')
    parser.add_argument('filename') # positional argument
    args = parser.parse_args()

    matrix = create_matrix(new_empty_matrix(int(args.width), int(args.height)))

    svg = svg_generate(matrix)
    f = open(args.filename, "w")
    f.write(svg)
    f.close()
    exit(0)
