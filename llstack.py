class Node:
    """
    Represents a single node in the linked list stack.

    Each node stores:
    - data: A tuple containing two positive integers
    - next: A reference to the next node in the stack

    Attributes:
        data (tuple): A tuple of two positive integers
        next (Node): Reference to the next node (or None if last node)
    """

    def __init__(self, data: tuple):
        # Store the data tuple in this node
        self.data = data
        # Initially, this node doesn't point to any next node
        self.next = None


class LLStack:
    """
    A custom stack data structure implemented using a linked list.

    This stack has special constraints:
    - Only allows storing tuples of two positive integers
    - Supports push (add) and pop (remove) operations
    - Keeps track of the number of elements in the stack

    Attributes:
        __head (Node): The top node of the stack
        __size (int): The current number of elements in the stack
    """

    def __init__(self):
        # Start with an empty stack (no head node)
        self.__head = None
        # Start with zero elements
        self.__size = 0

    @property
    def size(self) -> int:
        """
        Get the current number of elements in the stack.

        Returns:
            int: The number of elements in the stack
        """
        return self.__size

    def pop(self) -> tuple:
        """
        Remove and return the top element from the stack.

        Raises:
            IndexError: If trying to pop from an empty stack

        Returns:
            tuple: The top element (a tuple of two positive integers)
        """
        # Check if the stack is empty
        if self.__head is None:
            raise IndexError("Pop from empty stack")

        # Store the data from the top node
        data = self.__head.data
        # Move the head to the next node (removing the top node)
        self.__head = self.__head.next
        # Decrease the stack size
        self.__size -= 1

        return data

    def push(self, data: tuple):
        """
        Add a new element to the top of the stack.

        Validates input to ensure:
        - Input is a tuple
        - Tuple contains exactly 2 values
        - Both values are positive integers

        Args:
            data (tuple): A tuple of two positive integers to add to the stack

        Raises:
            TypeError: If input is not a tuple or contains non-integer values
            ValueError: If tuple doesn't have exactly 2 values or contains negative numbers
        """
        # Validate that input is a tuple
        if not isinstance(data, tuple):
            raise TypeError("Data must be a tuple")

        # Validate tuple length
        if len(data) != 2:
            raise ValueError("Tuple must contain exactly 2 values")

        # Validate that both values are integers
        if not (isinstance(data[0], int) and isinstance(data[1], int)):
            raise TypeError("Both values must be integers")

        # Validate that both values are non-negative
        if data[0] < 0 or data[1] < 0:
            raise ValueError("Both values must be positive integers")

        # Create a new node with the input data
        new_node = Node(data)
        # Set the new node's next pointer to the current head
        new_node.next = self.__head
        # Make the new node the new head of the stack
        self.__head = new_node
        # Increase the stack size
        self.__size += 1

    def __str__(self) -> str:
        """
        Generate a string representation of the stack.

        Converts the stack to a string in the format:
        (x1,y1) -> (x2,y2) -> ... -> (xn,yn)
        Where each tuple represents the data in a node.

        Returns:
            str: A string representation of the stack contents
        """
        # If stack is empty, return an empty string
        if self.__head is None:
            return ''

        def build_str(current: Node) -> str:
            """
            Recursive helper function to build the stack string representation.

            Builds the string from the bottom of the stack up.

            Args:
                current (Node): The current node being processed

            Returns:
                str: A string representation of the nodes from current to the end
            """
            # Base case: if we've reached the end of the stack
            if current is None:
                return ''

            # Recursively process the rest of the stack
            rest = build_str(current.next)

            # If there are more nodes, add an arrow
            if rest:
                return f'{rest} -> ({current.data[0]},{current.data[1]})'

            # For the bottom node, just return its representation
            return f'({current.data[0]},{current.data[1]})'

        # Start the string building process from the head
        return build_str(self.__head)
