
class PerfurmanceMeasure:
    
    def __init__(self) -> None:
        self.F1 = 0 # agent moves 
        self.F2 = 0 # unsuccessfull agent move 
        self.F3 = 0 # unsuccessfull vacuums
        self.F4 = 0 # succesfull vaccums 
        self.F5 = 0 # number of dirty rooms after each step