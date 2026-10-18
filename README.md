# Circuit Loop SVG Python

A simple circuit-pattern SVG generator written in Python.

Usage: `python3 circuit.py [-w WIDTH] [-t HEIGHT] [-d DENSITY] [-s SEED] filename`

- `-w`, `--width`: number of tile columns (default: 16)
- `-t`, `--height`: number of tile rows (default: 16)
- `-d`, `--density`: probability of a wire between adjacent tiles, 0 to 1 (default: 0.55)
- `-s`, `--seed`: random seed for reproducible output (if omitted, a random one is used; it is always printed as `Seed: N`)

## How it works

Each tile is a 4-bit `UDLR` mask (up, down, left, right). The generator
picks which edges between neighbouring cells exist and derives every
tile from them, so all wires are always connected and none points
outside the grid.

Tiles are drawn as: nothing (0 wires), a pad (1 wire), a straight wire or
rounded corner (2 wires) and a filled junction shape (3 or 4 wires). The whole
circuit is a single `<path>` plus a few `<circle>` and `<use>` elements.
