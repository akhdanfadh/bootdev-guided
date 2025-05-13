from cell import MazeCell
from graphics import Window


def main():
    win = Window(800, 600)

    cell = MazeCell(win)
    cell.has_top_wall = False
    cell.has_right_wall = False
    cell.draw(50, 100, 100, 150)

    cell = MazeCell(win)
    cell.has_left_wall = False
    cell.has_right_wall = False
    cell.draw(100, 100, 200, 150)

    cell = MazeCell(win)
    cell.has_left_wall = False
    cell.has_bottom_wall = False
    cell.draw(200, 100, 250, 150)

    win.wait_for_close()


if __name__ == "__main__":
    main()
