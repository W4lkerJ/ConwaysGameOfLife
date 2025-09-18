import unittest
from game_of_life.domain.position import Position


class TestPosition(unittest.TestCase):
    def test_position_creation(self):
        """Test basic position creation."""
        pos = Position(5, 10)
        self.assertEqual(pos.row, 5)
        self.assertEqual(pos.col, 10)

    def test_position_equality(self):
        """Test position equality comparison."""
        pos1 = Position(3, 4)
        pos2 = Position(3, 4)
        pos3 = Position(3, 5)

        self.assertEqual(pos1, pos2)
        self.assertNotEqual(pos1, pos3)

    def test_position_immutability(self):
        """Test that position is immutable (frozen dataclass)."""
        pos = Position(1, 2)

        # Attempting to modify should raise AttributeError
        with self.assertRaises(AttributeError):
            pos.row = 5
        with self.assertRaises(AttributeError):
            pos.col = 10

    def test_get_neighbors_count(self):
        """Test that get_neighbors returns exactly 8 neighbors."""
        pos = Position(5, 5)
        neighbors = pos.get_neighbors()
        self.assertEqual(len(neighbors), 8)

    def test_get_neighbors_positions(self):
        """Test that get_neighbors returns correct neighbor positions."""
        pos = Position(5, 5)
        neighbors = pos.get_neighbors()

        expected_neighbors = [
            Position(4, 4), Position(4, 5), Position(4, 6),
            Position(5, 4),                 Position(5, 6),
            Position(6, 4), Position(6, 5), Position(6, 6)
        ]

        self.assertEqual(set(neighbors), set(expected_neighbors))

    def test_get_neighbors_excludes_self(self):
        """Test that get_neighbors doesn't include the position itself."""
        pos = Position(3, 3)
        neighbors = pos.get_neighbors()
        self.assertNotIn(pos, neighbors)

    def test_get_neighbors_origin(self):
        """Test get_neighbors for position at origin."""
        pos = Position(0, 0)
        neighbors = pos.get_neighbors()

        expected_neighbors = [
            Position(-1, -1), Position(-1, 0), Position(-1, 1),
            Position(0, -1),                   Position(0, 1),
            Position(1, -1),  Position(1, 0),  Position(1, 1)
        ]

        self.assertEqual(set(neighbors), set(expected_neighbors))

    def test_get_neighbors_negative_coordinates(self):
        """Test get_neighbors for negative coordinates."""
        pos = Position(-2, -3)
        neighbors = pos.get_neighbors()

        expected_neighbors = [
            Position(-3, -4), Position(-3, -3), Position(-3, -2),
            Position(-2, -4),                   Position(-2, -2),
            Position(-1, -4), Position(-1, -3), Position(-1, -2)
        ]

        self.assertEqual(set(neighbors), set(expected_neighbors))

    def test_position_string_representation(self):
        """Test string representation of position."""
        pos = Position(1, 2)
        # Testing that it has a reasonable string representation
        str_repr = str(pos)
        self.assertIn("1", str_repr)
        self.assertIn("2", str_repr)