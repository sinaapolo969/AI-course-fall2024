import heapq

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
            total_sum += ((position[0] - goal_position[0]) ** 2 + (position[1] - goal_position[1]) ** 2 + (position[2] - goal_position[2]) ** 2) ** 0.5
        return total_sum

    def apply_rotation(self, bead1, bead2, angle):
        """
        Apply rotation on a copy of the state and return the new state.
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
        start_serialized = tuple(self.environment.state.items())
        heapq.heappush(frontier, (0, start_serialized, []))

        # Set to keep track of visited states
        c = 0
        while frontier:
            f_cost, serialized_state, path = heapq.heappop(frontier)

            # Deserialize the state
            current_state = dict(serialized_state)

            # Check if the goal is reached
            self.environment.state = current_state  # Update the environment's state

            # Expand the current state
            possible_moves = self.get_valid_moves(current_state)
            for bead1, bead2 in possible_moves:
                for angle in [90, -90, 180]:
                    # Save the current state
                    original_state = self.environment.state.copy()
                    self.apply_rotation(bead1, bead2, angle)
                    # Serialize the new state
                    new_state = self.environment.state.copy()
                    serialized_new_state = tuple(new_state.items())

                    # Calculate costs
                    g_cost = len(path) + 1  # Actual cost to reach this state
                    h_cost = self.heuristic(new_state)  # Heuristic cost
                    f_cost = g_cost + h_cost
                    # Add the new state to the frontier
                    new_path = path + [(bead1, bead2, angle)]
                    heapq.heappush(frontier, (f_cost, serialized_new_state, new_path))
                    if self.environment.is_solved():
                        return new_path

                    # Restore the original state
                    self.environment.state = original_state
            c += 1
            if c % 1000 == 0:
                self.environment.plot_states()
        return None  # No solution found