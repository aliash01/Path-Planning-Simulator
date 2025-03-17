import heapq
from collections import deque

import heapq
from collections import deque

class PathfindingAlgorithms:
    def __init__(self, grid, grid_height, grid_width):
        self.grid = grid
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left
        
    def update_grid_reference(self, grid, grid_height, grid_width):
        """Update the grid reference when the grid is modified in the main application"""
        self.grid = grid
        self.grid_height = grid_height
        self.grid_width = grid_width
        
    def is_valid_position(self, position):
        """Check if a position is valid (within grid bounds and not an obstacle)"""
        i, j = position
        return (0 <= i < self.grid_height and 
                0 <= j < self.grid_width and 
                self.grid[i][j] != "X")
    
    def a_star(self, start, goal, visualize_callback=None):
        """
        A* pathfinding algorithm
        
        Args:
            start: Tuple (row, col) of start position
            goal: Tuple (row, col) of goal position
            visualize_callback: Function to call for visualization during search
            
        Returns:
            came_from: Dictionary containing the path connections
        """
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance
            
        priority_queue = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}
        
        while priority_queue:
            _, current = heapq.heappop(priority_queue)
            
            if visualize_callback:
                visualize_callback(current, current == goal)
                
            if current == goal:
                break
                
            for dy, dx in self.directions:
                neighbor = (current[0] + dy, current[1] + dx)
                
                if self.is_valid_position(neighbor):
                    temp_g_score = g_score[current] + 1
                    
                    if neighbor not in g_score or temp_g_score < g_score[neighbor]:
                        g_score[neighbor] = temp_g_score
                        f_score[neighbor] = temp_g_score + heuristic(neighbor, goal)
                        heapq.heappush(priority_queue, (f_score[neighbor], neighbor))
                        came_from[neighbor] = current
                        
        return came_from
        
    def bfs(self, start, goal, visualize_callback=None):
        """Breadth-First Search algorithm
        
        Args:
            start: Tuple (row, col) of start position
            goal: Tuple (row, col) of goal position
            visualize_callback: Function to call for visualization during search
            
        Returns:
            came_from: Dictionary containing the path connections
        """
        queue = deque([start])
        came_from = {start: None}
        
        while queue:
            current = queue.popleft()
            
            if visualize_callback:
                visualize_callback(current, current == goal)
                
            if current == goal:
                break
                
            for dy, dx in self.directions:
                neighbor = (current[0] + dy, current[1] + dx)
                
                if (self.is_valid_position(neighbor) and neighbor not in came_from):
                    came_from[neighbor] = current
                    queue.append(neighbor)
                    
        return came_from
        
    def dijkstra(self, start, goal, visualize_callback=None):
        """Dijkstra's algorithm
        
        Args:
            start: Tuple (row, col) of start position
            goal: Tuple (row, col) of goal position
            visualize_callback: Function to call for visualization during search
            
        Returns:
            came_from: Dictionary containing the path connections
        """
        priority_queue = [(0, start)]
        came_from = {}
        cost_so_far = {start: 0}
        
        while priority_queue:
            current_cost, current = heapq.heappop(priority_queue)
            
            if visualize_callback:
                visualize_callback(current, current == goal)
                
            if current == goal:
                break
                
            for dy, dx in self.directions:
                neighbor = (current[0] + dy, current[1] + dx)
                
                if self.is_valid_position(neighbor):
                    new_cost = cost_so_far[current] + 1
                    
                    if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                        cost_so_far[neighbor] = new_cost
                        heapq.heappush(priority_queue, (new_cost, neighbor))
                        came_from[neighbor] = current
                        
        return came_from
        
    def dfs(self, start, goal, visualize_callback=None):
        """Depth-First Search algorithm
        
        Args:
            start: Tuple (row, col) of start position
            goal: Tuple (row, col) of goal position
            visualize_callback: Function to call for visualization during search
            
        Returns:
            came_from: Dictionary containing the path connections
        """
        stack = [start]
        came_from = {}
        visited = set()
        
        while stack:
            current = stack.pop()
            
            if visualize_callback:
                visualize_callback(current, current == goal)
                
            if current == goal:
                break
                
            if current in visited:
                continue
            visited.add(current)
            
            for dy, dx in self.directions:
                neighbor = (current[0] + dy, current[1] + dx)
                
                if (self.is_valid_position(neighbor) and neighbor not in visited):
                    came_from[neighbor] = current
                    stack.append(neighbor)
                    
        return came_from