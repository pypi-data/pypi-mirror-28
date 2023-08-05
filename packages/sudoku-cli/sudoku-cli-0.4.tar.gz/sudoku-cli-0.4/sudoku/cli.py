# stdlib imports
import sys

# third-party imports
import click

# local imports
from .io import from_file, to_file, to_stdout
from .solver import Solver


@click.command()
@click.option(
    '--input_file',
    '-i',
    required=True,
    type=str,
    help='File containing encoded sudoku problems.'
)
@click.option(
    '--output_file',
    '-o',
    type=str,
    help='File to write solutions to.'
)
@click.option(
    '--size',
    '-s',
    type=int,
    default=9,
    help='Size of the encoded sudoku problems. Defaults to 9.'
)
def sudoku(input_file, output_file, size):
    """A command line tool for taking a file encoding sudoku problems and
    writing their solutions to either stdout (by default) or an output file.
    """
    problems = from_file(input_file, size)
    if output_file:
        solutions = []

    for problem in problems:
        solution = Solver(problem).solve()
        if output_file:
            sys.stdout.write('.')
            sys.stdout.flush()
            solutions.append(solution)
        else:
            to_stdout(solution)

    if output_file:
        print()
        to_file(solutions, output_file)
