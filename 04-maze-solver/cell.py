from graphics import Line, Point, Window


class MazeCell:
    """A box in the grid that builds the maze.

    Attributes:
        has_left_wall: Whether the cell has a left wall.
        has_right_wall: Whether the cell has a right wall.
        has_top_wall: Whether the cell has a top wall.
        has_bottom_wall: Whether the cell has a bottom wall.
    """

    def __init__(self, window: Window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = None
        self.__y1 = None
        self.__x2 = None
        self.__y2 = None
        self.__window = window

    def draw(self, x1: int, y1: int, x2: int, y2: int):
        """Draw the cell on the window.

        Args:
            x1: The x-coordinate of the left edge of the cell.
            y1: The y-coordinate of the top edge of the cell.
            x2: The x-coordinate of the right edge of the cell.
            y2: The y-coordinate of the bottom edge of the cell.
        """
        assert x1 < x2 and y1 < y2, (
            "x1 must be less than x2 and y1 must be less than y2"
        )

        width, height = self.__window.get_dimensions()
        assert x1 >= 0 and y1 >= 0, "x1 and y1 must be greater than or equal to 0"
        assert x2 <= width and y2 <= height, (
            "x2 and y2 must be less than or equal to the window width and height"
        )

        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self.__window.draw_line(line)
        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self.__window.draw_line(line)
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self.__window.draw_line(line)
        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self.__window.draw_line(line)

    def draw_move(self, to_cell: "MazeCell", undo: bool = False):
        """Draw a move from this cell to another cell.

        Args:
            to_cell: The cell to move to.
            undo: Whether to undo the move. Denoted by "gray" color line, else "red".
        """
        line = Line(Point(*self.get_center()), Point(*to_cell.get_center()))
        self.__window.draw_line(line, "gray" if undo else "red", 1)

    def get_center(self) -> tuple[int, int]:
        """Get the center of the cell.

        Returns:
            The center of the cell.
        """
        return ((self.__x1 + self.__x2) / 2, (self.__y1 + self.__y2) / 2)
