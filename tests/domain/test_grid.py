import unittest
from game_of_life.domain.grid import Grid
from game_of_life.domain.position import Position
from game_of_life.domain.cell_state import CellState


class TestGrid(unittest.TestCase):
    def test_grid_initialization(self):
        """Test grid creation with different parameters."""
        alive_cells = {Position(1, 1), Position(2, 2)}
        grid = Grid(10, 15, alive_cells)

        self.assertEqual(grid.width, 10)
        self.assertEqual(grid.height, 15)
        self.assertEqual(grid.alive_cells, alive_cells)

    def test_empty_grid_initialization(self):
        """Test creating an empty grid."""
        grid = Grid(5, 5, set())
        self.assertEqual(len(grid.alive_cells), 0)

    def test_is_valid_position_within_bounds(self):
        """Test position validation for positions within grid bounds."""
        grid = Grid(10, 10, set())

        # Test corners
        self.assertTrue(grid.is_valid_position(Position(0, 0)))
        self.assertTrue(grid.is_valid_position(Position(9, 9)))
        self.assertTrue(grid.is_valid_position(Position(0, 9)))
        self.assertTrue(grid.is_valid_position(Position(9, 0)))

        # Test middle positions
        self.assertTrue(grid.is_valid_position(Position(5, 5)))

    def test_is_valid_position_outside_bounds(self):
        """Test position validation for positions outside grid bounds."""
        grid = Grid(10, 10, set())

        # Test negative coordinates
        self.assertFalse(grid.is_valid_position(Position(-1, 0)))
        self.assertFalse(grid.is_valid_position(Position(0, -1)))
        self.assertFalse(grid.is_valid_position(Position(-1, -1)))

        # Test coordinates beyond bounds
        self.assertFalse(grid.is_valid_position(Position(10, 0)))
        self.assertFalse(grid.is_valid_position(Position(0, 10)))
        self.assertFalse(grid.is_valid_position(Position(10, 10)))

    def test_get_cell_state_alive(self):
        """Test getting state of alive cells."""
        alive_cells = {Position(2, 3), Position(4, 5)}
        grid = Grid(10, 10, alive_cells)

        self.assertEqual(grid.get_cell_state(Position(2, 3)), CellState.ALIVE)
        self.assertEqual(grid.get_cell_state(Position(4, 5)), CellState.ALIVE)

    def test_get_cell_state_dead(self):
        """Test getting state of dead cells."""
        alive_cells = {Position(2, 3)}
        grid = Grid(10, 10, alive_cells)

        self.assertEqual(grid.get_cell_state(Position(0, 0)), CellState.DEAD)
        self.assertEqual(grid.get_cell_state(Position(5, 5)), CellState.DEAD)
        self.assertEqual(grid.get_cell_state(Position(9, 9)), CellState.DEAD)

    def test_neighbor_counting(self):
        """Test neighbor counting for basic patterns."""
        # Create a small pattern
        alive_cells = {Position(1, 1), Position(1, 2), Position(2, 1)}
        grid = Grid(5, 5, alive_cells)

        # Position (1,1) should have 2 neighbors
        self.assertEqual(grid.count_alive_neighbors(Position(1, 1)), 2)
        # Position (2,2) should have 3 neighbors
        self.assertEqual(grid.count_alive_neighbors(Position(2, 2)), 3)

    def test_neighbor_counting_empty_grid(self):
        """Test neighbor counting on empty grid."""
        grid = Grid(5, 5, set())

        # Any position should have 0 neighbors
        self.assertEqual(grid.count_alive_neighbors(Position(2, 2)), 0)
        self.assertEqual(grid.count_alive_neighbors(Position(0, 0)), 0)

    def test_neighbor_counting_single_cell(self):
        """Test neighbor counting with single alive cell."""
        alive_cells = {Position(2, 2)}
        grid = Grid(5, 5, alive_cells)

        # The cell itself should have 0 neighbors
        self.assertEqual(grid.count_alive_neighbors(Position(2, 2)), 0)

        # Adjacent cells should have 1 neighbor
        self.assertEqual(grid.count_alive_neighbors(Position(1, 1)), 1)
        self.assertEqual(grid.count_alive_neighbors(Position(1, 2)), 1)
        self.assertEqual(grid.count_alive_neighbors(Position(3, 3)), 1)

        # Distant cells should have 0 neighbors
        self.assertEqual(grid.count_alive_neighbors(Position(0, 0)), 0)
        self.assertEqual(grid.count_alive_neighbors(Position(4, 4)), 0)

    def test_neighbor_counting_boundary_conditions(self):
        """Test neighbor counting at grid boundaries."""
        # Place cell at corner
        alive_cells = {Position(0, 0)}
        grid = Grid(3, 3, alive_cells)

        # Corner cell should count its neighbors correctly
        # (Only 3 possible neighbors exist for corner position)
        self.assertEqual(grid.count_alive_neighbors(Position(1, 1)), 1)

        # Place cells around the corner
        alive_cells = {Position(0, 1), Position(1, 0), Position(1, 1)}
        grid = Grid(3, 3, alive_cells)

        # Corner position should have 3 neighbors
        self.assertEqual(grid.count_alive_neighbors(Position(0, 0)), 3)

    def test_get_all_positions_to_check_empty_grid(self):
        """Test getting positions to check on empty grid."""
        grid = Grid(5, 5, set())
        positions = grid.get_all_positions_to_check()
        self.assertEqual(len(positions), 0)

    def test_get_all_positions_to_check_single_cell(self):
        """Test getting positions to check with single alive cell."""
        alive_cells = {Position(2, 2)}
        grid = Grid(5, 5, alive_cells)
        positions = grid.get_all_positions_to_check()

        # Should include the cell itself plus its 8 neighbors
        expected_positions = {
            Position(2, 2),  # The cell itself
            Position(1, 1), Position(1, 2), Position(1, 3),
            Position(2, 1),                  Position(2, 3),
            Position(3, 1), Position(3, 2), Position(3, 3)
        }

        self.assertEqual(positions, expected_positions)

    def test_get_all_positions_to_check_boundary_cell(self):
        """Test getting positions to check for cell at grid boundary."""
        alive_cells = {Position(0, 0)}  # Corner cell
        grid = Grid(3, 3, alive_cells)
        positions = grid.get_all_positions_to_check()

        # Should only include valid positions (no negative coordinates)
        expected_positions = {
            Position(0, 0),  # The cell itself
            Position(0, 1), Position(1, 0), Position(1, 1)
        }

        self.assertEqual(positions, expected_positions)

    def test_get_all_positions_to_check_multiple_cells(self):
        """Test getting positions to check with multiple alive cells."""
        alive_cells = {Position(1, 1), Position(1, 2)}
        grid = Grid(5, 5, alive_cells)
        positions = grid.get_all_positions_to_check()

        # Should include both cells and all their neighbors (with overlap)
        expected_positions = {
            # Around Position(1, 1)
            Position(0, 0), Position(0, 1), Position(0, 2),
            Position(1, 0), Position(1, 1), Position(1, 2),
            Position(2, 0), Position(2, 1), Position(2, 2),
            # Additional from Position(1, 2)
            Position(0, 3), Position(1, 3), Position(2, 3)
        }

        self.assertEqual(positions, expected_positions)

    def test_neighbor_counting_full_neighborhood(self):
        """Test neighbor counting with full 8-neighbor setup."""
        center = Position(2, 2)
        # Place all 8 neighbors around center
        alive_cells = {
            Position(1, 1), Position(1, 2), Position(1, 3),
            Position(2, 1),                  Position(2, 3),
            Position(3, 1), Position(3, 2), Position(3, 3)
        }
        grid = Grid(5, 5, alive_cells)

        # Center should have 8 neighbors
        self.assertEqual(grid.count_alive_neighbors(center), 8)

        # Test specific positions manually for accuracy
        # Corner (1,1) has neighbors: (1,2) and (2,1) that are alive
        self.assertEqual(grid.count_alive_neighbors(Position(1, 1)), 2)

        # Corner (1,3) has neighbors: (1,2) and (2,3) that are alive
        self.assertEqual(grid.count_alive_neighbors(Position(1, 3)), 2)

        # Corner (3,1) has neighbors: (2,1) and (3,2) that are alive
        self.assertEqual(grid.count_alive_neighbors(Position(3, 1)), 2)

        # Corner (3,3) has neighbors: (2,3) and (3,2) that are alive
        self.assertEqual(grid.count_alive_neighbors(Position(3, 3)), 2)

        # Edge (1,2) has neighbors: (1,1), (1,3), (2,1), (2,3) that are alive
        self.assertEqual(grid.count_alive_neighbors(Position(1, 2)), 4)

        # Edge (2,1) has neighbors: (1,1), (1,2), (3,1), (3,2) that are alive
        self.assertEqual(grid.count_alive_neighbors(Position(2, 1)), 4)

        # Edge (2,3) has neighbors: (1,2), (1,3), (3,2), (3,3) that are alive
        self.assertEqual(grid.count_alive_neighbors(Position(2, 3)), 4)

        # Edge (3,2) has neighbors: (2,1), (2,3), (3,1), (3,3) that are alive
        self.assertEqual(grid.count_alive_neighbors(Position(3, 2)), 4)