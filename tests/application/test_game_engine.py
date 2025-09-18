import unittest

from game_of_life.application.game_engine import GameEngine
from game_of_life.domain.grid import Grid
from game_of_life.domain.game_rules import GameRules, StandardRules
from game_of_life.domain.position import Position


class MockRules(GameRules):
    """Mock implementation of GameRules for testing."""

    @staticmethod
    def should_cell_live(is_alive: bool, neighbor_count: int) -> bool:
        """Simple mock rule: cell lives if it has exactly 2 neighbors."""
        return neighbor_count == 2


class TestGameEngine(unittest.TestCase):
    """Comprehensive tests for GameEngine class."""

    def setUp(self):
        """Set up test fixtures."""
        self.engine = GameEngine()
        self.custom_engine = GameEngine(MockRules())

    def test_constructor_default_rules(self):
        """Test GameEngine constructor with default StandardRules."""
        engine = GameEngine()
        self.assertIsInstance(engine.rules, StandardRules)

    def test_constructor_custom_rules(self):
        """Test GameEngine constructor with custom rules."""
        custom_rules = MockRules()
        engine = GameEngine(custom_rules)
        self.assertEqual(engine.rules, custom_rules)

    def test_compute_next_generation_empty_grid(self):
        """Test compute_next_generation with empty grid returns empty grid."""
        empty_grid = Grid(10, 10, set())
        result = self.engine.compute_next_generation(empty_grid)

        self.assertEqual(result.width, 10)
        self.assertEqual(result.height, 10)
        self.assertEqual(len(result.alive_cells), 0)

    def test_compute_next_generation_single_cell_dies(self):
        """Test that a single isolated cell dies (underpopulation)."""
        grid = Grid(5, 5, {Position(2, 2)})
        result = self.engine.compute_next_generation(grid)

        self.assertEqual(len(result.alive_cells), 0)

    def test_compute_next_generation_two_cells_die(self):
        """Test that two adjacent cells both die."""
        grid = Grid(5, 5, {Position(2, 2), Position(2, 3)})
        result = self.engine.compute_next_generation(grid)

        self.assertEqual(len(result.alive_cells), 0)

    def test_compute_next_generation_block_still_life(self):
        """Test that a 2x2 block remains stable (still life)."""
        block_cells = {
            Position(1, 1), Position(1, 2),
            Position(2, 1), Position(2, 2)
        }
        grid = Grid(5, 5, block_cells)
        result = self.engine.compute_next_generation(grid)

        self.assertEqual(result.alive_cells, block_cells)

    def test_compute_next_generation_beehive_still_life(self):
        """Test that a beehive pattern remains stable."""
        beehive_cells = {
            Position(1, 2), Position(1, 3),
            Position(2, 1), Position(2, 4),
            Position(3, 2), Position(3, 3)
        }
        grid = Grid(6, 6, beehive_cells)
        result = self.engine.compute_next_generation(grid)

        self.assertEqual(result.alive_cells, beehive_cells)

    def test_compute_next_generation_blinker_oscillator(self):
        """Test blinker oscillator - horizontal line becomes vertical."""
        horizontal_blinker = {Position(2, 1), Position(2, 2), Position(2, 3)}
        grid = Grid(5, 5, horizontal_blinker)
        result = self.engine.compute_next_generation(grid)

        expected_vertical = {Position(1, 2), Position(2, 2), Position(3, 2)}
        self.assertEqual(result.alive_cells, expected_vertical)

    def test_compute_next_generation_blinker_complete_cycle(self):
        """Test complete blinker cycle - back to original after 2 generations."""
        horizontal_blinker = {Position(2, 1), Position(2, 2), Position(2, 3)}
        grid = Grid(5, 5, horizontal_blinker)

        # First generation: horizontal -> vertical
        gen1 = self.engine.compute_next_generation(grid)
        expected_vertical = {Position(1, 2), Position(2, 2), Position(3, 2)}
        self.assertEqual(gen1.alive_cells, expected_vertical)

        # Second generation: vertical -> horizontal (back to start)
        gen2 = self.engine.compute_next_generation(gen1)
        self.assertEqual(gen2.alive_cells, horizontal_blinker)

    def test_compute_next_generation_toad_oscillator(self):
        """Test toad oscillator pattern."""
        toad_gen1 = {
            Position(2, 2), Position(2, 3), Position(2, 4),
            Position(3, 1), Position(3, 2), Position(3, 3)
        }
        grid = Grid(6, 6, toad_gen1)
        result = self.engine.compute_next_generation(grid)

        # Toad should transform to its second state
        toad_gen2 = {
            Position(1, 3),
            Position(2, 1), Position(2, 4),
            Position(3, 1), Position(3, 4),
            Position(4, 2)
        }
        self.assertEqual(result.alive_cells, toad_gen2)

    def test_compute_next_generation_edge_boundary(self):
        """Test behavior at grid boundaries."""
        # Place cells at edge of 3x3 grid
        edge_cells = {Position(0, 1), Position(1, 1), Position(2, 1)}
        grid = Grid(3, 3, edge_cells)
        result = self.engine.compute_next_generation(grid)

        # Should form horizontal line at row 1
        expected = {Position(1, 0), Position(1, 1), Position(1, 2)}
        self.assertEqual(result.alive_cells, expected)

    def test_compute_next_generation_corner_boundary(self):
        """Test behavior at grid corners."""
        # Single cell in corner should die
        corner_grid = Grid(3, 3, {Position(0, 0)})
        result = self.engine.compute_next_generation(corner_grid)

        self.assertEqual(len(result.alive_cells), 0)

    def test_compute_next_generation_with_custom_rules(self):
        """Test engine works correctly with custom rules."""
        # Using MockRules: cell lives if exactly 2 neighbors
        grid = Grid(5, 5, {
            Position(1, 1), Position(1, 2), Position(1, 3)
        })
        result = self.custom_engine.compute_next_generation(grid)

        # With MockRules, any cell with exactly 2 neighbors lives
        # This includes the center cell and several new births
        expected_with_mock_rules = {
            Position(0, 1), Position(0, 3),  # New births with 2 neighbors each
            Position(1, 2),                   # Survives (2 neighbors)
            Position(2, 1), Position(2, 3)   # New births with 2 neighbors each
        }
        self.assertEqual(result.alive_cells, expected_with_mock_rules)

    def test_compute_next_generation_large_grid_performance(self):
        """Test performance optimization with large sparse grid."""
        # Create large grid with few alive cells
        large_grid = Grid(1000, 1000, {
            Position(500, 500), Position(500, 501), Position(501, 500)
        })

        # Should complete quickly due to optimization
        result = self.engine.compute_next_generation(large_grid)

        # Verify result is correct
        self.assertEqual(result.width, 1000)
        self.assertEqual(result.height, 1000)
        # This L-shaped pattern becomes a 2x2 block (stable pattern)
        expected_block = {
            Position(500, 500), Position(500, 501),
            Position(501, 500), Position(501, 501)
        }
        self.assertEqual(result.alive_cells, expected_block)

    def test_compute_next_generation_preserves_grid_dimensions(self):
        """Test that grid dimensions are preserved in result."""
        original_grid = Grid(7, 11, {Position(3, 5)})
        result = self.engine.compute_next_generation(original_grid)

        self.assertEqual(result.width, 7)
        self.assertEqual(result.height, 11)

    def test_compute_next_generation_returns_new_grid_instance(self):
        """Test that a new Grid instance is returned, not modified original."""
        original_cells = {Position(1, 1), Position(1, 2), Position(2, 1), Position(2, 2)}
        original_grid = Grid(5, 5, original_cells)
        result = self.engine.compute_next_generation(original_grid)

        # Should be different instances
        self.assertIsNot(result, original_grid)
        # Original should be unchanged
        self.assertEqual(original_grid.alive_cells, original_cells)

    def test_compute_next_generation_birth_rule(self):
        """Test cell birth rule specifically."""
        # Arrange 3 cells in L-shape to create birth scenario
        grid = Grid(5, 5, {
            Position(1, 1), Position(2, 1), Position(2, 2)
        })
        result = self.engine.compute_next_generation(grid)

        # Position(1, 2) should be born (exactly 3 neighbors)
        self.assertIn(Position(1, 2), result.alive_cells)


if __name__ == '__main__':
    unittest.main()