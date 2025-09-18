import unittest
from game_of_life.domain.grid import Grid
from game_of_life.domain.position import Position



class TestGrid(unittest.TestCase):
    def test_neighbor_counting(self):
        # Create a small pattern
        alive_cells = {Position(1, 1), Position(1, 2), Position(2, 1)}
        grid = Grid(5, 5, alive_cells)

        # Position (1,1) should have 2 neighbors
        self.assertEqual(grid.count_alive_neighbors(Position(1, 1)), 2)
        # Position (2,2) should have 3 neighbors
        self.assertEqual(grid.count_alive_neighbors(Position(2, 2)), 3)