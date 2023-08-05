def serialize(grid):
    """Serializes sudoku grids into a string.

    Args:
        grid (list of lists of ints): This list characterizes a sudoku
            grid. The ints are in 0-9, where 0 denotes an empty cell and any
            other number is a filled cell.

    Returns:
        str: This string represents a walk through the grid from top to bottom
            and left to right.
    """
    string = ''
    for row in grid:
        for cell in row:
            string += str(cell)

    return string


def deserialize(string, size):
    """Deserializes sudoku grid strings into lists.

    Args:
        string (str): This string represents a sudoku grid in the standard
        format.

        size (int): A number specifying the size of the sudoku grid
        encoded in `string`.

    Returns:
        list: The list representing the grid from `string`.
    """
    grid = []
    for i in range(0, len(string), size):
        cell_characters = list(string[i:i + size])
        row = [int(character) for character in cell_characters]
        grid.append(row)

    return grid
