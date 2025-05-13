from tkinter import BOTH, Canvas, Tk


class Point:
    """A point in 2D space.

    Attributes:
        x: The x-coordinate of the point in pixels. 0 is the left edge of the window.
        y: The y-coordinate of the point in pixels. 0 is the top edge of the window.
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Line:
    """A line in 2D space.

    Attributes:
        p1: The first point of the line.
        p2: The second point of the line.
    """

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas: Canvas, fill_color: str = "black", width: int = 2):
        """Draw the line on the canvas."""
        canvas.create_line(
            (self.p1.x, self.p1.y),
            (self.p2.x, self.p2.y),
            fill=fill_color,
            width=width,
        )


class Window:
    def __init__(self, width: int, height: int):
        self.__running = False
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)

    def redraw(self):
        """Redraw all the graphics in the window."""
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        """Main loop for the window."""
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def close(self):
        self.__running = False

    def draw_line(self, line: Line, fill_color: str = "black", width: int = 2):
        """Draw a line on the canvas."""
        line.draw(self.__canvas, fill_color, width)
