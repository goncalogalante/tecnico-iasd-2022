# Artificial Intelligence and Decision Systems, 2022
# IASD 2022/23 Project Assignment #1:
‘Roll the Ball’ Slide Puzzle
Luis Cust ́odio and Rodrigo Ventura
Instituto Superior T ́ecnico, University of Lisbon
(Version 1.0, September 19, 2022)

# Introduction

Free the Ball, or Roll the Ball, is a classic tile puzzle where the goal is to move the sliding
tiles to unblock a path for the ball to roll to the exit (Figure 1).
The puzzle is similar to the 8-puzzle in the sense that i) it is played in a squared grid of
N cells; ii) it has empty cells to where the movable tiles can be slid; iii) it starts in an initial
configuration. It is different from the 8-puzzle since i) it does not have a final configuration
but a goal to be achieved; ii) it may have more than one empty cell; iii) some tiles can be
movable (can slide) others cannot.
This year’s IASD project consists in developing a program using Python to solve ‘Roll
the Ball’ puzzles. The project will be divided in three parts/assignments, each one with a
deliverable. This first assignment aims at reading a puzzle from an input file and determining
if in the initial configuration the goal is achieved (i.e. the ball can roll to the exit).

#1 Problem Statement and Solution
The puzzle is represented by a grid of N by N cells where some (most of) the cells are
occupied by tiles and some (few) are empty. For instance, in Figure 2, there is a 4 by 4
puzzle, where the black squares represent empty cells (4 of them) and the rest of the cells
are occupied by different tiles.
Figure 2: An example of a ‘Free the Ball’ puzzle
All puzzles should have two special tiles: i) one that establishes where the ball starts,
and ii) another one that defines where the ball should exit. In Figure 2, the former is the
tile in the top-right corner and the latter is the left most tile in the 3rd line. Both of these
tiles are colored blue because they are not movable.
For the purpose of this project all puzzles are squared (defined by parameter N ) and
numbered from top to bottom (lines) and from left to right (columns). So the puzzle in
Figure 2 is numbered like presented in Figure 3. The cells are represented by the pair
(row, column). The top-left corner cell is always cell (0, 0) and the bottom-right cell is
always cell (N − 1, N − 1).
The solution for puzzle in Figure 2 is presented in Figure 4. It involves three moves: (i)
slide tile (2, 1) to empty cell (1, 1), (ii) slide tile (2, 2) to empty cell (2, 1), and (iii) slide tile
2
Figure 3: The numbering of a puzzle
(3, 2) to empty cell (2, 2).
Figure 4: The solution for the puzzle
