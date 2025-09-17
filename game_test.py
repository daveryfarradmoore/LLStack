import unittest
from game import Map, InvalidCoordinateError, OutOfBoundaries
from llstack import LLStack


class LLStackTest(unittest.TestCase):
    def setUp(self):
        self.stack = LLStack()

    def test_initial_size(self):
        """Test that a new stack starts with size 0"""
        self.assertEqual(self.stack.size, 0)

    def test_push_increases_size(self):
        """Test that push increases the stack size"""
        self.stack.push((1, 2))
        self.assertEqual(self.stack.size, 1)

    def test_pop_decreases_size(self):
        """Test that pop decreases the stack size"""
        self.stack.push((1, 2))
        self.stack.pop()
        self.assertEqual(self.stack.size, 0)

    def test_push_invalid_type(self):
        """Test pushing non-tuple data raises TypeError"""
        with self.assertRaises(TypeError):
            self.stack.push("not a tuple")

    def test_push_invalid_tuple_length(self):
        """Test pushing tuple with incorrect length raises ValueError"""
        with self.assertRaises(ValueError):
            self.stack.push((1,))

    def test_push_invalid_tuple_values(self):
        """Test pushing tuple with non-integer values raises TypeError"""
        with self.assertRaises(TypeError):
            self.stack.push((1, 'a'))

    def test_push_negative_values(self):
        """Test pushing tuple with negative values raises ValueError"""
        with self.assertRaises(ValueError):
            self.stack.push((-1, 2))

    def test_pop_from_empty_stack(self):
        """Test popping from an empty stack raises IndexError"""
        with self.assertRaises(IndexError):
            self.stack.pop()

    def test_multiple_push_and_pop(self):
        """Test multiple push and pop operations"""
        test_data = [(1, 2), (3, 4), (5, 6)]
        for data in test_data:
            self.stack.push(data)

        # Pop should return in reverse order
        for data in reversed(test_data):
            self.assertEqual(self.stack.pop(), data)

    def test_str_representation(self):
        """Test string representation of the stack"""
        self.stack.push((1, 2))
        self.stack.push((3, 4))
        self.assertEqual(str(self.stack), '(1,2) -> (3,4)')

        self.stack = LLStack()
        self.assertEqual(str(self.stack), '')


class MapTest(unittest.TestCase):
    def setUp(self):
        # Basic grid for most tests
        self.basic_grid = [
            ['grass', 'grass', 'grass'],
            ['grass', 'ocean', 'grass'],
            ['grass', 'grass', 'grass']
        ]

    def test_map_constructor(self):
        """Test valid map creation"""
        map_obj = Map(self.basic_grid, (0, 0), (2, 2))
        self.assertEqual(map_obj.grid, self.basic_grid)

        # Test invalid grid types
        with self.assertRaises(TypeError):
            Map('not a list', (0, 0), (2, 2))
        with self.assertRaises(TypeError):
            Map([['not', 'a'], ['string']], (0, 0), (2, 2))
        with self.assertRaises(ValueError):
            Map([['invalid', 'type']], (0, 0), (2, 2))

    def test_start_coords_property(self):
        """Test start coordinates property"""
        map_obj = Map(self.basic_grid, (0, 0), (2, 2))
        self.assertEqual(map_obj.start_coords, (0, 0))

        # Test invalid start coordinates
        with self.assertRaises(TypeError):
            Map(self.basic_grid, 'not a tuple', (2, 2))
        with self.assertRaises(ValueError):
            Map(self.basic_grid, (0,), (2, 2))
        with self.assertRaises(TypeError):
            Map(self.basic_grid, (0, 'a'), (2, 2))
        with self.assertRaises(ValueError):
            Map(self.basic_grid, (-1, 0), (2, 2))
        with self.assertRaises(OutOfBoundaries):
            Map(self.basic_grid, (5, 0), (2, 2))
        with self.assertRaises(InvalidCoordinateError):
            Map([['ocean', 'grass'], ['grass', 'grass']], (0, 0), (1, 1))

    def test_end_coords_property(self):
        """Test end coordinates property"""
        map_obj = Map(self.basic_grid, (0, 0), (2, 2))
        self.assertEqual(map_obj.end_coords, (2, 2))

        # Test invalid end coordinates
        with self.assertRaises(TypeError):
            Map(self.basic_grid, (0, 0), 'not a tuple')
        with self.assertRaises(ValueError):
            Map(self.basic_grid, (0, 0), (0,))
        with self.assertRaises(TypeError):
            Map(self.basic_grid, (0, 0), (0, 'a'))
        with self.assertRaises(ValueError):
            Map(self.basic_grid, (0, 0), (-1, 0))
        with self.assertRaises(OutOfBoundaries):
            Map(self.basic_grid, (0, 0), (5, 0))
        with self.assertRaises(InvalidCoordinateError):
            Map([['grass', 'grass'], ['grass', 'ocean']], (0, 0), (1, 1))
        with self.assertRaises(ValueError):
            Map(self.basic_grid, (0, 0), (0, 0))

    def test_path_finding(self):
        """Test finding a valid path"""
        grid = [
            ['grass', 'grass', 'grass'],
            ['grass', 'ocean', 'grass'],
            ['grass', 'grass', 'grass']
        ]
        map_obj = Map(grid, (0, 0), (2, 2))
        path = map_obj.find_path()

        self.assertIsNotNone(path)
        self.assertIsInstance(path, LLStack)
        self.assertTrue(path.size > 0)

        # Verify path starts and ends at correct locations
        self.assertEqual(path.peek(), (2, 2))
        last = path.pop()
        while path.size > 0:
            last = path.pop()
        self.assertEqual(last, (0, 0))

    def test_no_path_scenario(self):
        """Test scenario with no possible path"""
        grid = [
            ['grass', 'ocean', 'grass'],
            ['ocean', 'ocean', 'ocean'],
            ['grass', 'ocean', 'grass']
        ]
        map_obj = Map(grid, (0, 0), (2, 2))
        path = map_obj.find_path()

        self.assertIsNone(path)

    def test_shortest_path(self):
        """Test finding the shortest path"""
        grid = [
            ['grass', 'grass', 'grass', 'grass'],
            ['grass', 'ocean', 'ocean', 'grass'],
            ['grass', 'grass', 'grass', 'grass']
        ]
        map_obj = Map(grid, (0, 0), (2, 3))
        path = map_obj.find_shortest_path()

        self.assertIsNotNone(path)
        self.assertIsInstance(path, LLStack)
        self.assertTrue(path.size > 0)

        # Verify path starts and ends at correct locations
        self.assertEqual(path.peek(), (2, 3))
        last = path.pop()
        while path.size > 0:
            last = path.pop()
        self.assertEqual(last, (0, 0))

    def test_no_path_in_shortest_path(self):
        """Test shortest path when no path exists"""
        grid = [
            ['grass', 'ocean', 'grass'],
            ['ocean', 'ocean', 'ocean'],
            ['grass', 'ocean', 'grass']
        ]
        map_obj = Map(grid, (0, 0), (2, 2))
        path = map_obj.find_shortest_path()

        self.assertIsNone(path)

    def test_grid_integrity(self):
        """Test that original grid is not modified during path finding"""
        grid = [
            ['grass', 'grass', 'grass'],
            ['grass', 'ocean', 'grass'],
            ['grass', 'grass', 'grass']
        ]
        original_grid = [row[:] for row in grid]
        map_obj = Map(grid, (0, 0), (2, 2))

        map_obj.find_path()
        map_obj.find_shortest_path()

        # Verify grid remains unchanged
        self.assertEqual(grid, original_grid)


if __name__ == '__main__':
    unittest.main()