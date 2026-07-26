# LLStack

A custom stack data structure implemented using a linked list, featuring a pathfinding game that demonstrates its usage.

## Overview

LLStack is a Python implementation of a stack data structure using a linked list. The project includes:

- **LLStack**: A custom stack implementation that stores tuples of two positive integers
- **Map**: A pathfinding game that uses the LLStack for storing coordinate paths
- **Comprehensive Testing**: Full test suite using Python's unittest framework

## Features

### LLStack Class
- **Type-safe**: Only accepts tuples of two positive integers
- **Standard Stack Operations**: `push()` and `pop()` methods
- **Size Tracking**: Property to get current number of elements
- **String Representation**: Human-readable format showing stack contents
- **Comprehensive Validation**: Input validation with descriptive error messages

### Map Class (Pathfinding Game)
- **Grid-based Navigation**: 2D grid with 'grass' and 'ocean' terrain types
- **Path Finding**: Depth-first search algorithm to find valid paths
- **Shortest Path**: Optimized algorithm to find the shortest route
- **Coordinate Validation**: Ensures start/end points are valid and reachable
- **Custom Exceptions**: Specific error handling for invalid coordinates

## Installation

1. Clone the repository:
```bash
git clone https://github.com/daveryfarradmoore/LLStack.git
cd LLStack
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. The project uses only Python standard library, so no additional dependencies are required.

## Usage

### Basic LLStack Operations

```python
from llstack import LLStack

# Create a new stack
stack = LLStack()

# Push elements (tuples of two positive integers)
stack.push((1, 2))
stack.push((3, 4))
stack.push((5, 6))

# Check stack size
print(f"Stack size: {stack.size}")  # Output: Stack size: 3

# Pop elements (returns in LIFO order)
print(stack.pop())  # Output: (5, 6)
print(stack.pop())  # Output: (3, 4)

# String representation
print(stack)  # Output: (1,2)
```

### Pathfinding Game

Launch the Tkinter interface with:

```bash
python main.py
```

In the GUI, click cells to toggle ocean terrain, enter start/end coordinates, and use either pathfinding button to display the resulting route.

```python
from game import Map

# Create a game map
grid = [
    ['grass', 'grass', 'grass'],
    ['grass', 'ocean', 'grass'],
    ['grass', 'grass', 'grass']
]

# Initialize map with start and end coordinates
game_map = Map(grid, (0, 0), (2, 2))

# Find any valid path
path = game_map.find_path()
if path:
    print("Path found!")
    print(path)  # Shows coordinates from start to end
else:
    print("No path available")

# Find shortest path
shortest_path = game_map.find_shortest_path()
if shortest_path:
    print("Shortest path found!")
    print(shortest_path)
```

## Running Tests

Execute the test suite to verify all functionality:

```bash
python game_test.py
```

The test suite includes:
- LLStack functionality tests (push, pop, validation, string representation)
- Map class tests (constructor validation, coordinate validation, pathfinding)
- Edge case testing (empty stacks, invalid inputs, no-path scenarios)

## Project Structure

```
LLStack/
├── README.md           # This file
├── llstack.py          # LLStack implementation
├── game.py             # Map class and pathfinding logic
├── game_test.py        # Comprehensive test suite
├── main.py             # Main entry point (currently empty)
└── venv/               # Virtual environment (excluded from git)
```

## Implementation Details

### LLStack
- Uses a linked list with `Node` class for internal storage
- Maintains a `__head` pointer to the top of the stack
- Validates all inputs to ensure type safety and data integrity
- Provides detailed error messages for debugging

### Map Pathfinding
- **Depth-First Search**: `find_path()` method uses recursive DFS with backtracking
- **Shortest Path**: `find_shortest_path()` uses distance-based optimization
- **Coordinate System**: (row, col) format with 0-based indexing
- **Terrain Types**: 'grass' (traversable) and 'ocean' (impassable)

## Error Handling

The project includes comprehensive error handling:

- **TypeError**: Invalid data types
- **ValueError**: Invalid values (negative numbers, wrong tuple length)
- **IndexError**: Operations on empty stack
- **InvalidCoordinateError**: Invalid placement on map
- **OutOfBoundaries**: Coordinates outside grid limits

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

**D'Avery Farrad Moore**
- GitHub: [@daveryfarradmoore](https://github.com/daveryfarradmoore)
- Student at Grand Valley State University
