import unittest
from game_of_life.domain.game_rules import GameRules, StandardRules


class TestGameRules(unittest.TestCase):
    def test_abstract_base_class(self):
        """Test that GameRules is abstract and cannot be instantiated."""
        with self.assertRaises(TypeError):
            GameRules()


class TestStandardRules(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.rules = StandardRules()

    def test_cell_survival_with_2_neighbors(self):
        """Test that live cell with 2 neighbors survives."""
        self.assertTrue(self.rules.should_cell_live(True, 2))

    def test_cell_survival_with_3_neighbors(self):
        """Test that live cell with 3 neighbors survives."""
        self.assertTrue(self.rules.should_cell_live(True, 3))

    def test_cell_death_with_underpopulation(self):
        """Test that live cell dies with fewer than 2 neighbors."""
        self.assertFalse(self.rules.should_cell_live(True, 0))
        self.assertFalse(self.rules.should_cell_live(True, 1))

    def test_cell_death_with_overpopulation(self):
        """Test that live cell dies with more than 3 neighbors."""
        self.assertFalse(self.rules.should_cell_live(True, 4))
        self.assertFalse(self.rules.should_cell_live(True, 5))
        self.assertFalse(self.rules.should_cell_live(True, 6))
        self.assertFalse(self.rules.should_cell_live(True, 7))
        self.assertFalse(self.rules.should_cell_live(True, 8))

    def test_cell_birth_with_3_neighbors(self):
        """Test that dead cell with exactly 3 neighbors becomes alive."""
        self.assertTrue(self.rules.should_cell_live(False, 3))

    def test_dead_cell_stays_dead_insufficient_neighbors(self):
        """Test that dead cell stays dead with insufficient neighbors."""
        self.assertFalse(self.rules.should_cell_live(False, 0))
        self.assertFalse(self.rules.should_cell_live(False, 1))
        self.assertFalse(self.rules.should_cell_live(False, 2))

    def test_dead_cell_stays_dead_too_many_neighbors(self):
        """Test that dead cell stays dead with too many neighbors."""
        self.assertFalse(self.rules.should_cell_live(False, 4))
        self.assertFalse(self.rules.should_cell_live(False, 5))
        self.assertFalse(self.rules.should_cell_live(False, 6))
        self.assertFalse(self.rules.should_cell_live(False, 7))
        self.assertFalse(self.rules.should_cell_live(False, 8))

    def test_all_neighbor_combinations_alive_cell(self):
        """Test all possible neighbor combinations for alive cell."""
        # Expected results for alive cell with 0-8 neighbors
        expected_results = [False, False, True, True, False, False, False, False, False]

        for neighbor_count in range(9):
            result = self.rules.should_cell_live(True, neighbor_count)
            expected = expected_results[neighbor_count]
            self.assertEqual(
                result, expected,
                f"Alive cell with {neighbor_count} neighbors should {'live' if expected else 'die'}"
            )

    def test_all_neighbor_combinations_dead_cell(self):
        """Test all possible neighbor combinations for dead cell."""
        # Expected results for dead cell with 0-8 neighbors
        expected_results = [False, False, False, True, False, False, False, False, False]

        for neighbor_count in range(9):
            result = self.rules.should_cell_live(False, neighbor_count)
            expected = expected_results[neighbor_count]
            self.assertEqual(
                result, expected,
                f"Dead cell with {neighbor_count} neighbors should {'become alive' if expected else 'stay dead'}"
            )

    def test_conway_rules_documentation(self):
        """Test specific Conway's Game of Life scenarios mentioned in documentation."""
        # Rule 1: Any living cell with 2 or 3 neighbors survives
        self.assertTrue(self.rules.should_cell_live(True, 2))
        self.assertTrue(self.rules.should_cell_live(True, 3))

        # Rule 2: Any dead cell with exactly 3 neighbors becomes alive
        self.assertTrue(self.rules.should_cell_live(False, 3))

        # Rule 3: All other cells die or stay dead
        # Live cells with wrong neighbor counts die
        for count in [0, 1, 4, 5, 6, 7, 8]:
            self.assertFalse(self.rules.should_cell_live(True, count))

        # Dead cells with wrong neighbor counts stay dead
        for count in [0, 1, 2, 4, 5, 6, 7, 8]:
            self.assertFalse(self.rules.should_cell_live(False, count))

    def test_static_method_behavior(self):
        """Test that should_cell_live can be called as static method."""
        # Should work without instance
        self.assertTrue(StandardRules.should_cell_live(True, 2))
        self.assertTrue(StandardRules.should_cell_live(False, 3))
        self.assertFalse(StandardRules.should_cell_live(True, 4))

    def test_edge_case_maximum_neighbors(self):
        """Test behavior with maximum possible neighbors (8)."""
        self.assertFalse(self.rules.should_cell_live(True, 8))
        self.assertFalse(self.rules.should_cell_live(False, 8))

    def test_edge_case_minimum_neighbors(self):
        """Test behavior with minimum possible neighbors (0)."""
        self.assertFalse(self.rules.should_cell_live(True, 0))
        self.assertFalse(self.rules.should_cell_live(False, 0))