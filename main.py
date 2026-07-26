"""Tkinter interface for the linked-list stack pathfinding demo."""

import tkinter as tk
from tkinter import ttk

from game import InvalidCoordinateError, Map, OutOfBoundaries


class PathfindingApp(tk.Tk):
    """Interactive map editor and pathfinding visualizer."""

    ROWS = 8
    COLUMNS = 12
    CELL_SIZE = 48

    def __init__(self):
        super().__init__()
        self.title("LLStack Pathfinding")
        self.resizable(False, False)

        self.grid_data = self._default_grid()
        self.start_var = tk.StringVar(value="0, 0")
        self.end_var = tk.StringVar(value=f"{self.ROWS - 1}, {self.COLUMNS - 1}")
        self.status_var = tk.StringVar(
            value="Click cells to add or remove ocean. Then find a path."
        )
        self.cell_buttons = {}
        self.path_cells = set()

        self._build_controls()
        self._build_grid()
        self._redraw_grid()

    def _default_grid(self):
        """Create an open map with a few obstacles for the first run."""
        grid = [["grass" for _ in range(self.COLUMNS)] for _ in range(self.ROWS)]
        for row, column in ((1, 3), (2, 3), (3, 3), (4, 7), (5, 7), (6, 7)):
            grid[row][column] = "ocean"
        return grid

    def _build_controls(self):
        controls = ttk.Frame(self, padding=12)
        controls.grid(row=0, column=0, sticky="ew")

        ttk.Label(controls, text="Start (row, col)").grid(row=0, column=0, padx=(0, 6))
        ttk.Entry(controls, textvariable=self.start_var, width=9).grid(row=0, column=1)
        ttk.Label(controls, text="End (row, col)").grid(row=0, column=2, padx=(14, 6))
        ttk.Entry(controls, textvariable=self.end_var, width=9).grid(row=0, column=3)
        ttk.Button(controls, text="Set points", command=self._set_points).grid(
            row=0, column=4, padx=(14, 0)
        )

        ttk.Button(controls, text="Find path", command=self._find_path).grid(
            row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0)
        )
        ttk.Button(controls, text="Find shortest", command=self._find_shortest_path).grid(
            row=1, column=2, columnspan=2, sticky="ew", padx=(14, 0), pady=(10, 0)
        )
        ttk.Button(controls, text="Reset map", command=self._reset_map).grid(
            row=1, column=4, padx=(14, 0), pady=(10, 0)
        )

        ttk.Label(
            controls,
            textvariable=self.status_var,
            foreground="#555555",
        ).grid(row=2, column=0, columnspan=5, sticky="w", pady=(10, 0))

    def _build_grid(self):
        board = ttk.Frame(self, padding=(12, 0, 12, 12))
        board.grid(row=1, column=0)

        for row in range(self.ROWS):
            ttk.Label(board, text=str(row), width=2, anchor="center").grid(
                row=row + 1, column=0
            )
            for column in range(self.COLUMNS):
                button = tk.Button(
                    board,
                    width=3,
                    height=1,
                    font=("TkDefaultFont", 12, "bold"),
                    relief="flat",
                    command=lambda r=row, c=column: self._toggle_cell(r, c),
                )
                button.grid(row=row + 1, column=column + 1, padx=1, pady=1)
                self.cell_buttons[(row, column)] = button

        ttk.Label(board, text="").grid(row=0, column=0)
        for column in range(self.COLUMNS):
            ttk.Label(board, text=str(column), width=4, anchor="center").grid(
                row=0, column=column + 1
            )

    def _parse_coordinate(self, value, label):
        try:
            row_text, column_text = value.split(",")
            return int(row_text.strip()), int(column_text.strip())
        except (ValueError, AttributeError):
            raise ValueError(f"{label} must look like row, col") from None

    def _coordinates(self):
        return (
            self._parse_coordinate(self.start_var.get(), "Start"),
            self._parse_coordinate(self.end_var.get(), "End"),
        )

    def _make_map(self):
        start, end = self._coordinates()
        return Map([row[:] for row in self.grid_data], start, end)

    def _set_points(self):
        try:
            self._make_map()
        except (ValueError, TypeError, InvalidCoordinateError, OutOfBoundaries) as error:
            self.status_var.set(str(error))
            return
        self.path_cells.clear()
        self._redraw_grid()
        self.status_var.set("Start and end points updated.")

    def _toggle_cell(self, row, column):
        try:
            start, end = self._coordinates()
        except ValueError:
            start, end = None, None

        if (row, column) in (start, end):
            self.status_var.set("Choose a different cell before changing terrain.")
            return

        self.grid_data[row][column] = (
            "ocean" if self.grid_data[row][column] == "grass" else "grass"
        )
        self.path_cells.clear()
        self._redraw_grid()
        self.status_var.set("Map updated. Choose a pathfinding action.")

    def _show_path(self, shortest=False):
        try:
            game_map = self._make_map()
        except (ValueError, TypeError, InvalidCoordinateError, OutOfBoundaries) as error:
            self.status_var.set(str(error))
            return

        path = game_map.find_shortest_path() if shortest else game_map.find_path()
        if path is None:
            self.path_cells.clear()
            self._redraw_grid()
            self.status_var.set("No path exists between these points.")
            return

        coordinates = []
        while path.size:
            coordinates.append(path.pop())
        self.path_cells = set(coordinates)
        self._redraw_grid()
        path_type = "Shortest path" if shortest else "Path"
        self.status_var.set(f"{path_type} found: {len(coordinates)} cells.")

    def _find_path(self):
        self._show_path(shortest=False)

    def _find_shortest_path(self):
        self._show_path(shortest=True)

    def _reset_map(self):
        self.grid_data = self._default_grid()
        self.start_var.set("0, 0")
        self.end_var.set(f"{self.ROWS - 1}, {self.COLUMNS - 1}")
        self.path_cells.clear()
        self._redraw_grid()
        self.status_var.set("Map reset.")

    def _redraw_grid(self):
        try:
            start, end = self._coordinates()
        except ValueError:
            start, end = None, None

        for (row, column), button in self.cell_buttons.items():
            coordinate = (row, column)
            terrain = self.grid_data[row][column]
            text = ""
            background = "#d9f2d9" if terrain == "grass" else "#6fa8dc"
            foreground = "#173b17" if terrain == "grass" else "#ffffff"

            if coordinate in self.path_cells:
                background = "#f6d365"
            if coordinate == start:
                text = "S"
                background = "#58a55c"
            elif coordinate == end:
                text = "E"
                background = "#d95d5d"

            button.configure(text=text, bg=background, activebackground=background, fg=foreground)


if __name__ == "__main__":
    app = PathfindingApp()
    app.mainloop()
