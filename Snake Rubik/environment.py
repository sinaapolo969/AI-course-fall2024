from math import radians, cos, sin
import heapq

from matplotlib import pyplot as plt

class SnakeRubikEnvironment:
    def __init__(self):
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
        self.glued_beads = {(5, 6), (12, 13), (14, 15), (16, 18), (18, 19)}
        self.state = self.beads.copy()

    def rotate(self, bead1, bead2, angle):
        if (bead1, bead2) in self.glued_beads or (bead2, bead1) in self.glued_beads:
            return
        if angle not in [90, -90, 180]:
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

        ax.set_xlim([-7, 7])
        ax.set_ylim([-7, 7])
        ax.set_zlim([-7, 7])

        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_zlabel('Z-axis')
        ax.set_title('Solved Snake Rubik Puzzle (3x3x3 Cube)')
        ax.grid(True)
        plt.show()


    def reset(self):
        self.state = self.beads.copy()

# class SnakeRubikAgent:
#     def __init__(self, environment):
#         self.environment = environment

#     def ucs(self):
#         """
#         Solve the Snake Rubik problem using Uniform-Cost Search (UCS).
#         Returns the solution as a list of moves.
#         """
#         # Priority queue for UCS
#         frontier = []
#         heapq.heappush(frontier, (0, tuple(sorted(self.environment.state.items())), []))  # (cost, serialized_state, path)

#         # Set to keep track of visited states
#         visited = set()

#         while frontier:
#             cost, serialized_state, path = heapq.heappop(frontier)

#             # Deserialize the state
#             current_state = dict(serialized_state)

#             if serialized_state in visited:
#                 continue

#             # Mark the state as visited
#             visited.add(serialized_state)

#             # Check if the goal is reached
#             self.environment.state = current_state  # Update the environment's state
#             if self.environment.is_solved():
#                 return path

#             # Expand the current state
#             for bead1, bead2 in self.get_valid_moves(current_state):
#                 for angle in [90, -90, 180]:
#                     new_state = self.apply_rotation(bead1, bead2, angle)
#                     self.environment.plot_states()
#                     serialized_new_state = tuple(sorted(new_state.items()))

#                     if serialized_new_state not in visited:
#                         new_cost = cost + 1

#                         new_path = path + [(bead1, bead2, angle)]
#                         heapq.heappush(frontier, (new_cost, serialized_new_state, new_path))

#         return None 


#     def get_valid_moves(self, state):
#         """
#         Get valid bead pairs that can be rotated.
#         """
#         valid_moves = []
#         for bead1 in state:
#             for bead2 in state:
#                 if bead1 != bead2 and (bead1, bead2) not in self.environment.glued_beads and \
#                         (bead2, bead1) not in self.environment.glued_beads and self.environment.get_shared_axis(bead1, bead2) != None:
#                     valid_moves.append((bead1, bead2))
#         return valid_moves

#     def apply_rotation(self, bead1, bead2, angle):
#         """
#         Apply rotation on a copy of the state and return the new state.
#         """
#         self.environment.rotate(bead1, bead2, angle)
#         return self.environment.state.copy()


class SnakeRubikAgent:
    def __init__(self, environment):
        self.environment = environment
        self.goal_positions = {i: pos for i, pos in enumerate(self.environment.solution_vals, 1)}

    def heuristic(self, state):
        """
        Heuristic function: Calculate the Manhattan distance
        between the current positions and the goal positions.
        """
        total_sum = 0
        for bead, position in state.items():
            goal_position = self.goal_positions[bead]
            total_sum += sum(abs(a - b) for a, b in zip(position, goal_position))
        return total_sum

    def apply_rotation(self, bead1, bead2, angle):
        """
        Apply rotation and return the new state as a hashable tuple.
        """
        self.environment.rotate(bead1, bead2, angle)

    def get_valid_moves(self, state):
        """
        Get valid bead pairs that can be rotated.
        """
        valid_moves = []
        for bead1 in state:
            for bead2 in state:
                if bead1 != bead2 and (bead1, bead2) not in self.environment.glued_beads and \
                        (bead2, bead1) not in self.environment.glued_beads and self.environment.get_shared_axis(bead1, bead2) != None \
                            and abs(bead1 - bead2) == 1:
                    valid_moves.append((bead1, bead2))
        return valid_moves

    def a_star(self):
        """
        Solve the Snake Rubik problem using A* Search.
        Returns the solution as a list of moves.
        """
        # Priority queue for A* (cost + heuristic, serialized_state, path)
        frontier = []
        initial_state = tuple(sorted(self.environment.state.values()))
        heapq.heappush(frontier, (0, initial_state, []))

        # Set to keep track of visited states
        visited = set()
        c = 0
        while frontier:
            f_cost, current_state, path = heapq.heappop(frontier)

            if current_state in visited:
                continue

            # Mark the state as visited
            visited.add(current_state)

            # Check if the goal is reached
            self.environment.state = {i + 1: pos for i, pos in enumerate(current_state)}
            if self.environment.is_solved():
                return path

            # Expand the current state
            possible_moves = self.get_valid_moves(self.environment.state)
            for bead1, bead2 in possible_moves:
                for angle in [90, -90, 180]:
                    self.apply_rotation(bead1, bead2, angle)
                    serialized_new_state = tuple(sorted(self.environment.state.values()))
                    if self.environment.state.values() not in visited:
                        # Calculate costs
                        g_cost = len(path) + 1  # Actual cost to reach this state
                        h_cost = self.heuristic(self.environment.state)  # Heuristic cost
                        f_cost = g_cost + h_cost

                        # Add the new state to the frontier
                        new_path = path + [(bead1, bead2, angle)]
                        heapq.heappush(frontier, (f_cost, serialized_new_state, new_path))
            c += 1
            if c % 1000 == 0:
                print(self.environment.plot_states())
        return None  # No solution found
   

# Example usage
env = SnakeRubikEnvironment()
agent = SnakeRubikAgent(env)


solution = agent.a_star()

if solution:
    print("Solution found!")
    for move in solution:
        bead1, bead2, angle = move
        print(f"Rotate bead {bead1} and bead {bead2} by {angle}°")
else:
    print("No solution found.")