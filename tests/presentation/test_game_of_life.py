import unittest
from unittest.mock import Mock, patch, call
from io import StringIO

from game_of_life.presentation.game_of_life import GameOfLife
from game_of_life.domain.grid import Grid
from game_of_life.domain.position import Position
from game_of_life.application.game_engine import GameEngine
from game_of_life.infrastructure.interfaces.pattern_loader import PatternLoader
from game_of_life.infrastructure.interfaces.renderer import Renderer


class MockPatternLoader(PatternLoader):
    """Mock implementation of PatternLoader for testing."""

    def __init__(self, pattern_cells=None):
        self.pattern_cells = pattern_cells or set()

    def load(self):
        return self.pattern_cells


class MockRenderer(Renderer):
    """Mock implementation of Renderer for testing."""

    def __init__(self):
        self.render_calls = []

    def render(self, grid, generation):
        self.render_calls.append((grid, generation))


class TestGameOfLife(unittest.TestCase):
    """Comprehensive tests for GameOfLife class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_pattern_loader = MockPatternLoader()
        self.mock_renderer = MockRenderer()
        self.mock_engine = Mock(spec=GameEngine)

        self.game = GameOfLife(
            width=10,
            height=8,
            pattern_loader=self.mock_pattern_loader,
            renderer=self.mock_renderer,
            engine=self.mock_engine
        )

    def test_constructor_dependency_injection(self):
        """Test GameOfLife constructor stores dependencies correctly."""
        self.assertEqual(self.game.width, 10)
        self.assertEqual(self.game.height, 8)
        self.assertEqual(self.game.pattern_loader, self.mock_pattern_loader)
        self.assertEqual(self.game.renderer, self.mock_renderer)
        self.assertEqual(self.game.engine, self.mock_engine)

    def test_constructor_initial_state(self):
        """Test GameOfLife constructor sets correct initial state."""
        self.assertEqual(self.game.generation, 0)
        self.assertEqual(self.game.grid.width, 10)
        self.assertEqual(self.game.grid.height, 8)
        self.assertEqual(len(self.game.grid.alive_cells), 0)

    def test_load_pattern_without_offset(self):
        """Test loading pattern without offset."""
        pattern_cells = {Position(1, 1), Position(1, 2), Position(2, 1)}
        self.mock_pattern_loader.pattern_cells = pattern_cells

        self.game.load_pattern()

        self.assertEqual(self.game.grid.alive_cells, pattern_cells)
        self.assertEqual(self.game.generation, 0)

    def test_load_pattern_with_positive_offset(self):
        """Test loading pattern with positive offset."""
        original_pattern = {Position(0, 0), Position(0, 1), Position(1, 0)}
        self.mock_pattern_loader.pattern_cells = original_pattern

        self.game.load_pattern(offset=(2, 3))

        expected_pattern = {Position(2, 3), Position(2, 4), Position(3, 3)}
        self.assertEqual(self.game.grid.alive_cells, expected_pattern)
        self.assertEqual(self.game.generation, 0)

    def test_load_pattern_with_negative_offset(self):
        """Test loading pattern with negative offset (if result is valid)."""
        original_pattern = {Position(5, 5), Position(5, 6), Position(6, 5)}
        self.mock_pattern_loader.pattern_cells = original_pattern

        self.game.load_pattern(offset=(-2, -2))

        expected_pattern = {Position(3, 3), Position(3, 4), Position(4, 3)}
        self.assertEqual(self.game.grid.alive_cells, expected_pattern)

    def test_load_pattern_out_of_bounds_raises_error(self):
        """Test loading pattern with positions outside grid bounds raises ValueError."""
        # Pattern that would go outside 10x8 grid with offset
        pattern_cells = {Position(8, 8), Position(8, 9)}
        self.mock_pattern_loader.pattern_cells = pattern_cells

        with self.assertRaises(ValueError) as context:
            self.game.load_pattern(offset=(1, 1))

        self.assertIn("is not a valid position", str(context.exception))

    def test_load_pattern_resets_generation(self):
        """Test that loading pattern resets generation to 0."""
        # Advance generation first
        self.game.generation = 5

        pattern_cells = {Position(1, 1)}
        self.mock_pattern_loader.pattern_cells = pattern_cells

        self.game.load_pattern()

        self.assertEqual(self.game.generation, 0)

    def test_load_pattern_empty_pattern(self):
        """Test loading empty pattern."""
        self.mock_pattern_loader.pattern_cells = set()

        self.game.load_pattern()

        self.assertEqual(len(self.game.grid.alive_cells), 0)
        self.assertEqual(self.game.generation, 0)

    def test_step_calls_engine_compute_next_generation(self):
        """Test step method calls engine.compute_next_generation."""
        # Set up initial state and mock response
        initial_grid = self.game.grid
        next_grid = Grid(10, 8, {Position(2, 2)})
        self.mock_engine.compute_next_generation.return_value = next_grid

        self.game.step()

        self.mock_engine.compute_next_generation.assert_called_once_with(initial_grid)

    def test_step_updates_grid_and_generation(self):
        """Test step method updates grid and increments generation."""
        initial_generation = self.game.generation
        next_grid = Grid(10, 8, {Position(3, 3)})
        self.mock_engine.compute_next_generation.return_value = next_grid

        self.game.step()

        self.assertEqual(self.game.grid, next_grid)
        self.assertEqual(self.game.generation, initial_generation + 1)

    def test_step_multiple_times(self):
        """Test multiple step calls work correctly."""
        grids = [
            Grid(10, 8, {Position(1, 1)}),
            Grid(10, 8, {Position(2, 2)}),
            Grid(10, 8, {Position(3, 3)})
        ]
        self.mock_engine.compute_next_generation.side_effect = grids

        for i, expected_grid in enumerate(grids):
            self.game.step()
            self.assertEqual(self.game.grid, expected_grid)
            self.assertEqual(self.game.generation, i + 1)

    @patch('time.sleep')
    def test_run_finite_generations(self, mock_sleep):
        """Test run method with finite generations."""
        # Start with alive cells to prevent immediate extinction
        self.game.grid = Grid(10, 8, {Position(0, 0)})

        # Setup engine to return different grids for each generation
        grids = [Grid(10, 8, {Position(i, i)}) for i in range(1, 4)]
        self.mock_engine.compute_next_generation.side_effect = grids

        self.game.run(generations=3, delay=0.1)

        # Should render 3 times: initial, gen1, gen2 (loop exits before gen3 render)
        self.assertEqual(len(self.mock_renderer.render_calls), 3)
        self.assertEqual(self.game.generation, 3)
        self.assertEqual(mock_sleep.call_count, 3)
        mock_sleep.assert_has_calls([call(0.1)] * 3)

    @patch('time.sleep')
    def test_run_zero_generations(self, mock_sleep):
        """Test run method with zero generations."""
        # Start with alive cells to avoid immediate extinction detection
        self.game.grid = Grid(10, 8, {Position(1, 1)})

        self.game.run(generations=0, delay=0.1)

        # With generations=0, loop never executes, so no renders
        self.assertEqual(len(self.mock_renderer.render_calls), 0)
        self.assertEqual(self.game.generation, 0)
        mock_sleep.assert_not_called()

    @patch('time.sleep')
    @patch('builtins.print')
    def test_run_stops_on_stable_pattern(self, mock_print, mock_sleep):
        """Test run method stops when pattern stabilizes."""
        # Start with alive cells
        initial_pattern = {Position(1, 1), Position(1, 2)}
        self.game.grid = Grid(10, 8, initial_pattern)

        # Engine returns the same pattern, creating stability
        stable_grid = Grid(10, 8, initial_pattern)
        self.mock_engine.compute_next_generation.return_value = stable_grid

        self.game.run(delay=0.01, stop_on_stable=True)

        # Should detect stability after pattern repeats (at generation 1)
        self.assertEqual(self.game.generation, 1)
        mock_print.assert_called_with("\nPattern stabilized at generation 1")

    @patch('time.sleep')
    @patch('builtins.print')
    def test_run_stops_on_oscillating_pattern(self, mock_print, mock_sleep):
        """Test run method stops when pattern oscillates."""
        # Start with initial pattern
        initial_pattern = {Position(1, 1)}
        self.game.grid = Grid(10, 8, initial_pattern)

        # Create oscillation: initial -> grid2 -> back to initial
        grid2 = Grid(10, 8, {Position(2, 2)})
        grid_back_to_initial = Grid(10, 8, initial_pattern)
        self.mock_engine.compute_next_generation.side_effect = [grid2, grid_back_to_initial]

        self.game.run(delay=0.01, stop_on_stable=True)

        # Should detect oscillation when initial pattern appears again
        self.assertEqual(self.game.generation, 2)
        mock_print.assert_called_with("\nPattern stabilized at generation 2")

    @patch('time.sleep')
    @patch('builtins.print')
    def test_run_stops_on_extinction(self, mock_print, mock_sleep):
        """Test run method stops when all cells die."""
        empty_grid = Grid(10, 8, set())
        self.mock_engine.compute_next_generation.return_value = empty_grid

        # Start with some alive cells
        self.game.grid = Grid(10, 8, {Position(1, 1)})

        self.game.run(delay=0.01)

        self.assertEqual(self.game.generation, 1)
        mock_print.assert_called_with("\nAll cells died at generation 1")

    @patch('time.sleep')
    @patch('builtins.print')
    def test_run_handles_keyboard_interrupt(self, mock_print, mock_sleep):
        """Test run method handles KeyboardInterrupt gracefully."""
        # Start with alive cells to avoid immediate extinction
        self.game.grid = Grid(10, 8, {Position(1, 1)})
        self.mock_engine.compute_next_generation.return_value = Grid(10, 8, {Position(2, 2)})

        mock_sleep.side_effect = KeyboardInterrupt()

        self.game.run(delay=0.1)

        mock_print.assert_called_with("\nSimulation stopped at generation 0")

    @patch('time.sleep')
    def test_run_infinite_generations_parameter(self, mock_sleep):
        """Test run method with None generations parameter."""
        # Setup to stop after 2 generations due to extinction
        empty_grid = Grid(10, 8, set())
        non_empty_grid = Grid(10, 8, {Position(1, 1)})
        self.mock_engine.compute_next_generation.side_effect = [non_empty_grid, empty_grid]

        self.game.grid = Grid(10, 8, {Position(2, 2)})

        with patch('builtins.print'):
            self.game.run(generations=None, delay=0.01)

        # Should run until extinction
        self.assertEqual(self.game.generation, 2)

    @patch('time.sleep')
    def test_run_renderer_called_each_generation(self, mock_sleep):
        """Test run method calls renderer for each generation."""
        # Start with alive cells to prevent extinction
        self.game.grid = Grid(10, 8, {Position(0, 0)})

        grids = [Grid(10, 8, {Position(i, i)}) for i in range(1, 3)]
        self.mock_engine.compute_next_generation.side_effect = grids

        self.game.run(generations=2, delay=0.01)

        # Should render: initial, gen1 = 2 times
        self.assertEqual(len(self.mock_renderer.render_calls), 2)

        # Check renderer was called with correct generation numbers
        expected_generations = [0, 1]  # Initial, then after first step
        actual_generations = [call[1] for call in self.mock_renderer.render_calls]
        self.assertEqual(actual_generations, expected_generations)

    @patch('time.sleep')
    def test_run_stop_on_stable_false_ignores_stability(self, mock_sleep):
        """Test run method ignores stability when stop_on_stable=False."""
        # Start with alive cells
        self.game.grid = Grid(10, 8, {Position(1, 1)})

        stable_grid = Grid(10, 8, {Position(1, 1)})
        self.mock_engine.compute_next_generation.return_value = stable_grid

        self.game.run(generations=3, delay=0.01, stop_on_stable=False)

        # Should run full 3 generations despite stability
        self.assertEqual(self.game.generation, 3)
        self.assertEqual(len(self.mock_renderer.render_calls), 3)

    def test_integration_load_and_run(self):
        """Test integration of load_pattern and run methods."""
        # Setup pattern
        pattern_cells = {Position(1, 1), Position(1, 2)}
        self.mock_pattern_loader.pattern_cells = pattern_cells

        # Setup engine response
        next_grid = Grid(10, 8, {Position(2, 2)})
        self.mock_engine.compute_next_generation.return_value = next_grid

        # Load pattern and run
        self.game.load_pattern(offset=(2, 2))

        with patch('time.sleep'):
            self.game.run(generations=1, delay=0.01)

        # Verify pattern was loaded with offset
        expected_loaded = {Position(3, 3), Position(3, 4)}
        # Engine should have been called with the loaded pattern grid
        engine_call_grid = self.mock_engine.compute_next_generation.call_args[0][0]
        self.assertEqual(engine_call_grid.alive_cells, expected_loaded)

        # Verify final state
        self.assertEqual(self.game.grid, next_grid)
        self.assertEqual(self.game.generation, 1)

    def test_edge_case_1x1_grid(self):
        """Test GameOfLife with minimal 1x1 grid."""
        small_game = GameOfLife(
            width=1,
            height=1,
            pattern_loader=MockPatternLoader(),
            renderer=MockRenderer(),
            engine=Mock(spec=GameEngine)
        )

        self.assertEqual(small_game.width, 1)
        self.assertEqual(small_game.height, 1)
        self.assertEqual(len(small_game.grid.alive_cells), 0)

    def test_edge_case_large_grid_dimensions(self):
        """Test GameOfLife with large grid dimensions."""
        large_game = GameOfLife(
            width=1000,
            height=500,
            pattern_loader=MockPatternLoader(),
            renderer=MockRenderer(),
            engine=Mock(spec=GameEngine)
        )

        self.assertEqual(large_game.width, 1000)
        self.assertEqual(large_game.height, 500)

    def test_load_pattern_at_grid_boundary(self):
        """Test loading pattern that exactly fits at grid boundary."""
        # Pattern that exactly fits in bottom-right corner
        pattern_cells = {Position(0, 0)}
        self.mock_pattern_loader.pattern_cells = pattern_cells

        # Place it at the last valid position
        self.game.load_pattern(offset=(7, 9))  # 8-1, 10-1 for 0-indexed

        expected_pattern = {Position(7, 9)}
        self.assertEqual(self.game.grid.alive_cells, expected_pattern)

    @patch('time.sleep')
    def test_run_with_custom_delay(self, mock_sleep):
        """Test run method respects custom delay parameter."""
        self.mock_engine.compute_next_generation.return_value = Grid(10, 8, set())

        # Start with alive cell to prevent immediate extinction
        self.game.grid = Grid(10, 8, {Position(1, 1)})

        with patch('builtins.print'):
            self.game.run(generations=1, delay=0.5)

        mock_sleep.assert_called_once_with(0.5)

    @patch('time.sleep')
    def test_run_history_management(self, mock_sleep):
        """Test run method manages history correctly for oscillation detection."""
        # Start with alive cells
        self.game.grid = Grid(10, 8, {Position(0, 0)})

        # Create sequence longer than max_history (5) without repetition
        grids = [Grid(10, 8, {Position(i, 0)}) for i in range(1, 8)]
        self.mock_engine.compute_next_generation.side_effect = grids

        self.game.run(generations=7, delay=0.01, stop_on_stable=True)

        # Should complete all 7 generations without stopping
        self.assertEqual(self.game.generation, 7)


if __name__ == '__main__':
    unittest.main()