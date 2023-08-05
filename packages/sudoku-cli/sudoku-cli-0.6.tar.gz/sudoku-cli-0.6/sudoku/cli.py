# stdlib imports
import sys

# third-party imports
import click

# local imports
from .serialization import serialize, deserialize
from .solver import Solver
from .exceptions import InvalidProblemError


@click.command()
@click.argument('input_file', type=click.File())
@click.option(
    '--size',
    '-s',
    type=int,
    default=9,
    help='Size of the encoded sudoku problems. Defaults to 9.'
)
@click.option(
    '--ignore',
    '-i',
    is_flag=True,
    help='Silently ignores all errors. Writes blank lines for unworkable \
problems.'
)
def sudoku(input_file, size, ignore):
    """A command line tool for taking an input file encoding sudoku problems
    and writing their solutions to stdout.

    The input file consists of one sudoku problem per line, where each line is
    a string of integers in the range 0-9. A 0 denotes an empty location while
    all the other digits are filled cells. This string represents a walk
    through the grid from top to bottom and left to right.

    By default it exits with a message after encountering either an invalid
    problem or an unsolvable problem.
    """
    for i, line in enumerate(input_file):
        problem = deserialize(line.strip(), size)

        try:
            solution = Solver(problem).solve()
        except InvalidProblemError as e:
            if not ignore:
                sys.exit('Error: {} on line {}'.format(e, i + 1))
            solution = None

        if not ignore and not solution:
            sys.exit('Error: unsolvable problem on line {}'.format(i + 1))

        if i >= 1:
            sys.stdout.write('\n')

        sys.stdout.write(serialize(solution))
