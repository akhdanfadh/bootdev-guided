from cell import MazeCell
from graphics import Window


def main():
    win = Window(800, 600)

    cell = MazeCell(win)
    cell.has_top_wall = False
    cell.has_right_wall = False
    cell.draw(50, 100, 100, 150)

    cell2 = MazeCell(win)
    cell2.has_left_wall = False
    cell2.has_right_wall = False
    cell2.draw(100, 100, 200, 150)

    cell.draw_move(cell2, True)

    cell = MazeCell(win)
    cell.has_left_wall = False
    cell.has_bottom_wall = False
    cell.draw(200, 100, 250, 150)

    cell2.draw_move(cell, False)

    win.wait_for_close()


if __name__ == "__main__":
    main()
