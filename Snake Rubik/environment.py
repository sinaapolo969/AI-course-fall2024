from math import radians, cos, sin
import heapq

from matplotlib import pyplot as plt
from copy import deepcopy

class SnakeRubikEnvironment:
    def __init__(self, sample=None, one_move=False):

        self.glued_beads = {(5, 6), (12, 13), (14, 15), (16, 18), (18, 19)}
        self.beads = {
            1: (-5, 2, -6),
            2: (-5, 2, -5),
            3: (-5, 2, -4),
            4: (-4, 2, -4),
            5: (-3, 2, -4),
            6: (-3, 2, -3),
            7: (-3, 2, -2),
            8: (-2, 2, -2),
            9: (-1, 2, -2),
            10: (-1, 2, -1),
            11: (0, 2, -1),
            12: (0, 2, 0),
            13: (0, 1, 0),
            14: (0, 0, 0),
            15: (1, 0, 0),
            16: (2, 0, 0),
            17: (2, 0, 1),
            18: (3, 0, 1),
            19: (3, 0, 2),
            20: (3, 0, 3),
            21: (4, 0, 3),
            22: (4, 0, 4),
            23: (4, 0, 5),
            24: (5, 0, 5),
            25: (5, 0, 6),
            26: (6, 0, 6),
            27: (7, 0, 6),
        }
        if sample and not one_move:
            self.beads = sample
            self.state = self.beads.copy()
        
        if one_move and sample:
            self.state = sample
            self.rotate(23, 24, 90)
            self.plot_states()

        self.solution = {
            1: (-1, 1, -1), # 1
            2: (0, 1, -1), # 2
            3: (1, 1, -1), # 3
            4: (1, 0, -1) , # 4
            5: (0, 0, -1), # 5
            6: (0, 0, 0), # 6
            7: (0, 0, 1), # 7
            8: (0, -1, 1), # 8
            9: (0, -1, 0), # 9
            10: (0, -1, -1), # 10   
            11: (1, -1, -1), # 11
            12: (1, -1, 0), # 12
            13: (1, 0, 0), # 13
            14: (1, 1, 0), # 14
            15: (0, 1, 0), # 15
            16: (-1, 1, 0), # 16
            17: (-1, 0, 0), # 17
            18: (-1, 0, -1), # 18
            19: (-1, -1, -1), # 19
            20: (-1, -1, 0), # 20
            21: (-1, -1, 1), # 21
            22: (-1, 0, 1), # 22
            23: (-1, 1, 1), # 23
            24: (0, 1, 1), # 24
            25: (1, 1, 1), # 25
            26: (1, 0, 1), # 26
            27: (1, -1, 1), # 27
        }
        self.solution_vals = set(self.solution.values())
        

    def rotate(self, bead1, bead2, angle):
        if (bead1, bead2) in self.glued_beads or (bead2, bead1) in self.glued_beads:
            return
        if angle not in [90, -90]:
            return
        axis = self.get_shared_axis(bead1, bead2)
        if not axis:
            return
        if bead2 > bead1:
            beads_to_rotate = [i for i in range(bead2, 28)]
            for bead in beads_to_rotate:
                self.state[bead] = self.rotate_point(self.state[bead], self.state[bead1], axis, angle)
        else:
            beads_to_rotate = [i for i in range(bead1, 0, -1)]
            for bead in beads_to_rotate:
                self.state[bead] = self.rotate_point(self.state[bead], self.state[bead2], axis, -angle)
        

    def get_shared_axis(self, bead1, bead2):
        x1, y1, z1 = self.state[bead1]
        x2, y2, z2 = self.state[bead2]
        dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
        if dx != 0 and dy == dz == 0:
            return 'x'
        elif dy != 0 and dx == dz == 0:
            return 'y'
        elif dz != 0 and dx == dy == 0:
            return 'z'
        return None

    def rotate_point(self, point, origin, axis, angle):
        angle = radians(angle)
        x, y, z = point
        ox, oy, oz = origin
        if axis == 'x':
            y, z = cos(angle)*(y - oy) - sin(angle)*(z - oz) + oy, sin(angle)*(y - oy) + cos(angle)*(z - oz) + oz
        elif axis == 'y':
            x, z = cos(angle)*(x - ox) + sin(angle)*(z - oz) + ox, -sin(angle)*(x - ox) + cos(angle)*(z - oz) + oz
        elif axis == 'z':
            x, y = cos(angle)*(x - ox) - sin(angle)*(y - oy) + ox, sin(angle)*(x - ox) + cos(angle)*(y - oy) + oy
        return (round(x), round(y), round(z))

    def get_neighbors(self, bead):
        neighbors = []
        for bead1 in self.solution.keys():
            if self.get_shared_axis(bead, bead1) != None:
                neighbors.append(bead1)
        return neighbors
    
    def is_solved(self):
        return self.solution_vals == set(self.state.values())

    def plot_states(self):
        points = list(self.state.values())
        x, y, z = zip(*points)

        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(x, y, z, c='blue', s=100)

        for i, (px, py, pz) in enumerate(points, 1):
            ax.text(px, py, pz, f'{i}', color='red')

        ax.set_xlim([-4, 4])
        ax.set_ylim([-4, 4])
        ax.set_zlim([-4, 4])

        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_zlabel('Z-axis')
        ax.set_title('Solved Snake Rubik Puzzle (3x3x3 Cube)')
        ax.grid(True)
        plt.show()


    def reset(self):
        self.state = self.beads.copy()