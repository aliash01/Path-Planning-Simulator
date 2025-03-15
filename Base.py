class GridEnv:
    def __init__(self, grid_width=5, grid_height=5):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.grid = [["O" for _ in range(self.grid_width)] for _ in range(self.grid_height)]
    
        self.menu()

    def print_current_grid(self):
            for row in self.grid:
                print(row)

    def menu(self):
        option = input("1) Edit Grid\n2) Run Simulation\n")
        if option == "1":
            self.env_setup()
        if option == "2":
            print("WIP")
        else:
            print("Please enter a valid option")
            self.menu()

    def env_setup(self):
        """
        Function for setting up the environment obstacles and layout
        """
        done = False
        while not done:
            self.print_current_grid()
            grid_alter = input("Would you like to add or remove any obstacles?\n1) Add Obstacle\n2) Remove Obstacle\n3) Edit Grid Size \n4) Finish Editing\n")

            def check_grid(check):
                for row in self.grid:
                    if check in row:
                        return True
                return False

            if grid_alter == "1":
                if check_grid("O"):
                    change_x = int(input("Please enter the row you wish to add an obstacle to."))
                    change_y = int(input("Please enter the column you wish to add an obstacle to."))

                    if self.grid[change_x][change_y] != "X":
                        self.grid[change_x][change_y] = "X"

                    else:
                        print("This space already has an obstacle.")

                else:
                    print("There are currently no unoccupied spaces.")
                
            elif grid_alter == "2":
                if check_grid("X"):
                    change_x = int(input("Please enter the row you wish to add an obstacle to."))
                    change_y = int(input("Please enter the column you wish to add an obstacle to."))

                    if self.grid[change_x][change_y] != "O":
                        self.grid[change_x][change_y] = "O"

                    else:
                        print("This space is already empty.")

                else:
                    print("There are currently no obstacles")
            elif grid_alter == "3":
                new_width = int(input("Enter new grid width: "))
                new_height = int(input("Enter new grid height: "))

                if new_width <= 0 or new_height <= 0:
                    print("Grid dimensions must be positive integers.")

            elif grid_alter == "4":
                done = True

            else:
                print("Please enter a valid option")
        


gridenv = GridEnv()

