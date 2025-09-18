# Conway's Game of Life

## Features
- **Architecture**: Separated into Domain, Application, and Infrastructure layers and following SOLID Principles where they make sense (Open-Closed, Single-Responsibility)
- **Optimized Performance**: Only checks cells that could change (alive cells and their neighbors)
- **Multiple Input Formats**: Plain text and JSON
- **Configurable Grid Size**: Supports any grid dimensions
- **Pattern Detection**: Automatically detects stable and oscillating patterns
- **Extensible Design**: Easy to add new pattern formats, renderers and custom rules
- **Tested Code**: Contains unittests for all parts of the simulation

## Installation
No external dependencies required! Uses only Python standard library.

```bash
# Clone or download the game_of_life.py file
python -m game_of_life.game
```

## Quick Start
```python
from game_of_life.application.game_engine import GameEngine
from game_of_life.infrastructure.implementations.console_renderer import ConsoleRenderer
from game_of_life.infrastructure.implementations.pattern_loader.plain_text_pattern_loader import PlainTextPatternLoader
from game_of_life.presentation.game_of_life import GameOfLife
from game_of_life.patterns import Patterns


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

```

## Pattern Formats
### Plain Text Format (.txt)

The simplest format for human readability. Use:
- `*` or `1` for alive cells
- `.` or `0` for dead cells

**Example with glider**


```
.*. 
..*
***
```

**Loading:**
```python
from game_of_life.infrastructure.implementations.pattern_loader.plain_text_pattern_loader import PlainTextPatternLoader

pattern = """
    .*. 
    ..*
    ***
    """

pattern_loader = PlainTextPatternLoader(pattern)
pattern_loader.load()
```

### JSON Format (.json)
Machine-readable format, good for programmatic generation.

**Example file: `pattern.json`**
```json
{
  "alive_cells": [
    [0, 1],
    [1, 2],
    [2, 0],
    [2, 1],
    [2, 2]
  ]
}
```

**Loading:**
```python

from game_of_life.infrastructure.implementations.pattern_loader.json_pattern_loader import JSONPatternLoader

pattern = """
     {
      "alive_cells": [
        [0, 1],
        [1, 2],
        [2, 0],
        [2, 1],
        [2, 2]
      ]
    }
    """

pattern_loader = JSONPatternLoader(pattern)
pattern_loader.load()

```


## Configuration Options
### Grid Size
```python
# Create a large grid for complex patterns
game = GameOfLife(width=100, height=80)
```

### Pattern Placement

Use the `offset` parameter to place patterns at specific locations:

```python
# Place pattern at row 10, column 15
game.load_pattern(offset=(10, 15))
```

### Simulation Parameters
```python
game.run(
    generations=500,      # Number of generations (None for infinite)
    delay=0.05,          # Delay between generations in seconds
    stop_on_stable=True  # Stop when pattern stabilizes
)
```

## Predefined Patterns
The library includes several classic patterns:

```python
from game_of_life.game import GameOfLife
from game_of_life.patterns import Patterns

from game_of_life.infrastructure.implementations.console_renderer import ConsoleRenderer
from game_of_life.application.game_engine import GameEngine
from game_of_life.infrastructure.implementations.pattern_loader.plain_text_pattern_loader import PlainTextPatternLoader


pattern_loader = PlainTextPatternLoader(Patterns.BLINKER)
pattern_loader = PlainTextPatternLoader(Patterns.TOAD)
pattern_loader = PlainTextPatternLoader(Patterns.BEACON)
pattern_loader = PlainTextPatternLoader(Patterns.PULSAR)

game = GameOfLife(
    width=60,
    height=40,
    pattern_loader=pattern_loader,
    renderer=ConsoleRenderer(),
    engine=GameEngine()
)

```

## Creating Custom Patterns
### Method 1: Plain Text String

```python
from game_of_life.game import GameOfLife
from game_of_life.patterns import Patterns

from game_of_life.infrastructure.implementations.console_renderer import ConsoleRenderer
from game_of_life.application.game_engine import GameEngine
from game_of_life.infrastructure.implementations.pattern_loader.plain_text_pattern_loader import PlainTextPatternLoader


my_pattern = """
..***
.*...
*....
*....
*....
"""

pattern_loader = PlainTextPatternLoader(my_pattern)

game = GameOfLife(
    width=60,
    height=40,
    pattern_loader=pattern_loader,
    renderer=ConsoleRenderer(),
    engine=GameEngine()
)

game.load_pattern()
```

### Method 2: JSON String

```python
from game_of_life.game import GameOfLife
from game_of_life.patterns import Patterns

from game_of_life.infrastructure.implementations.console_renderer import ConsoleRenderer
from game_of_life.application.game_engine import GameEngine
from game_of_life.infrastructure.implementations.pattern_loader.plain_text_pattern_loader import PlainTextPatternLoader


my_pattern = """
{
    "alive_cells": [
        [5, 5], [5, 6], [5, 7],
        [6, 5], [7, 6]
    ]
}
"""

pattern_loader = PlainTextPatternLoader(my_pattern)

game = GameOfLife(
    width=60,
    height=40,
    pattern_loader=pattern_loader,
    renderer=ConsoleRenderer(),
    engine=GameEngine()
)

game.load_pattern()
```

## Advanced Usage
### Custom Rules
Implement different cellular automata:

```python
class HighLifeRules(GameRules):
    @staticmethod
    def should_cell_live(is_alive: bool, neighbor_count: int) -> bool:
        if is_alive:
            return neighbor_count in [2, 3]
        else:
            return neighbor_count in [3, 6]  # Birth on 3 or 6

# Use custom rules
engine = GameEngine(rules=HighLifeRules())
game = GameOfLife(engine=engine)
```

### Custom Renderer
Create alternative display methods:

```python
class FileRenderer(Renderer):
    def __init__(self, filename):
        self.filename = filename
    
    def render(self, grid: Grid, generation: int):
        with open(f"{self.filename}_{generation:04d}.txt", 'w') as f:
            for row in range(grid.height):
                for col in range(grid.width):
                    if Position(row, col) in grid.alive_cells:
                        f.write('*')
                    else:
                        f.write('.')
                f.write('\n')

# Save each generation to file
game = GameOfLife(renderer=FileRenderer('output'))
```