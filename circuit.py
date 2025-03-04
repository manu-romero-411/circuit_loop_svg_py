#!/usr/bin/env python3
from operator import index
from queue import Full
import random

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

def restrict_values(matrix):
    limit = 16
    for i in range(0,16):
        for j in range(0,limit):
            if allowed_up[i][j] == 0 or allowed_up[j][i] == 0:
                return(False)
            if allowed_left[i][j] == 0 or allowed_left[j][i] == 0:
                return(False)

    return(True)

def generate(rows,cols):
    matrix = [([0] * cols) for i in range(rows)]
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            matrix[i][j] = random.randint(0, 15)

    matrix[1][1] = 0
    matrix[1][cols-2] = 0
    matrix[rows-2][1] = 0
    matrix[rows-2][cols-2] = 0
    return(matrix)

def improve_func(matrix):
    optim = matrix

    for i in range(2, len(optim) - 1):
        for j in range(2, len(optim[0]) - 1):
            value = optim[i][j]

            # if dir == "u":
            posb_u = possible_values(value, "up")
            value_u = optim[i-1][j]
            if not value_u in posb_u:
                optim[i-1][j] = random.choice(posb_u)

            # if dir == "d":
            #     value_d = optim[i+1][j]
            #     posb_d = possible_values(value, "down")
            #     if not value_d in posb_d:
            #         optim[i+1][j] = random.choice(posb_d)            
            
            # if dir == "l":
            value_l = optim[i][j-1]
            posb_l = possible_values(value, "left")
            if not value_l in posb_l:
                optim[i][j-1] = random.choice(posb_l)
                
            # if dir == "r":
            #     value_r = optim[i][j+1]
            #     posb_r = possible_values(value, "right")
            #     if not value_r in posb_r:
            #         optim[i][j+1] = random.choice(posb_r)

    return(optim)

def mutatio(matrix, num_muts):
    rows = len(matrix)
    cols = len(matrix[0])
    matrix_new = None
    for i in range(0, num_muts):
        matrix_new = matrix
        rand_tile = random.randint(0, 15)
        rand_row = random.randint(0, rows)
        rand_col = random.randint(0, cols)
        matrix_new[rand_row - 1][rand_col - 1] = rand_tile
        posb_u = possible_values(rand_tile, "up")
        value_u = matrix_new[rand_row - 2][rand_col - 1]
        if not value_u in posb_u:
            matrix_new[rand_row - 2][rand_col - 1] = random.choice(posb_u)

        value_l = matrix_new[rand_row - 1][rand_col - 2]
        posb_l = possible_values(rand_tile, "left")
        if not value_l in posb_l:
            matrix_new[rand_row - 1][rand_col - 2] = random.choice(posb_l)
        print(cost(matrix_new))
        if cost(matrix_new) == 0:
            return(matrix_new)
    return(matrix_new)
 
def check_edges(rows, cols, max_rows, max_cols):
    if (rows == 1 and cols == 1) \
    or (rows == 1 and cols == max_cols - 1) \
    or (rows == max_rows - 1 and cols == 1) \
    or (rows == max_rows - 1 and cols == max_cols - 1) :
        return False
    return True
    

def cost(matrix):
    cost = 0
    for i in range(1, len(matrix) - 1):
        for j in range(1, len(matrix[0]) - 1):
            if(check_edges(i, j, len(matrix), len(matrix[0]))):
                posb_u = possible_values(matrix[i][j], "up")
                posb_d = possible_values(matrix[i][j], "down")
                posb_l = possible_values(matrix[i][j], "left")
                posb_r = possible_values(matrix[i][j], "right")

                if not matrix[i-1][j] in posb_u:
                    cost = cost + 1

                if not matrix[i+1][j] in posb_d:
                    cost = cost + 1

                if not matrix[i][j-1] in posb_l:
                    cost = cost + 1

                if not matrix[i][j+1] in posb_r:
                    cost = cost + 1
    return(cost)

#matrix = local_search(8, 8)

#sols = [generate(8,8) for i in range(0,9)]
#print(cost(sols[0]))

test = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 10, 13, 1, 15, 0, 0], [0, 2, 0, 0, 9, 8, 5, 0], [0, 9, 12, 12, 14, 5, 13, 0], [0, 1, 12, 9, 12, 4, 10, 0], [0, 13, 1, 12, 4, 2, 11, 0], [0, 0, 3, 8, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
tested = improve_func(test)
while(cost(tested) != 0):
    tested = mutatio(test, 3000)
    print(cost(tested))

print(cost(tested))
