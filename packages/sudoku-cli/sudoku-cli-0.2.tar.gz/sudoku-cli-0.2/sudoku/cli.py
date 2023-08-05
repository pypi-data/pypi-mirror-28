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
def sudoku(input_file, output_file):
    """A command line tool for taking a file encoding sudoku problems and
    writing their solutions to either stdout (by default) or an output file.
    """
    problems = from_file(input_file)
    if output_file:
        solutions = []

    for problem in problems:
        solution = Solver(problem).solve(validate=True)
        if output_file:
            solutions.append(solution)
        else:
            to_stdout(solution)

    if output_file:
        to_file(solutions, output_file)
