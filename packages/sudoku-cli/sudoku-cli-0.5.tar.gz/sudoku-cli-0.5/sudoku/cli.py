# stdlib imports
import sys

# third-party imports
import click

# local imports
from .io import from_file, to_file, to_stdout
from .solver import Solver
from .exceptions import InvalidProblemError


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option(
    '--output_file',
    '-o',
    type=click.Path(),
    help='File to write solutions to.'
)
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
def sudoku(input_file, output_file, size, ignore):
    """A command line tool for taking an input file encoding sudoku problems and
    writing their solutions to either stdout (by default) or an output file.

    The input file consists of one sudoku problem per line, where each line is
    a string of integers in the range 0-9. A 0 denotes an empty location while
    all the other digits are filled cells. This string represents a walk
    through the grid from top to bottom and left to right.

    By default it exits with a message after encountering either an invalid
    problem or an unsolvable problem.
    """
    problems = from_file(input_file, size)
    if output_file:
        solutions = []

    for i, problem in enumerate(problems):
        try:
            solution = Solver(problem).solve()
        except InvalidProblemError as e:
            if not ignore:
                sys.exit('Error: {} on line {}'.format(e, i + 1))

        if not ignore and not solution:
            sys.exit('Error: unsolvable problem on line {}'.format(i + 1))

        if output_file:
            sys.stdout.write('.')
            sys.stdout.flush()
            solutions.append(solution)
        else:
            to_stdout(solution)

    if output_file:
        print()
        to_file(solutions, output_file)
