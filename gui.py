import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

class GridSizeDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, initial_width=5, initial_height=5):
        self.width = initial_width
        self.height = initial_height
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text="Grid Width:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        tk.Label(master, text="Grid Height:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        
        self.width_entry = tk.Entry(master)
        self.width_entry.grid(row=0, column=1, pady=5, padx=5)
        self.width_entry.insert(0, str(self.width))
        
        self.height_entry = tk.Entry(master)
        self.height_entry.grid(row=1, column=1, pady=5, padx=5)
        self.height_entry.insert(0, str(self.height))
        
        return self.width_entry  # Initial focus
    
    def validate(self):
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            
            if width < 1 or width > 20 or height < 1 or height > 20:
                messagebox.showerror("Invalid Input", "Grid dimensions must be between 1 and 20.")
                return False
                
            self.result = (width, height)
            return True
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers.")
            return False

class VisualGridEnv:
    def __init__(self, grid_width=5, grid_height=5, cell_size=80):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_size = cell_size
        self.grid = [["O" for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Grid Environment Simulator")
        self.root.resizable(False, False)
        
        # Frame for the grid
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(pady=10)
        
        # Create the menu frame
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(pady=10)
        
        self.toggle_btn = tk.Button(self.menu_frame, text="Toggle Obstacle Mode", command=self.toggle_obstacle_mode)
        self.toggle_btn.grid(row=0, column=0, padx=5)
        
        self.resize_btn = tk.Button(self.menu_frame, text="Resize Grid", command=self.resize_grid)
        self.resize_btn.grid(row=0, column=1, padx=5)
        
        self.sim_btn = tk.Button(self.menu_frame, text="Run Simulation", command=self.run_simulation)
        self.sim_btn.grid(row=0, column=2, padx=5)
        
        # Track current mode - default to toggle mode
        self.current_mode = "view"
        
        # Create the grid
        self.canvas_cells = []
        self.create_grid()
        
        # Start the GUI event loop
        self.root.mainloop()
    
    def create_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        
        self.canvas_cells = []

        self.canvas = tk.Canvas(
            self.grid_frame, 
            width=self.grid_width * self.cell_size,
            height=self.grid_height * self.cell_size,
            bg="white"
        )
        self.canvas.pack()
        
        # Draw grid lines and cells
        for i in range(self.grid_height):
            row_cells = []
            for j in range(self.grid_width):
                # Calculate coordinates
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Create cell rectangle
                fill_color = "white" if self.grid[i][j] == "O" else "black"
                cell = self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="gray")
                self.canvas.tag_bind(cell, "<Button-1>", lambda event, row=i, col=j: self.cell_clicked(row, col))
                row_cells.append(cell)
            self.canvas_cells.append(row_cells)
    
    def update_grid_display(self):
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                fill_color = "white" if self.grid[i][j] == "O" else "black"
                self.canvas.itemconfig(self.canvas_cells[i][j], fill=fill_color)
    
    def cell_clicked(self, row, col):
        if self.current_mode == "toggle":
            # Toggle between "O" and "X"
            if self.grid[row][col] == "O":
                self.grid[row][col] = "X"
                self.canvas.itemconfig(self.canvas_cells[row][col], fill="black")
            else:
                self.grid[row][col] = "O"
                self.canvas.itemconfig(self.canvas_cells[row][col], fill="white")
    
    def toggle_obstacle_mode(self):
        # Toggle between "toggle" and "view" modes
        if self.current_mode == "toggle":
            self.current_mode = "view"
            self.toggle_btn.config(relief=tk.RAISED, text="Enable Obstacle Mode")
        else:
            self.current_mode = "toggle"
            self.toggle_btn.config(relief=tk.SUNKEN, text="Disable Obstacle Mode")
    
    def resize_grid(self):
        try:
            dialog = GridSizeDialog(
                self.root, 
                "Resize Grid", 
                initial_width=self.grid_width,
                initial_height=self.grid_height
            )
            
            if dialog.result:  # If the user clicked OK
                new_width, new_height = dialog.result
                
                # Create new grid preserving existing cells where possible
                new_grid = [["O" for _ in range(new_width)] for _ in range(new_height)]
                for i in range(min(self.grid_height, new_height)):
                    for j in range(min(self.grid_width, new_width)):
                        new_grid[i][j] = self.grid[i][j]
                
                self.grid_width = new_width
                self.grid_height = new_height
                self.grid = new_grid
                
                # Recreate the grid
                self.create_grid()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to resize grid: {str(e)}")
    
    def run_simulation(self):
        sim_window = tk.Toplevel(self.root)
        sim_window.title("Simulation")
        sim_window.geometry("400x300")  
        
        tk.Button(sim_window, text="Set Start Position", command=self.set_start_position).pack(pady=20)
        tk.Button(sim_window, text="Set Goal Position", command=self.set_goal_position).pack(pady=20)

        tk.Label(sim_window, text="Simulation is running...", font=("Arial", 14)).pack(pady=20)
        
        tk.Button(sim_window, text="Close", command=sim_window.destroy).pack(pady=10)

    def set_start_position(self):
        # Create a dialog for entering start position coordinates
        start_dialog = tk.Toplevel(self.root)
        start_dialog.title("Set Start Position")
        start_dialog.geometry("300x150")
        start_dialog.resizable(False, False)
        
        # Center the dialog on the screen
        start_dialog.grab_set()  # Make dialog modal
        
        # Create input fields
        tk.Label(start_dialog, text="X coordinate (0-{}):".format(self.grid_width-1)).pack(pady=(10, 5))
        x_entry = tk.Entry(start_dialog, width=10)
        x_entry.pack()
        
        tk.Label(start_dialog, text="Y coordinate (0-{}):".format(self.grid_height-1)).pack(pady=(10, 5))
        y_entry = tk.Entry(start_dialog, width=10)
        y_entry.pack()
        
        # Function to handle coordinate submission
        def submit_coords():
            try:
                x = int(x_entry.get())
                y = int(y_entry.get())
                
                # Validate coordinates
                if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
                    # Reset previous start position if exists
                    for i in range(self.grid_height):
                        for j in range(self.grid_width):
                            if self.grid[i][j] == "S":
                                self.grid[i][j] = "O"
                    
                    # Set new start position
                    self.grid[y][x] = "S"
                    self.update_grid_display()  # Update the grid visualization
                    start_dialog.destroy()
                else:
                    messagebox.showerror("Invalid Coordinates", 
                                        f"Coordinates must be within grid bounds (0-{self.grid_width-1}, 0-{self.grid_height-1})")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers for coordinates.")
        
        # Submit button
        tk.Button(start_dialog, text="Set Start", command=submit_coords).pack(pady=10)

    def set_goal_position(self):
        # Create a dialog for entering goal position coordinates
        goal_dialog = tk.Toplevel(self.root)
        goal_dialog.title("Set Goal Position")
        goal_dialog.geometry("300x150")
        goal_dialog.resizable(False, False)
        
        # Center the dialog on the screen
        goal_dialog.grab_set()  # Make dialog modal
        
        # Create input fields
        tk.Label(goal_dialog, text="X coordinate (0-{}):".format(self.grid_width-1)).pack(pady=(10, 5))
        x_entry = tk.Entry(goal_dialog, width=10)
        x_entry.pack()
        
        tk.Label(goal_dialog, text="Y coordinate (0-{}):".format(self.grid_height-1)).pack(pady=(10, 5))
        y_entry = tk.Entry(goal_dialog, width=10)
        y_entry.pack()
        
        # Function to handle coordinate submission
        def submit_coords():
            try:
                x = int(x_entry.get())
                y = int(y_entry.get())
                
                # Validate coordinates
                if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
                    # Reset previous goal position if exists
                    for i in range(self.grid_height):
                        for j in range(self.grid_width):
                            if self.grid[i][j] == "G":
                                self.grid[i][j] = "O"
                    
                    # Set new goal position
                    self.grid[y][x] = "G"
                    self.update_grid_display()  # Update the grid visualization
                    goal_dialog.destroy()
                else:
                    messagebox.showerror("Invalid Coordinates", 
                                        f"Coordinates must be within grid bounds (0-{self.grid_width-1}, 0-{self.grid_height-1})")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers for coordinates.")
        
        # Submit button
        tk.Button(goal_dialog, text="Set Goal", command=submit_coords).pack(pady=10)     

    def update_grid_display(self):
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if self.grid[i][j] == "O":
                    fill_color = "white"
                elif self.grid[i][j] == "X":
                    fill_color = "black"
                elif self.grid[i][j] == "S":
                    fill_color = "green"
                elif self.grid[i][j] == "G":
                    fill_color = "yellow"
                else:
                    fill_color = "white"
                
                self.canvas.itemconfig(self.canvas_cells[i][j], fill=fill_color)
    
    def check_grid(self, check):
        for row in self.grid:
            if check in row:
                return True
        return False

# Run the application
if __name__ == "__main__":
    app = VisualGridEnv()