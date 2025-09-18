# tests/test_domain.py
import unittest
from game_of_life.domain.game_rules import GameRules


class TestGameRules(unittest.TestCase):
    def test_cell_survival(self):
        rules = GameRules()
        # Live cell with 2 neighbors survives
        self.assertTrue(rules.should_cell_live(True, 2))
        # Live cell with 3 neighbors survives
        self.assertTrue(rules.should_cell_live(True, 3))
        # Live cell with 4 neighbors dies
        self.assertFalse(rules.should_cell_live(True, 4))

    def test_cell_birth(self):
        rules = GameRules()
        # Dead cell with exactly 3 neighbors becomes alive
        self.assertTrue(rules.should_cell_live(False, 3))
        # Dead cell with 2 neighbors stays dead
        self.assertFalse(rules.should_cell_live(False, 2))