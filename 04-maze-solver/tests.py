import unittest

from graphics import Window
from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )

    def test_maze_create_cells_different_size(self):
        num_cols = 5
        num_rows = 7
        m2 = Maze(0, 0, num_rows, num_cols, 15, 15)
        self.assertEqual(
            len(m2._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m2._Maze__cells[0]),
            num_rows,
        )

    def test_maze_larger_than_window(self):
        win = Window(100, 100)
        # Each cell is 60x60, 2x2 grid, so 120x120 > 100x100 window
        with self.assertRaises(AssertionError):
            Maze(0, 0, 2, 2, 60, 60, win)

    def test_maze_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            m1._Maze__cells[0][0].has_top_wall,
            False,
        )
        self.assertEqual(
            m1._Maze__cells[num_cols - 1][num_rows - 1].has_bottom_wall,
            False,
        )

    def test_reset_cells_visited(self):
        num_cols = 4
        num_rows = 3
        m = Maze(0, 0, num_rows, num_cols, 10, 10)
        # Manually set all cells to visited True
        for col in range(num_cols):
            for row in range(num_rows):
                m._Maze__cells[col][row].visited = True
        # Call the reset method
        m._reset_cells_visited()
        # Assert all cells are now False
        for col in range(num_cols):
            for row in range(num_rows):
                self.assertFalse(m._Maze__cells[col][row].visited)


if __name__ == "__main__":
    unittest.main()
