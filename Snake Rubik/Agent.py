import heapq
import hashlib
import random  # For random sampling

class SnakeRubikAgent:
    def __init__(self, environment):
        self.environment = environment
        self.goal_positions = {i: pos for i, pos in enumerate(self.environment.solution_vals, 1)}

    def heuristic(self, state):
        """
        Heuristic function: Calculate the Manhattan distance between the goal position and the current position
        for all beads in the state.
        """
        return sum(
            map(
                lambda bead: abs(state[bead][0] - self.goal_positions[bead][0]) +
                            abs(state[bead][1] - self.goal_positions[bead][1]) +
                            abs(state[bead][2] - self.goal_positions[bead][2]),
                state.keys()
            )
        )

    def apply_rotation(self, bead1, bead2, angle):
        """
        Apply rotation on a copy of the state and return the new state.
        """
        org_state = self.environment.state.copy()
        self.environment.rotate(bead1, bead2, angle)
        new_state = self.environment.state.copy()
        self.environment.state = org_state  # Restore the original state
        return new_state

    def get_valid_moves(self, state):
        """
        Get valid bead pairs that can be rotated.
        """
        return [
            (bead1, bead2)
            for bead1 in state
            for bead2 in state
            if bead1 != bead2 
            and (bead1, bead2) not in self.environment.glued_beads
            and (bead2, bead1) not in self.environment.glued_beads
            and self.environment.get_shared_axis(bead1, bead2) is not None
            and abs(bead1 - bead2) == 1
        ]


    def a_star(self):
        """
        Solve the Snake Rubik problem using A* Search.
        Returns the solution as a list of moves.
        """

        # Priority queue for A* (cost + heuristic, serialized_state, path)
        frontier = []
        start_serialized = tuple(sorted(self.environment.state.items()))
        heapq.heappush(frontier, (0, start_serialized, []))

        # Set to keep track of visited states
        visited = set()
        c = 0

        while frontier:
            f_cost, serialized_state, path = heapq.heappop(frontier)

            # Deserialize the state
            current_state = dict(serialized_state)
            hash_key = hash(frozenset(current_state.items()))
            if hash_key in visited:
                continue
            if self.environment.is_solved():
                print('ypoooo')
                return path

            # Mark the state as visited
            visited.add(hash_key)
            self.environment.state = current_state  # Update the environment's state

            # Expand the current state
            possible_moves = self.get_valid_moves(current_state)
            flag = False
            for bead1, bead2 in possible_moves:
                for angle in [90, -90]:
                    new_state = self.apply_rotation(bead1, bead2, angle)
                    # Serialize the new state
                    serialized_new_state = tuple(sorted(new_state.items()))
                    # Calculate costs
                    hash_key = hash(frozenset(new_state.items()))
                    if hash_key not in visited:
                        g_cost = len(path) + 1  # Actual cost to reach this state
                        h_cost = self.heuristic(new_state)  # Heuristic cost
                        f_cost = g_cost + h_cost
                        # Add the new state to the frontier
                        new_path = path + [(bead1, bead2, angle)]  
                        # check if this state with lower f_cost is already in the frontier then not add it
                        for i in frontier:
                            if i[1] == serialized_new_state and i[0] < f_cost:
                                flag = True
                        if not flag:
                            heapq.heappush(frontier, (f_cost, serialized_new_state, new_path))

                    c += 1
                    if c % 1000 == 0:
                        print(f"Visited states: {len(visited)}, Frontier size: {len(frontier)}")
                        self.environment.plot_states()

            # Periodically reduce the size of the visited set using LRU cache
            if c % 100000 == 0:
                print(f"Iteration {c}: Reducing visited states...")
                while len(visited) > 100000:
                    visited.pop()

        return None  # No solution found

    
    def ucs(self):
        """
        Solve the Snake Rubik problem using Uniform-Cost Search (UCS).
        Returns the solution as a list of moves.
        """
        # Priority queue for UCS
        frontier = []
        heapq.heappush(frontier, (0, tuple(self.environment.state.items()), []))  # (cost, serialized_state, path)
        # Set to keep track of visited states
        visited = set()
        c = 0
        while frontier:
            cost, serialized_state, path = heapq.heappop(frontier)
            # Deserialize the state
            current_state = dict(serialized_state)
            if serialized_state in visited:
                continue
            # Mark the state as visited
            visited.add(serialized_state)
            # Check if the goal is reached
            self.environment.state = current_state  # Update the environment's state
            if self.environment.is_solved():
                return path
            # Expand the current state
            for bead1, bead2 in self.get_valid_moves(current_state):
                for angle in [90, -90, 180]:
                    original_state = self.environment.state.copy()
                    self.apply_rotation(bead1, bead2, angle)
                    # Serialize the new state
                    new_state = self.environment.state.copy()
                    serialized_new_state = tuple(new_state.items())
                    if serialized_new_state not in visited:
                        new_cost = cost + 1
                        new_path = path + [(bead1, bead2, angle)]
                        heapq.heappush(frontier, (new_cost, serialized_new_state, new_path))
                        if self.environment.is_solved():
                            return new_path
                    self.environment.state = original_state
            c += 1
            if c % 1000 == 0:
                self.environment.plot_states()
        return None 