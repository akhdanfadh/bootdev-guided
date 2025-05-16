import random
import time

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
        self.visited = False
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
        if self.__window is None:
            return

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

        line = Line(Point(x1, y1), Point(x1, y2))
        self.__window.draw_line(line, "black" if self.has_left_wall else "white")

        line = Line(Point(x2, y1), Point(x2, y2))
        self.__window.draw_line(line, "black" if self.has_right_wall else "white")

        line = Line(Point(x1, y1), Point(x2, y1))
        self.__window.draw_line(line, "black" if self.has_top_wall else "white")

        line = Line(Point(x1, y2), Point(x2, y2))
        self.__window.draw_line(line, "black" if self.has_bottom_wall else "white")

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


class Maze:
    """A maze that is a grid of cells."""

    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        window: Window = None,
        seed: int = None,
        animation_speed: float = 0.05,
    ):
        """Initialize the maze.

        Args:
            x1: The x-coordinate of the left edge of the maze.
            y1: The y-coordinate of the top edge of the maze.
            num_rows: The number of rows in the maze.
            num_cols: The number of columns in the maze.
            cell_size_x: The width of each cell.
            cell_size_y: The height of each cell.
            window: The window to draw the maze in.
        """
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__window = window
        self.__animation_speed = animation_speed
        if seed:
            random.seed(seed)

        self.__cells: list[list[MazeCell]] = None
        self._create_cells()

    def _create_cells(self):
        """Create the cells in the maze and draw them on the window.

        The cells are stored in a 2D list (column-major order), so the first index is the column and the second index is the row. This design is to replicate (x,y) coordinates.
        """
        # Populate the matrix
        self.__cells = [
            [MazeCell(self.__window) for _ in range(self.__num_rows)]
            for _ in range(self.__num_cols)
        ]

        # Calculate the position and animate
        for col in range(self.__num_cols):
            for row in range(self.__num_rows):
                self._draw_cell(col, row)

        # Making entrance and exit
        self._break_entrance_and_exit()

        # Break walls
        self._break_walls_recursive(0, 0)

        # Reset visited cells
        self._reset_cells_visited()

    def _draw_cell(self, col: int, row: int):
        """Calculate the x/y position of a cell.

        Args:
            col: Horizontal index (x) of the cell in the grid
            row: Vertical index (y) of the cell in the grid
        """
        if self.__window is None:
            return

        x1 = self.__x1 + col * self.__cell_size_x
        y1 = self.__y1 + row * self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y

        self.__cells[col][row].draw(x1, y1, x2, y2)
        self._animate()

    def _reset_cells_visited(self):
        """Reset the visited attribute for all cells."""
        for row in self.__cells:
            for cell in row:
                cell.visited = False

    def _break_entrance_and_exit(self):
        """Break the walls for maze entrance and exit.

        The entrance is always at the top of the top-left cell, while
        the exit is always at the bottom of the bottom-right cell.
        """
        self.__cells[0][0].has_top_wall = False  # entrance
        self._draw_cell(0, 0)  # redraw the canvas

        exit_col, exit_row = self.__num_cols - 1, self.__num_rows - 1
        self.__cells[exit_col][exit_row].has_bottom_wall = False  # exit
        self._draw_cell(exit_col, exit_row)

    def _break_walls_recursive(self, col: int, row: int):
        """A depth-first traversal through the cells to break down walls."""
        current_cell = self.__cells[col][row]
        current_cell.visited = True

        while True:
            # Get unvisited neighbors
            neighbors = self._get_adjacent_cells(col, row)
            unvisited = [
                (direction, cell) for direction, cell in neighbors if not cell.visited
            ]

            # If no unvisited neighbors, update drawing of current cell and break loop
            if not unvisited:
                self._draw_cell(col, row)
                return

            # Choose random unvisited neighbor and break walls in between
            direction: str
            next_cell: MazeCell
            direction, next_cell = random.choice(unvisited)
            if direction == "top":
                next_cell.has_bottom_wall = False
                current_cell.has_top_wall = False
                self._break_walls_recursive(col, row - 1)
            elif direction == "left":
                next_cell.has_right_wall = False
                current_cell.has_left_wall = False
                self._break_walls_recursive(col - 1, row)
            elif direction == "right":
                next_cell.has_left_wall = False
                current_cell.has_right_wall = False
                self._break_walls_recursive(col + 1, row)
            elif direction == "bottom":
                next_cell.has_top_wall = False
                current_cell.has_bottom_wall = False
                self._break_walls_recursive(col, row + 1)

    def _get_adjacent_cells(self, col: int, row: int) -> list[tuple[str, MazeCell]]:
        """Get all adjacent cells for a current cell."""
        neighbors = []
        if row > 0:  # top
            neighbors.append(("top", self.__cells[col][row - 1]))
        if col > 0:  # left
            neighbors.append(("left", self.__cells[col - 1][row]))
        if row < self.__num_rows - 1:  # bottom
            neighbors.append(("bottom", self.__cells[col][row + 1]))
        if col < self.__num_cols - 1:  # right
            neighbors.append(("right", self.__cells[col + 1][row]))
        return neighbors

    def _animate(self):
        """Visualize what the algorithms are doing in real time."""
        if self.__window is None:
            return

        self.__window.redraw()
        time.sleep(self.__animation_speed)
