# stdlib imports
import sys

# local imports
from .serialization import serialize, deserialize


def from_file(filename, problem_size=9):
    """Creates sudoku problems from a file.

    Args:
        filename (str): A file that contains one problem per line. All problems
            must be the same size. The line consists of ints in 0-9, where 0
            denotes an empty cell and any other number is a filled cell. The
            cells in the string are ordered top to bottom and left to right.

        problem_size (int): A number specifying the size of the sudoku grids in
            the given file.

    Returns:
        list: A list of the sudoku problems defined in the file.
    """
    with open(filename, 'r') as file:
        return [deserialize(line.strip(), problem_size) for line in file]


def to_file(solutions, output_filename):
    """Writes sudoku solutions to a file.

    Args:
        solutions (list of solutions): The list of solutions to be written in
            the standard form.

        output_filename (str): The file that will be overwritten with the
            solutions in the standard format specified above.
    """
    with open(output_filename, 'w') as file:
        for i in range(len(solutions)):
            file.write(serialize(solutions[i]))
            if i < len(solutions) - 1:
                file.write('\n')


def to_stdout(solution):
    """Writes a sudoku solution to stdout.

    Args:
        solution (list): A solution written in the standard form.
    """
    sys.stdout.write(serialize(solution) + '\n')
