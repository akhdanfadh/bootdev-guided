from tkinter import BOTH, Canvas, Tk


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
