from environment import *
from Agent import *

def main():
    # Initialize the environment
    environment = SnakeRubikEnvironment()

    # Initialize the agent
    agent = SnakeRubikAgent(environment)

    # Solve the Snake Rubik problem using A* Search
    solution = agent.a_star()

    # Print the solution
    print(solution)

if __name__ == "__main__":
    main()