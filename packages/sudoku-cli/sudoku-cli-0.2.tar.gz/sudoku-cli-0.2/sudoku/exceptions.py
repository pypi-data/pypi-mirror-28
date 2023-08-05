class InvalidProblemError(Exception):
    """An exception raised when:

    1) The problem is not a square grid
    2) The problem size is not a square number
    3) The problem has a row that is not a list
    """
    pass
