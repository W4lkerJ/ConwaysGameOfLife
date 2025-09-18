import time
from typing import Optional, Tuple

from game_of_life.domain.grid import Grid
from game_of_life.domain.position import Position
from game_of_life.application.game_engine import GameEngine
from game_of_life.infrastructure.interfaces.pattern_loader import PatternLoader
from game_of_life.infrastructure.interfaces.renderer import Renderer


class GameOfLife:
    """Main application class orchestrating the simulation."""

    def __init__(
            self,
            width: int,
            height: int,
            pattern_loader: PatternLoader,
            renderer: Renderer,
            engine: GameEngine
    ):
        """
        Initialize the Game of Life simulation.

        Args:
            width: Grid width
            height: Grid height
            renderer: Renderer to use for display
            engine: Game engine to use for computation
        """
        self.width = width
        self.height = height
        self.pattern_loader = pattern_loader
        self.renderer = renderer
        self.engine = engine
        self.grid = Grid(width, height, set())
        self.generation = 0

    def load_pattern(self, offset: Tuple[int, int] = (0, 0)) -> None:
        """
        Load a starting pattern into the grid.

        Args:
            offset: Position offset for placing the pattern

        Raises:
            ValueError: If format is not supported
        """

        pattern_cells = self.pattern_loader.load()

        # Apply offset and validate positions
        alive_cells = set()
        for pos in pattern_cells:
            new_pos = Position(pos.row + offset[0], pos.col + offset[1])

            if self.grid.is_valid_position(new_pos):
                alive_cells.add(new_pos)
            else:
                raise ValueError(f"Loaded position {new_pos} is not a valid position")

        self.grid = Grid(self.width, self.height, alive_cells)
        self.generation = 0

    def step(self) -> None:
        """Advance the simulation by one generation."""
        self.grid = self.engine.compute_next_generation(self.grid)
        self.generation += 1

    def run(
            self,
            generations: Optional[int] = None,
            delay: float = 0.1,
            stop_on_stable: bool = True
    ) -> None:
        """Run the simulation.

        Args:
            generations: Number of generations to run (None for infinite)
            delay: Delay between generations in seconds
            stop_on_stable: Stop if pattern becomes stable
        """
        previous_states = []
        max_history = 5  # Check for oscillations up to period 5

        try:
            gen_count = 0
            while generations is None or gen_count < generations:
                self.renderer.render(self.grid, self.generation)

                if stop_on_stable:
                    # Check for stable or oscillating patterns
                    current_state = frozenset(self.grid.alive_cells)
                    if current_state in previous_states:
                        print(f"\nPattern stabilized at generation {self.generation}")
                        break

                    previous_states.append(current_state)
                    if len(previous_states) > max_history:
                        previous_states.pop(0)

                if not self.grid.alive_cells:
                    print(f"\nAll cells died at generation {self.generation}")
                    break

                time.sleep(delay)
                self.step()
                gen_count += 1

        except KeyboardInterrupt:
            print(f"\nSimulation stopped at generation {self.generation}")
