from graphics import Line, Point, Window


def main():
    win = Window(800, 600)
    line = Line(Point(50, 100), Point(100, 50))
    win.draw_line(line)
    win.wait_for_close()


if __name__ == "__main__":
    main()
