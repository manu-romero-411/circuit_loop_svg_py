#!/usr/bin/env python3
"""Random circuit-pattern SVG generator.

Every tile of the grid is described by a 4-bit mask in ``UDLR`` order
(up, down, left, right). A set bit means the tile has a wire leaving
through that side, so a tile is simply one of the 16 values ``0b0000``
to ``0b1111``.

Consistency is guaranteed by construction: instead of picking tiles and
checking their neighbours, the generator decides which *edges* between
adjacent cells exist. The right bit of a tile and the left bit of the
tile next to it always come from the same edge, so wires never end in
the middle of nowhere and never point outside the grid.
"""

import argparse
import random
import sys
from typing import List, Optional, Tuple

UP = 0b1000
DOWN = 0b0100
LEFT = 0b0010
RIGHT = 0b0001

# Each side with its unit vector (dx, dy); y grows downwards in SVG.
SIDES: Tuple[Tuple[int, Tuple[int, int]], ...] = (
    (UP, (0, -1)),
    (DOWN, (0, 1)),
    (LEFT, (-1, 0)),
    (RIGHT, (1, 0)),
)

STRAIGHT_TILES = (UP | DOWN, LEFT | RIGHT)

TILE_SIZE = 32
HALF = TILE_SIZE // 2
WIRE_WIDTH = 6
PAD_RADIUS = 8

# Filled outlines for tiles with 3 or 4 wires, drawn in a 32x32 tile.
JUNCTION_PATHS = {
    LEFT | RIGHT | DOWN: (
        "M 32,13 C 25.29599,13 19.38386,16.512054 16,21.787109 "
        "12.61605,16.51255 6.7036399,13 0,13 v 6 C 7.2152399,19 13,24.784764 "
        "13,32 h 6 c 0,-7.215236 5.78477,-13.000001 13,-13 z"
    ),
    LEFT | UP | DOWN: (
        "M 19,32 C 19,25.29599 15.48795,19.38386 10.21289,16 15.48745,12.61605 "
        "19,6.7036401 19,0 H 13 C 13,7.2152401 7.21524,13 0,13 v 6 c 7.21524,0 "
        "13,5.78477 13,13 z"
    ),
    RIGHT | UP | DOWN: (
        "M 13,32 C 13,25.29599 16.51205,19.38386 21.78711,16 16.51255,12.61605 "
        "13,6.7036401 13,0 h 6 C 19,7.2152401 24.78476,13 32,13 v 6 c "
        "-7.21524,0 -13,5.78477 -13,13 z"
    ),
    LEFT | RIGHT | UP: (
        "M 32,19 C 25.29599,19 19.38386,15.487945 16,10.212891 "
        "12.61605,15.487449 6.7036404,19 0,19 V 13 C 7.2152404,13 13,7.2152358 "
        "13,0 h 6 C 19,7.2152358 24.78477,13 32,13 Z"
    ),
    UP | DOWN | LEFT | RIGHT: (
        "M 13,0 C 13,7.2152361 7.2152402,13 0,13 v 6 c 7.2152402,0 13,5.784764 "
        "13,13 h 6 C 19,24.784764 24.78477,19 32,19 V 13 C 24.78477,13 "
        "19,7.2152361 19,0 Z m 3,10.212891 C 17.48785,12.53228 "
        "19.465385,14.51096 21.783203,16 19.465385,17.48904 17.48785,19.46772 "
        "16,21.787109 14.511334,19.466728 12.532315,17.489345 10.212891,16 "
        "12.532315,14.510655 14.511334,12.533272 16,10.212891 Z"
    ),
}

Grid = List[List[int]]
Point = Tuple[int, int]


def generate_grid(
    rows: int, cols: int, density: float, rng: random.Random
) -> Grid:
    """Build a rows x cols grid of UDLR masks.

    ``density`` is the probability (0..1) that two adjacent cells are
    connected by a wire.
    """
    horizontal = [
        [rng.random() < density for _ in range(cols - 1)] for _ in range(rows)
    ]
    vertical = [
        [rng.random() < density for _ in range(cols)] for _ in range(rows - 1)
    ]
    return [
        [tile_mask(row, col, horizontal, vertical) for col in range(cols)]
        for row in range(rows)
    ]


def tile_mask(
    row: int, col: int, horizontal: List[List[bool]], vertical: List[List[bool]]
) -> int:
    """Return the UDLR mask of one tile from the grid's edge tables.

    ``horizontal[r][c]`` links cell (r, c) with (r, c + 1) and
    ``vertical[r][c]`` links cell (r, c) with (r + 1, c).
    """
    mask = 0
    if row > 0 and vertical[row - 1][col]:
        mask |= UP
    if row < len(vertical) and vertical[row][col]:
        mask |= DOWN
    if col > 0 and horizontal[row][col - 1]:
        mask |= LEFT
    if col < len(horizontal[row]) and horizontal[row][col]:
        mask |= RIGHT
    return mask


def is_consistent(grid: Grid) -> bool:
    """Check that every wire has a matching wire on the neighbouring tile."""
    rows, cols = len(grid), len(grid[0])
    for row in range(rows):
        for col in range(cols):
            mask = grid[row][col]
            if bool(mask & UP) != (row > 0 and bool(grid[row - 1][col] & DOWN)):
                return False
            if bool(mask & LEFT) != (col > 0 and bool(grid[row][col - 1] & RIGHT)):
                return False
            if mask & DOWN and row == rows - 1:
                return False
            if mask & RIGHT and col == cols - 1:
                return False
    return True


def point(origin: Point, vector: Tuple[int, int], distance: int) -> Point:
    """Return the point ``distance`` away from the tile centre along vector."""
    return (
        origin[0] + HALF + vector[0] * distance,
        origin[1] + HALF + vector[1] * distance,
    )


def tile_elements(mask: int, origin: Point) -> Tuple[List[str], List[str]]:
    """Return ``(path_commands, shapes)`` needed to draw one tile.

    * 1 wire: a pad (ring) with a wire going to the tile edge.
    * 2 wires: a straight wire or a 90 degree circular arc.
    * 3 or 4 wires: a filled junction shape (see ``JUNCTION_PATHS``).
    """
    vectors = [vector for flag, vector in SIDES if mask & flag]
    center = point(origin, (0, 0), 0)
    commands: List[str] = []
    shapes: List[str] = []

    if len(vectors) == 1:
        start = point(origin, vectors[0], HALF)
        end = point(origin, vectors[0], PAD_RADIUS)
        commands.append(f"M{start[0]},{start[1]}L{end[0]},{end[1]}")
        shapes.append(
            f'<circle cx="{center[0]}" cy="{center[1]}" r="{PAD_RADIUS}"/>'
        )
    elif len(vectors) == 2:
        start = point(origin, vectors[0], HALF)
        end = point(origin, vectors[1], HALF)
        if mask in STRAIGHT_TILES:
            commands.append(f"M{start[0]},{start[1]}L{end[0]},{end[1]}")
        else:
            # Quarter circle of radius HALF centred on the shared tile corner.
            sweep = int(
                vectors[1][0] * vectors[0][1] - vectors[1][1] * vectors[0][0] > 0
            )
            commands.append(
                f"M{start[0]},{start[1]}"
                f"A{HALF},{HALF} 0 0 {sweep} {end[0]},{end[1]}"
            )
    elif len(vectors) > 2:
        shapes.append(f'<use href="#j{mask}" x="{origin[0]}" y="{origin[1]}"/>')
    return commands, shapes


def junction_defs(grid: Grid) -> List[str]:
    """Return ``<path>`` definitions for the junction shapes the grid uses."""
    used = sorted({mask for line in grid for mask in line} & set(JUNCTION_PATHS))
    return [
        f'<path id="j{mask}" fill="#000" stroke="none" '
        f'd="{JUNCTION_PATHS[mask]}"/>'
        for mask in used
    ]


def build_svg(grid: Grid) -> str:
    """Render the whole grid as a single compact SVG document."""
    rows, cols = len(grid), len(grid[0])
    width, height = cols * TILE_SIZE, rows * TILE_SIZE
    commands: List[str] = []
    shapes: List[str] = []

    for row, line in enumerate(grid):
        for col, mask in enumerate(line):
            tile_commands, tile_shapes = tile_elements(
                mask, (col * TILE_SIZE, row * TILE_SIZE)
            )
            commands.extend(tile_commands)
            shapes.extend(tile_shapes)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}">',
        "<defs>",
        *junction_defs(grid),
        "</defs>",
        f'<g fill="none" stroke="#000" stroke-width="{WIRE_WIDTH}">',
        f'<path d="{"".join(commands)}"/>',
        *shapes,
        "</g>",
        "</svg>",
    ]
    return "\n".join(lines) + "\n"


def positive_int(text: str) -> int:
    """Argparse type: integer greater than zero."""
    value = int(text)
    if value < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return value


def probability(text: str) -> float:
    """Argparse type: float between 0 and 1."""
    value = float(text)
    if not 0.0 <= value <= 1.0:
        raise argparse.ArgumentTypeError("must be between 0 and 1")
    return value


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a circuit-like pattern as an SVG file."
    )
    parser.add_argument(
        "-w", "--width", type=positive_int, default=16,
        help="number of tile columns (default: 16)",
    )
    parser.add_argument(
        "-t", "--height", type=positive_int, default=16,
        help="number of tile rows (default: 16)",
    )
    parser.add_argument(
        "-d", "--density", type=probability, default=0.55,
        help="probability of a wire between adjacent tiles (default: 0.55)",
    )
    parser.add_argument(
        "-s", "--seed", type=int, default=None,
        help="random seed (default: random, always printed)",
    )
    parser.add_argument("filename", help="output SVG file")
    return parser.parse_args(argv)


def main() -> int:
    """Entry point."""
    args = parse_args()
    seed = args.seed if args.seed is not None else random.randrange(10**9)
    print(f"Seed: {seed}")
    rng = random.Random(seed)
    grid = generate_grid(args.height, args.width, args.density, rng)
    with open(args.filename, "w", encoding="utf-8") as svg_file:
        svg_file.write(build_svg(grid))
    return 0


if __name__ == "__main__":
    sys.exit(main())
