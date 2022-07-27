# neighborhood.py
# defines functions which return lists of two element vectors "around"
# a two element vector with boundary conditions

def neumann(pos, width, height):
    neighbors = []

    if pos[0] > 0:
        neighbors.append([pos[0] - 1, pos[1]])
    
    if pos[0] < width - 1:
        neighbors.append([pos[0] + 1, pos[1]])

    if pos[1] > 0:
        neighbors.append([pos[0], pos[1] - 1])

    if pos[1] < height - 1:
        neighbors.append([pos[0], pos[1] + 1])

    return neighbors


def moore(pos, width, height):
    neighbors = []

    if pos[0] > 0:
        neighbors.append([pos[0] - 1, pos[1]])

        if pos[1] > 0:
            neighbors.append([pos[0] - 1, pos[1] - 1])

        if pos[1] < height - 1:
            neighbors.append([pos[0] - 1, pos[1] + 1])
    
    if pos[0] < width - 1:
        neighbors.append([pos[0] + 1, pos[1]])

        if pos[1] > 0:
            neighbors.append([pos[0] + 1, pos[1] - 1])

        if pos[1] < height - 1:
            neighbors.append([pos[0] + 1, pos[1] + 1])

    if pos[1] > 0:
        neighbors.append([pos[0], pos[1] - 1])

    if pos[1] < height - 1:
        neighbors.append([pos[0], pos[1] + 1])

    return neighbors