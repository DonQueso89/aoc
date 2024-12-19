#!/usr/bin/env python

import argparse
from io import TextIOWrapper
from pathlib import Path
from utils import grids

parser = argparse.ArgumentParser(description='day X')

parser.add_argument('input', type=str, help='input file')

dir_ = Path(__file__).parent

def print_grid(boxes, walls, pos, xlim, ylim, griddef=None):
    grid = {}
    for x in range(xlim):
        for y in range(ylim):
            if (x, y) in walls:
                grid[(x, y)] = "#"
            elif (x, y) in boxes:
                if griddef:
                    grid[(x, y)] = griddef[(x, y)]
                else:
                    grid[(x, y)] = "O"
            elif (x, y) == pos:
                grid[(x, y)] = "@"
            else:
                grid[(x, y)] = " "
    grids.print_grid(grid, xlim, ylim, marked_chars=("@", "O"))

def main(infp: TextIOWrapper, args: argparse.Namespace):
    inp = (_ for _ in infp.read().splitlines())

    line = next(inp)
    y = 0
    pos = None
    boxes  = set()
    walls = set()
    grid2 = ""
    while line:
        for x, c in enumerate(line):
            if c == "@":
                pos = (x, y)
                grid2 += "@."
            elif c == "#":
                walls.add((x, y))
                grid2 += "##"
            elif c == "O":
                boxes.add((x, y))
                grid2 += "[]"
            else:
                grid2 += ".."
        line = next(inp)
        grid2 += "\n"
        y += 1
    ylim = y
    xlim = x + 1

    moves = ""
    for line in inp:
        if line:
            moves += line

    x, y = pos
    for move in moves:
        dx, dy = grids.caret_mapping[move]
        nx, ny = x + dx, y + dy
        if (nx, ny) in walls:
            continue
        if (nx, ny) in boxes:
            contiguous_boxes = []
            while (nx, ny) in boxes:
                contiguous_boxes.append((nx, ny))
                nx, ny = nx + dx, ny + dy
            if (nx, ny) in walls:
                continue
            boxes.remove(contiguous_boxes[0])
            boxes.add((nx, ny))
        x, y = x + dx, y + dy
    
    print(sum([x + y * 100 for x, y in boxes]))

    boxes  = set()
    walls = set()
    grid = {}
    for y, line in enumerate(grid2.splitlines()):
        for x, c in enumerate(line):
            if c == "@":
                pos = (x, y)
            elif c in "[]":
                boxes.add((x, y))
            elif c == "#":
                walls.add((x, y))
            grid[(x, y)] = c
    ylim = y + 1
    xlim = x + 1
    x, y = pos
    for move in moves:
        dx, dy = grids.caret_mapping[move]
        nx, ny = x + dx, y + dy
        if (nx, ny) in walls:
            continue
        if (nx, ny) in boxes:
            if move in "<>":
                contiguous_boxes = []
                while (nx, ny) in boxes:
                    contiguous_boxes.append((nx, ny))
                    nx, ny = nx + dx, ny + dy
                if (nx, ny) in walls:
                    continue
                boxes.remove(contiguous_boxes[0])
                boxes.add((nx, ny))
                replacements = []
                for bx, by in contiguous_boxes:
                    replacements.append((bx, by, grid.pop((bx, by))))
                grid[contiguous_boxes[0]] = "."
                for bx, by, c in replacements:
                    grid[(bx + dx, by + dy)] = c
            else:
                box_tree = set()
                box_tree.add((nx, ny))
                if grid[(nx, ny)] == "]":
                    sdx, sdy = grids.caret_mapping["<"]
                    box_tree.add((nx + sdx, ny + sdy))
                elif grid[(nx, ny)] == "[":
                    sdx, sdy = grids.caret_mapping[">"]
                    box_tree.add((nx + sdx, ny + sdy))
                else:
                    raise ValueError(f"{(x, y)} in boxes but not box in grid")

                prev_surface = box_tree.copy()
                move_boxes = True
                while prev_surface:
                    surface = prev_surface
                    box_tree |= surface
                    prev_surface = set()
                    for bx, by in surface:
                        nxt = (bx + dx, by + dy)
                        if nxt in walls:
                            move_boxes = False
                            break
                        if nxt in boxes:
                            prev_surface.add(nxt)
                            _nx, _ny = nxt
                            if grid[nxt] ==  "]":
                                sdx, sdy = grids.caret_mapping["<"]
                                prev_surface.add((_nx + sdx, _ny + sdy))
                            elif grid[nxt] ==  "[":
                                sdx, sdy = grids.caret_mapping[">"]
                                prev_surface.add((_nx + sdx, _ny + sdy))
                            else:
                                raise ValueError(f"{(x, y)} in boxes but not box in grid")
                    if not move_boxes:
                        break
                if move_boxes:
                    boxes -= box_tree
                    replacements =[]
                    for (bx, by) in box_tree:
                        boxes.add((bx + dx, by + dy))
                        replacements.append((bx, by, grid.pop((bx, by))))
                    for bx, by, _ in replacements:
                        grid[(bx, by)] = "."
                    for bx, by, c in replacements:
                        grid[(bx + dx, by + dy)] = c
                if not move_boxes:
                    continue
        x, y = x + dx, y + dy
    print(sum([x + y * 100 for x, y in boxes if grid[(x, y)] == "["]))

if __name__ == '__main__':
    args = parser.parse_args()
    infp = open(dir_ / args.input.split("/")[-1], 'r')
    main(infp, args)
