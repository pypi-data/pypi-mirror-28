==========
sudoku-cli
==========

A CLI tool for solving sudoku puzzles.

Installation
============

::

  pip install sudoku-cli

Commands
========

The help page for the ``sudoku`` command is a good overview:

::

  Usage: sudoku [OPTIONS] INPUT_FILE

    A command line tool for taking an input file encoding sudoku problems and
    writing their solutions to stdout.

    The input file consists of one sudoku problem per line, where each line is
    a string of integers in the range 0-9. A 0 denotes an empty location while
    all the other digits are filled cells. This string represents a walk
    through the grid from top to bottom and left to right.

    By default it exits with a message after encountering either an invalid
    problem or an unsolvable problem.

  Options:
    -s, --size INTEGER  Size of the encoded sudoku problems. Defaults to 9.
    -i, --ignore        Silently ignores all errors. Writes blank lines for
                        unworkable problems.
    --help              Show this message and exit.


input_file
----------

The input file format is described above in the help page.

So this board:

::

  |0 9 0| |0,0,0| |0,0,6|
  |0 0 0| |9,6,0| |4,8,5|
  |0 0 0| |5,8,1| |0,0,0|

  |0,0,4| |0,0,0| |0,0,0|
  |5,1,7| |2,0,0| |9,0,0|
  |6,0,2| |0,0,0| |3,7,0|
  
  |1,0,0| |8,0,4| |0,2,0|
  |7,0,6| |0,0,0| |8,1,0|
  |3,0,0| |0,9,0| |0,0,0|

Would be encoded by this string:

::

  090000006000960485000581000004000000517200900602000370100804020706000810300090000

Development
===========

A Makefile is included to simplify the running of some common commands. 

To install the requirements for local development:

::

  make requirements

To run the tests along with a coverage report and linting:

::

  make test

To install the package locally for testing:

::

  make install

To run the benchmarks:

::

  make benchmark