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
        
        # Add menu buttons - Now with just one toggle button instead of add/remove
        self.toggle_btn = tk.Button(self.menu_frame, text="Toggle Obstacle Mode", command=self.toggle_obstacle_mode)
        self.toggle_btn.grid(row=0, column=0, padx=5)
        
        self.resize_btn = tk.Button(self.menu_frame, text="Resize Grid", command=self.resize_grid)
        self.resize_btn.grid(row=0, column=1, padx=5)
        
        self.sim_btn = tk.Button(self.menu_frame, text="Run Simulation", command=self.run_simulation)
        self.sim_btn.grid(row=0, column=2, padx=5)
        
        # Track current mode - default to toggle mode
        self.current_mode = "toggle"
        
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
        self.current_mode = "toggle"
        self.toggle_btn.config(relief=tk.SUNKEN)
    
    def resize_grid(self):
        try:
            # Use our custom dialog to get both width and height at once
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
        messagebox.showinfo("Simulation", "Simulation feature is work in progress.")
    
    def check_grid(self, check):
        for row in self.grid:
            if check in row:
                return True
        return False

# Run the application
if __name__ == "__main__":
    app = VisualGridEnv()