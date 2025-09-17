from typing import List, Tuple, Dict, Set
from llstack import LLStack


class InvalidCoordinateError(Exception):
    """
    Custom exception raised when a coordinate is invalid for map placement.

    This occurs when trying to place a starting or ending point in an invalid location,
    such as in an ocean cell or outside the grid boundaries.
    """
    pass


class OutOfBoundaries(Exception):
    """
    Custom exception raised when coordinates are outside the map's grid limits.

    This helps prevent accessing grid locations that do not exist.
    """
    pass


class Map:
    """
    Represents a game map with pathfinding capabilities.

    The map is a 2D grid where:
    - Cells can be 'ocean' or 'grass'
    - Has defined start and end coordinates
    - Supports finding paths between start and end points

    Attributes:
        __grid (list): 2D grid representing the map terrain
        start_coords (tuple): Starting point coordinates
        end_coords (tuple): Destination point coordinates
    """

    def __init__(self, grid: list[list[str]], start_loc: tuple, end_loc: tuple):
        """
        Initialize the map with a grid, start, and end locations.

        Performs extensive input validation to ensure:
        - Grid is a list of lists
        - Grid contains only string values
        - Grid values are either 'ocean' or 'grass'

        Args:
            grid (list): 2D list representing map terrain
            start_loc (tuple): Starting point coordinates
            end_loc (tuple): Destination point coordinates

        Raises:
            TypeError: If grid format is incorrect
            ValueError: If grid contains invalid terrain values
        """
        # Validate grid is a list of lists of strings
        if not isinstance(grid, list) or not all(isinstance(row, list) for row in grid):
            raise TypeError("Grid must be a list of lists")

        if not all(all(isinstance(cell, str) for cell in row) for row in grid):
            raise TypeError("Grid must contain only strings")

        # Ensure grid only contains 'ocean' or 'grass'
        if not all(all(cell in ['ocean', 'grass'] for cell in row) for row in grid):
            raise ValueError("Grid values must be 'ocean' or 'grass'")

        # Store the grid privately
        self.__grid = grid
        # Set start and end coordinates with validation
        self.start_coords = start_loc
        self.end_coords = end_loc

    @property
    def grid(self):
        """
        Getter for the map grid.

        Returns:
            list: The 2D grid representing map terrain
        """
        return self.__grid

    @property
    def start_coords(self):
        """
        Getter for start coordinates.

        Returns:
            tuple: Starting point coordinates
        """
        return self.__start

    @start_coords.setter
    def start_coords(self, coords):
        """
        Setter for start coordinates with comprehensive validation.

        Ensures that:
        - Coordinates are a tuple of 2 positive integers
        - Coordinates are within grid boundaries
        - Start point is not in an ocean cell

        Args:
            coords (tuple): Proposed start coordinates

        Raises:
            TypeError: If coordinates are not a tuple of integers
            ValueError: If coordinates are invalid
            OutOfBoundaries: If coordinates are outside grid
            InvalidCoordinateError: If start point is in ocean
        """
        # Validate coordinate type and format
        if not isinstance(coords, tuple):
            raise TypeError("Start coordinates must be a tuple")
        if len(coords) != 2:
            raise ValueError("Start coordinates must be a tuple of length 2")
        if not all(isinstance(x, int) for x in coords):
            raise TypeError("Coordinates must be integers")
        if not all(x >= 0 for x in coords):
            raise ValueError("Coordinates must be positive integers")

        # Validate grid boundaries
        row, col = coords
        if row >= len(self.__grid):
            raise OutOfBoundaries("Row coordinate out of bounds")
        if col >= len(self.__grid[row]):
            raise OutOfBoundaries("Column coordinate out of bounds")

        # Ensure start point is not in ocean
        if self.__grid[row][col] == 'ocean':
            raise InvalidCoordinateError("Start position cannot be in ocean")

        # Set validated start coordinates
        self.__start = coords

    @property
    def end_coords(self):
        """
        Getter for end coordinates.

        Returns:
            tuple: Destination point coordinates
        """
        return self.__end

    @end_coords.setter
    def end_coords(self, coords):
        """
        Setter for end coordinates with comprehensive validation.

        Ensures that:
        - Coordinates are a tuple of 2 positive integers
        - Coordinates are within grid boundaries
        - End point is not in an ocean cell
        - End point is different from start point

        Args:
            coords (tuple): Proposed end coordinates

        Raises:
            TypeError: If coordinates are not a tuple of integers
            ValueError: If coordinates are invalid
            OutOfBoundaries: If coordinates are outside grid
            InvalidCoordinateError: If end point is in ocean
        """
        # Similar validation as start_coords setter
        if not isinstance(coords, tuple):
            raise TypeError("End coordinates must be a tuple")
        if len(coords) != 2:
            raise ValueError("End coordinates must be a tuple of length 2")
        if not all(isinstance(x, int) for x in coords):
            raise TypeError("Coordinates must be integers")
        if not all(x >= 0 for x in coords):
            raise ValueError("Coordinates must be positive integers")

        # Validate grid boundaries
        row, col = coords
        if row >= len(self.__grid):
            raise OutOfBoundaries("Row coordinate out of bounds")
        if col >= len(self.__grid[row]):
            raise OutOfBoundaries("Column coordinate out of bounds")

        # Ensure end point is not in ocean
        if self.__grid[row][col] == 'ocean':
            raise InvalidCoordinateError("End position cannot be in ocean")

        # Ensure end point is different from start point
        if coords == self.__start:
            raise ValueError("End coordinates cannot match start coordinates")

        # Set validated end coordinates
        self.__end = coords

    def __check_move(self, pos: tuple, visited: set) -> bool:
        """
        Check if a given position is valid for movement.

        Validates that a position:
        - Is within grid boundaries
        - Is not an ocean cell
        - Has not been previously visited

        Args:
            pos (tuple): Position coordinates to check
            visited (set): Set of already visited positions

        Returns:
            bool: True if position is valid for movement, False otherwise
        """
        row, col = pos

        # Check grid boundaries
        if row < 0 or row >= len(self.__grid):
            return False
        if col < 0 or col >= len(self.__grid[row]):
            return False

        # Ensure not an ocean cell
        if self.__grid[row][col] == 'ocean':
            return False

        # Ensure not already visited
        if pos in visited:
            return False

        return True

    def find_path(self) -> LLStack:
        """
        Find a path from start to end coordinates using depth-first search.

        Attempts to find a valid path through grass cells from start to end.
        Uses a recursive depth-first search approach with backtracking.

        Returns:
            LLStack: A stack of coordinates representing the path
            None: If no path can be found
        """
        # Initialize an empty stack and visited set
        stack = LLStack()
        visited = set()

        def __solve(row: int, col: int, neighbors=[(-1, 0), (1, 0), (0, -1), (0, 1)]) -> bool:
            """
            Recursive depth-first search to find a path to the destination.

            Explores neighboring cells in a specific order, backtracking if needed.

            Args:
                row (int): Current row coordinate
                col (int): Current column coordinate
                neighbors (list): Possible movement directions

            Returns:
                bool: True if path is found, False otherwise
            """
            # Check if destination is reached
            if (row, col) == self.__end:
                stack.push((row, col))
                return True

            # Prevent revisiting cells
            if (row, col) in visited:
                return False
            visited.add((row, col))

            def __explore(index=0):
                """
                Explore neighboring cells recursively.

                Tries to move in each direction, backtracking if no path is found.

                Args:
                    index (int): Current neighbor index to explore

                Returns:
                    bool: True if a path is found, False otherwise
                """
                # Base case: all neighbors explored
                if index == len(neighbors):
                    return False

                # Get current neighbor direction
                dr, dc = neighbors[index]
                new_row, new_col = row + dr, col + dc

                # Check if move is valid
                if (
                        0 <= new_row < len(self.__grid)
                        and 0 <= new_col < len(self.__grid[new_row])
                        and self.__grid[new_row][new_col] == "grass"
                ):
                    # Recursively try to solve from this position
                    if __solve(new_row, new_col):
                        stack.push((row, col))
                        return True

                # Try next neighbor if current one fails
                return __explore(index + 1)

            return __explore()

        # Start path finding from start coordinates
        start_row, start_col = self.__start
        if __solve(start_row, start_col):
            # Reverse the stack to get path from start to end
            reversed_stack = LLStack()
            while stack.size > 0:
                reversed_stack.push(stack.pop())
            return reversed_stack
        return None

    def find_shortest_path(self) -> LLStack:
        """
        Find the shortest path from start to end coordinates.

        Uses a distance-based approach to determine the optimal path:
        1. Compute distances to all reachable points
        2. Construct the shortest path using these distances

        Returns:
            LLStack: A stack of coordinates representing the shortest path
            None: If no path can be found
        """
        # Find distances from start to all reachable points
        distances = self.__find_distances(self.__start, {})

        # Check if end point is reachable
        if distances.get(self.__end) is None:
            return None

        # Initialize stack for path
        stack = LLStack()
        # Construct shortest path
        self.__construct_shortest_path(self.__start, distances, stack)
        return stack

    def __find_distances(self, current: tuple, memo: dict) -> dict:
        """
        Recursively compute distances from start to all reachable points.

        Uses memoization to store and update minimum distances.

        Args:
            current (tuple): Current position coordinates
            memo (dict): Memoization dictionary to track distances

        Returns:
            dict: Updated distances to all reachable points
        """
        # Check if current move is valid
        if not self.__check_move(current, set(memo.keys())):
            return memo

        # Mark end point with zero distance
        if current == self.__end:
            memo[current] = 0
            return memo

        # Initialize current point distance to infinity
        memo[current] = float('inf')
        row, col = current
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def process_neighbors(index: int, min_dist: float) -> float:
            """
            Recursively process neighboring cells to find minimum distance.

            Args:
                index (int): Current neighbor index
                min_dist (float): Current minimum distance

            Returns:
                float: Updated minimum distance
            """
            # Base case: all neighbors processed
            if index >= len(directions):
                return min_dist

            # Get current neighbor
            dr, dc = directions[index]
            next_pos = (row + dr, col + dc)

            # Recursively find distances
            self.__find_distances(next_pos, memo)

            # Update minimum distance if neighbor is reachable
            if next_pos in memo:
                min_dist = min(min_dist, 1 + memo[next_pos])

            # Process next neighbor
            return process_neighbors(index + 1, min_dist)

        # Find minimum distance to end
        min_distance = process_neighbors(0, float('inf'))

        # Update or remove current point's distance
        if min_distance == float('inf'):
            del memo[current]
        else:
            memo[current] = min_distance

        return memo

    def __construct_shortest_path(self, current: tuple, distances: dict, stack: LLStack) -> bool:
        """
        Recursively construct the shortest path using pre-computed distances.

        Backtracks from end to start, choosing the path with minimum distances.

        Args:
            current (tuple): Current position coordinates
            distances (dict): Pre-computed distances to points
            stack (LLStack): Stack to store path coordinates

        Returns:
            bool: True if path construction is successful, False otherwise
        """
        # Check if current point is reachable
        if current not in distances:
            return False

        # Add current point to path
        stack.push(current)

        # Check if end is reached
        if current == self.__end:
            return True

        row, col = current
        curr_dist = distances[current]
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def try_next_step(index: int) -> bool:
            """
            Recursively try to find the next step in the shortest path.

            Args:
                index (int): Current neighbor index

            Returns:
                bool: True if next step is found, False otherwise
            """
            # Base case: all neighbors processed
            if index >= len(directions):
                return False

            # Get current neighbor
            dr, dc = directions[index]
            next_pos = (row + dr, col + dc)

            # Check if next position leads to shortest path
            if (next_pos in distances and
                    distances[next_pos] == curr_dist - 1 and
                    self.__construct_shortest_path(next_pos, distances, stack)):
                return True

            # Try next neighbor
            return try_next_step(index + 1)

        # Attempt to find next step
        if not try_next_step(0):
            # Backtrack if no valid step found
            stack.pop()
            return False

        return True





