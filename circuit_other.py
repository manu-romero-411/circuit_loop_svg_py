import random

def generate_tile():
    u = random.choice([0,1])
    d = random.choice([0,1])
    l = random.choice([0,1])
    r = random.choice([0,1])
    return(str(l) + str(d) + str(u) + str(r))

def get_left(tile):
    return tile[0]

def get_down(tile):
    return tile[1]

def get_up(tile):
    return tile[2]

def get_right(tile):
    return tile[3]

def set_left(tile, val):
    return (val + tile[1] + tile[2] + tile[3])

def set_down(tile, val):
    return (tile[0] + val + tile[2] + tile[3])

def set_up(tile, val):
    return (tile[0] + tile[1] + val + tile[3])

def set_right(tile, val):
    return (tile[0] + tile[1] + tile[2] + val)


def generate_circuit(rows, cols):
    matrix = [(["0000"] * cols) for i in range(rows)]
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if(check_edges(i, j, rows, cols)):
                matrix[i][j] = generate_tile()
    return matrix

def check_edges(rows, cols, max_rows, max_cols):
    if (rows == 1 and cols == 1) \
    or (rows == 1 and cols == max_cols - 1) \
    or (rows == max_rows - 1 and cols == 1) \
    or (rows == max_rows - 1 and cols == max_cols - 1) :
        return False
    return True


def fix(matrix):
    fix = [([0] * len(matrix[0])) for i in range(len(matrix))]
    found = False
    while(found == False):
        cost = 0
        for i in range(1, len(matrix) - 1):
            for j in range(1, len(matrix[0]) - 1):
                # Caso vertical superior (ya proporcionado)
                if get_down(matrix[i-1][j]) != get_up(matrix[i][j]):
                    cost += 1
                    if fix[i-1][j] == 1:
                        set_down(matrix[i-1][j], get_up(matrix[i][j]))
                    else:
                        if random.choice(["0", "1"]) == matrix[i][j]:
                            set_down(matrix[i-1][j], get_up(matrix[i][j]))
                            fix[i-1][j] = 1
                        else:
                            set_up(matrix[i][j], get_down(matrix[i-1][j]))
                            fix[i][j] = 1

                # Caso horizontal izquierda (ya proporcionado)
                if get_right(matrix[i][j-1]) != get_left(matrix[i][j]):
                    cost += 1
                    if fix[i][j-1] == 1:
                        set_right(matrix[i][j-1], get_left(matrix[i][j]))
                    else:
                        if random.choice(["0", "1"]) == matrix[i][j]:
                            set_right(matrix[i][j-1], get_left(matrix[i][j]))
                            fix[i][j-1] = 1
                        else:
                            set_left(matrix[i][j], get_right(matrix[i][j-1]))
                            fix[i][j] = 1

                # Caso vertical inferior (completo)
                if get_up(matrix[i+1][j]) != get_down(matrix[i][j]):
                    cost += 1
                    if fix[i+1][j] == 1:
                        set_up(matrix[i+1][j], get_down(matrix[i][j]))
                    else:
                        if random.choice(["0", "1"]) == matrix[i][j]:
                            set_up(matrix[i+1][j], get_down(matrix[i][j]))
                            fix[i+1][j] = 1
                        else:
                            set_down(matrix[i][j], get_up(matrix[i+1][j]))
                            fix[i][j] = 1

                # Caso horizontal derecha (completo)
                if get_left(matrix[i][j+1]) != get_right(matrix[i][j]):
                    cost += 1
                    if fix[i][j+1] == 1:
                        set_left(matrix[i][j+1], get_right(matrix[i][j]))
                    else:
                        if random.choice(["0", "1"]) == matrix[i][j]:
                            set_left(matrix[i][j+1], get_right(matrix[i][j]))
                            fix[i][j+1] = 1
                        else:
                            set_right(matrix[i][j], get_left(matrix[i][j+1]))
                            fix[i][j] = 1
        print(cost)
        if cost == 0:
            found = True
    return matrix

aa = generate_circuit(32,18)
print(fix(aa))
