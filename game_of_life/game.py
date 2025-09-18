from game_of_life.application.game_engine import GameEngine
from game_of_life.infrastructure.implementations.console_renderer import ConsoleRenderer
from game_of_life.infrastructure.implementations.pattern_loader.plain_text_pattern_loader import PlainTextPatternLoader
from game_of_life.patterns import Patterns
from game_of_life.presentation.game_of_life import GameOfLife



def demo():
    """Run a demonstration of the Game of Life."""
    # Create a game instance
    game = GameOfLife(
        width=40,
        height=20,
        pattern_loader=PlainTextPatternLoader(Patterns.PULSAR),
        renderer=ConsoleRenderer(),
        engine=GameEngine()
    )

    # Load a glider pattern
    game.load_pattern(offset=(5, 5))

    # Run for 50 generations
    game.run(generations=50, delay=1)


if __name__ == "__main__":
    demo()
