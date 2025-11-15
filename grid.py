"""
Enhanced Grid with Better Visual Graphics
Improved cell rendering, gradients, and polish
"""

import pygame
from constants import *


class Grid:
    """Enhanced grid with polished graphics"""

    def __init__(self, rows=GRID_ROWS, cols=GRID_COLS):
        self.rows = rows
        self.cols = cols
        self.cell_size = CELL_SIZE
        self.offset_x = GRID_OFFSET_X
        self.offset_y = GRID_OFFSET_Y

        self.grid = [[CELL_EMPTY for _ in range(cols)] for _ in range(rows)]

        self.nobita_pos = None
        self.school_pos = None
        self.gian_pos = None
        self.gadget_positions = []
        self.door_positions = []

        self.path = []
        self.explored = set()
        self.current_path_index = 0

    def in_bounds(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_walkable(self, row, col):
        if not self.in_bounds(row, col):
            return False
        cell = self.grid[row][col]
        return cell not in [CELL_WALL, CELL_GIAN]

    def get_cell(self, row, col):
        if not self.in_bounds(row, col):
            return None
        return self.grid[row][col]

    def set_cell(self, row, col, cell_type):
        if self.in_bounds(row, col):
            self.grid[row][col] = cell_type

            if cell_type == CELL_NOBITA:
                self.nobita_pos = (row, col)
            elif cell_type == CELL_SCHOOL:
                self.school_pos = (row, col)
            elif cell_type == CELL_GIAN:
                self.gian_pos = (row, col)
            elif cell_type == CELL_BAMBOO:
                if (row, col) not in self.gadget_positions:
                    self.gadget_positions.append((row, col))
            elif cell_type == CELL_DOOR:
                if (row, col) not in self.door_positions:
                    self.door_positions.append((row, col))

    def get_neighbors(self, row, col, include_diagonal=False):
        neighbors = []
        directions = [
            (-1, 0, BASE_COST),
            (1, 0, BASE_COST),
            (0, -1, BASE_COST),
            (0, 1, BASE_COST)
        ]

        if include_diagonal:
            directions.extend([
                (-1, -1, DIAGONAL_COST),
                (-1, 1, DIAGONAL_COST),
                (1, -1, DIAGONAL_COST),
                (1, 1, DIAGONAL_COST)
            ])

        for dr, dc, cost in directions:
            new_row, new_col = row + dr, col + dc
            if self.is_walkable(new_row, new_col):
                neighbors.append((new_row, new_col, cost))

        return neighbors

    def pixel_to_grid(self, px, py):
        col = (px - self.offset_x) // self.cell_size
        row = (py - self.offset_y) // self.cell_size

        if self.in_bounds(row, col):
            return (int(row), int(col))
        return None

    def grid_to_pixel(self, row, col):
        px = self.offset_x + col * self.cell_size + self.cell_size // 2
        py = self.offset_y + row * self.cell_size + self.cell_size // 2
        return (px, py)

    def draw(self, screen):
        """Enhanced grid rendering with better graphics"""
        for row in range(self.rows):
            for col in range(self.cols):
                x = self.offset_x + col * self.cell_size
                y = self.offset_y + row * self.cell_size
                cell = self.grid[row][col]

                # Get cell color
                color = self._get_cell_color(row, col, cell)

                # Draw cell with gradient effect
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)

                # Main cell fill
                pygame.draw.rect(screen, color, rect)

                # Add depth with darker bottom/right edges for walls
                if cell == CELL_WALL:
                    # 3D effect for walls
                    darker = tuple(max(0, c - 30) for c in color)
                    pygame.draw.line(screen, darker, 
                                   (x, y + self.cell_size - 1), 
                                   (x + self.cell_size, y + self.cell_size - 1), 2)
                    pygame.draw.line(screen, darker,
                                   (x + self.cell_size - 1, y),
                                   (x + self.cell_size - 1, y + self.cell_size), 2)

                # Grid lines - subtle
                grid_color = (180, 180, 180) if cell == CELL_EMPTY else (100, 100, 100)
                pygame.draw.rect(screen, grid_color, rect, 1)

        # Draw explored cells (A* visualization)
        if EXPLORATION_ANIMATION and self.explored:
            self._draw_explored(screen)

        # Draw path
        if self.path:
            self._draw_path_enhanced(screen)

    def _get_cell_color(self, row, col, cell_type):
        """Get enhanced cell colors"""
        color_map = {
            CELL_EMPTY: (250, 250, 252),  # Slightly off-white
            CELL_WALL: (70, 70, 75),       # Darker gray
            CELL_NOBITA: COLOR_NOBITA,
            CELL_SCHOOL: COLOR_SCHOOL,
            CELL_GIAN: COLOR_GIAN,
            CELL_BAMBOO: COLOR_BAMBOO,
            CELL_DOOR: COLOR_DOOR
        }
        return color_map.get(cell_type, COLOR_EMPTY)

    def _draw_path_enhanced(self, screen):
        """Draw path with arrows and gradient"""
        if len(self.path) < 2:
            return

        # Draw path segments
        for i in range(len(self.path) - 1):
            start_row, start_col = self.path[i]
            end_row, end_col = self.path[i + 1]

            start_px, start_py = self.grid_to_pixel(start_row, start_col)
            end_px, end_py = self.grid_to_pixel(end_row, end_col)

            # Path line with gradient color
            if i == self.current_path_index:
                color = COLOR_CURRENT
                width = 6
            else:
                # Fade from cyan to blue along path
                t = i / len(self.path)
                color = self._lerp_color(COLOR_PATH, COLOR_NOBITA, t)
                width = 4

            pygame.draw.line(screen, color, (start_px, start_py), (end_px, end_py), width)

            # Draw small circles at waypoints
            pygame.draw.circle(screen, color, (start_px, start_py), 3)

        # Draw end point
        if self.path:
            end_row, end_col = self.path[-1]
            end_px, end_py = self.grid_to_pixel(end_row, end_col)
            pygame.draw.circle(screen, COLOR_SUCCESS, (end_px, end_py), 6)

    def _draw_explored(self, screen):
        """Draw explored cells with fade effect"""
        for row, col in self.explored:
            x = self.offset_x + col * self.cell_size
            y = self.offset_y + row * self.cell_size

            s = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
            s.fill((*COLOR_EXPLORED, 80))
            screen.blit(s, (x, y))

    def _lerp_color(self, color1, color2, t):
        """Linear interpolation between two colors"""
        return tuple(int(c1 + (c2 - c1) * t) for c1, c2 in zip(color1, color2))

    def set_path(self, path):
        self.path = path
        self.current_path_index = 0

    def clear_path(self):
        self.path = []
        self.explored = set()
        self.current_path_index = 0

    def load_level(self, level_data):
        """Load level from string data"""
        self.grid = [[CELL_EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
        self.gadget_positions = []
        self.door_positions = []

        for row in range(min(len(level_data), self.rows)):
            for col in range(min(len(level_data[row]), self.cols)):
                cell = level_data[row][col]

                cell_map = {
                    '.': CELL_EMPTY,
                    '#': CELL_WALL,
                    'N': CELL_NOBITA,
                    'S': CELL_SCHOOL,
                    'G': CELL_GIAN,
                    'B': CELL_BAMBOO,
                    'D': CELL_DOOR
                }

                cell_type = cell_map.get(cell, CELL_EMPTY)
                self.set_cell(row, col, cell_type)

    def reset(self):
        self.grid = [[CELL_EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
        self.path = []
        self.explored = set()
        self.nobita_pos = None
        self.school_pos = None
        self.gian_pos = None
        self.gadget_positions = []
        self.door_positions = []
