"""
Enhanced Entities with Better Visual Representation
Character sprites with detailed drawing
"""

import pygame
import time
from constants import *


class Entity:
    """Base class with enhanced drawing"""

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def get_position(self):
        return (self.row, self.col)

    def set_position(self, row, col):
        self.row = row
        self.col = col

    def draw(self, screen, grid):
        """Base draw method"""
        pass


class Nobita(Entity):
    """Enhanced Nobita with character details"""

    def __init__(self, row, col):
        super().__init__(row, col, COLOR_NOBITA)
        self.gadgets = {
            'bamboo': False,
            'bamboo_moves_left': 0
        }

    def move_to(self, row, col):
        self.set_position(row, col)
        if self.gadgets['bamboo']:
            self.gadgets['bamboo_moves_left'] -= 1
            if self.gadgets['bamboo_moves_left'] <= 0:
                self.deactivate_bamboo()

    def activate_bamboo(self, duration=BAMBOO_DURATION):
        self.gadgets['bamboo'] = True
        self.gadgets['bamboo_moves_left'] = duration

    def deactivate_bamboo(self):
        self.gadgets['bamboo'] = False
        self.gadgets['bamboo_moves_left'] = 0

    def draw(self, screen, grid):
        """Draw Nobita with detailed character"""
        px, py = grid.grid_to_pixel(self.row, self.col)

        # Glow effect if bamboo active
        if self.gadgets['bamboo']:
            for i in range(3):
                s = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                pygame.draw.circle(s, (*COLOR_BAMBOO, 40 - i * 10), 
                                 (CELL_SIZE // 2, CELL_SIZE // 2), 
                                 CELL_SIZE // 3 + i * 4)
                screen.blit(s, (px - CELL_SIZE // 2, py - CELL_SIZE // 2))

        # Main body - larger circle
        radius = CELL_SIZE // 2 - 5
        pygame.draw.circle(screen, self.color, (px, py), radius)
        pygame.draw.circle(screen, BLACK, (px, py), radius, 3)

        # Face details
        # Eyes
        eye_y = py - 5
        pygame.draw.circle(screen, WHITE, (px - 8, eye_y), 6)
        pygame.draw.circle(screen, WHITE, (px + 8, eye_y), 6)
        pygame.draw.circle(screen, BLACK, (px - 8, eye_y), 4)
        pygame.draw.circle(screen, BLACK, (px + 8, eye_y), 4)

        # Smile
        pygame.draw.arc(screen, BLACK, 
                       (px - 10, py, 20, 15), 
                       3.14, 0, 3)

        # Glasses frame (optional style)
        pygame.draw.circle(screen, BLACK, (px - 8, eye_y), 7, 2)
        pygame.draw.circle(screen, BLACK, (px + 8, eye_y), 7, 2)

        # Label
        font = pygame.font.Font(None, 16)
        label = font.render("N", True, WHITE)
        label_rect = label.get_rect(center=(px, py + radius + 10))
        screen.blit(label, label_rect)


class School(Entity):
    """Enhanced school building with flag"""

    def __init__(self, row, col):
        super().__init__(row, col, COLOR_SCHOOL)

    def draw(self, screen, grid):
        """Draw detailed school building"""
        px, py = grid.grid_to_pixel(self.row, self.col)

        # Building
        building_width = CELL_SIZE - 10
        building_height = int(CELL_SIZE * 0.8)
        building_rect = pygame.Rect(
            px - building_width // 2,
            py - building_height // 2,
            building_width,
            building_height
        )
        pygame.draw.rect(screen, self.color, building_rect)
        pygame.draw.rect(screen, BLACK, building_rect, 3)

        # Roof
        roof_points = [
            (px, py - building_height // 2 - 8),
            (px - building_width // 2 - 5, py - building_height // 2),
            (px + building_width // 2 + 5, py - building_height // 2)
        ]
        pygame.draw.polygon(screen, COLOR_DANGER, roof_points)
        pygame.draw.polygon(screen, BLACK, roof_points, 2)

        # Windows
        window_size = 6
        window_y_top = py - 8
        window_y_bottom = py + 6

        for wx in [px - 10, px + 2]:
            for wy in [window_y_top, window_y_bottom]:
                window_rect = pygame.Rect(wx, wy, window_size, window_size)
                pygame.draw.rect(screen, (100, 150, 255), window_rect)
                pygame.draw.rect(screen, BLACK, window_rect, 1)

        # Door
        door_rect = pygame.Rect(px - 4, py + building_height // 2 - 12, 8, 12)
        pygame.draw.rect(screen, (139, 69, 19), door_rect)
        pygame.draw.rect(screen, BLACK, door_rect, 1)

        # Flag pole
        pygame.draw.line(screen, BLACK, 
                        (px + building_width // 2, py - building_height // 2),
                        (px + building_width // 2, py - building_height // 2 - 15), 3)

        # Flag
        flag_points = [
            (px + building_width // 2, py - building_height // 2 - 15),
            (px + building_width // 2 + 12, py - building_height // 2 - 12),
            (px + building_width // 2, py - building_height // 2 - 9)
        ]
        pygame.draw.polygon(screen, COLOR_DANGER, flag_points)

        # Label
        font = pygame.font.Font(None, 16)
        label = font.render("SCHOOL", True, BLACK)
        label_rect = label.get_rect(center=(px, py + building_height // 2 + 12))
        screen.blit(label, label_rect)


class Gian(Entity):
    """Enhanced Gian with detailed angry character"""

    def __init__(self, row, col, patrol_points):
        super().__init__(row, col, COLOR_GIAN)
        self.patrol_points = patrol_points if patrol_points else [(row, col)]
        self.current_target = 0
        self.speed = GIAN_SPEED
        self.pause_time = GIAN_PATROL_PAUSE
        self.paused = False
        self.pause_start = None
        self.last_move_time = time.time()

    def update(self, dt):
        if self.paused:
            if time.time() - self.pause_start > self.pause_time:
                self.paused = False
                self.current_target = (self.current_target + 1) % len(self.patrol_points)
            return

        target = self.patrol_points[self.current_target]
        if (self.row, self.col) == target:
            self.paused = True
            self.pause_start = time.time()
            return

        current_time = time.time()
        if current_time - self.last_move_time >= 1.0 / self.speed:
            self.last_move_time = current_time

            if self.row < target[0]:
                self.row += 1
            elif self.row > target[0]:
                self.row -= 1
            elif self.col < target[1]:
                self.col += 1
            elif self.col > target[1]:
                self.col -= 1

    def draw(self, screen, grid):
        """Draw detailed Gian character"""
        px, py = grid.grid_to_pixel(self.row, self.col)

        # Danger zone indicator
        danger_surf = pygame.Surface((CELL_SIZE * 2, CELL_SIZE * 2), pygame.SRCALPHA)
        pygame.draw.circle(danger_surf, (*self.color, 30), 
                         (CELL_SIZE, CELL_SIZE), CELL_SIZE)
        screen.blit(danger_surf, (px - CELL_SIZE, py - CELL_SIZE))

        # Main body - larger
        radius = CELL_SIZE // 2 - 3
        pygame.draw.circle(screen, self.color, (px, py), radius)
        pygame.draw.circle(screen, BLACK, (px, py), radius, 3)

        # Angry eyes
        eye_y = py - 6
        # Left eye (angry slant)
        pygame.draw.line(screen, BLACK, (px - 12, eye_y - 2), (px - 6, eye_y + 2), 3)
        # Right eye (angry slant)
        pygame.draw.line(screen, BLACK, (px + 6, eye_y + 2), (px + 12, eye_y - 2), 3)

        # Pupils
        pygame.draw.circle(screen, BLACK, (px - 9, eye_y), 2)
        pygame.draw.circle(screen, BLACK, (px + 9, eye_y), 2)

        # Angry mouth (frown)
        pygame.draw.arc(screen, BLACK, 
                       (px - 12, py + 5, 24, 12), 
                       0, 3.14, 3)

        # Eyebrows (angry)
        pygame.draw.line(screen, BLACK, (px - 14, eye_y - 6), (px - 4, eye_y - 4), 2)
        pygame.draw.line(screen, BLACK, (px + 4, eye_y - 4), (px + 14, eye_y - 6), 2)

        # Label
        font = pygame.font.Font(None, 16)
        label = font.render("GIAN", True, WHITE)
        label_rect = label.get_rect(center=(px, py + radius + 10))

        # Label background
        bg_rect = label_rect.inflate(4, 2)
        pygame.draw.rect(screen, self.color, bg_rect, border_radius=3)
        screen.blit(label, label_rect)


class Gadget(Entity):
    """Enhanced gadget base class"""

    def __init__(self, row, col, gadget_type, color):
        super().__init__(row, col, color)
        self.gadget_type = gadget_type
        self.collected = False

    def collect(self):
        self.collected = True


class BambooCopter(Gadget):
    """Enhanced Bamboo Copter with animation"""

    def __init__(self, row, col):
        super().__init__(row, col, 'bamboo', COLOR_BAMBOO)
        self.rotation = 0

    def draw(self, screen, grid):
        if self.collected:
            return

        px, py = grid.grid_to_pixel(self.row, self.col)

        # Glow effect
        glow_surf = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*self.color, 60), 
                         (CELL_SIZE // 2, CELL_SIZE // 2), CELL_SIZE // 3)
        screen.blit(glow_surf, (px - CELL_SIZE // 2, py - CELL_SIZE // 2))

        # Propeller base
        pygame.draw.circle(screen, self.color, (px, py), 8)
        pygame.draw.circle(screen, BLACK, (px, py), 8, 2)

        # Rotating propellers
        self.rotation += 5
        blade_length = 18
        for angle in [self.rotation, self.rotation + 90, self.rotation + 180, self.rotation + 270]:
            import math
            rad = math.radians(angle)
            x1 = px + blade_length * math.cos(rad)
            y1 = py + blade_length * math.sin(rad)
            x2 = px - blade_length * math.cos(rad)
            y2 = py - blade_length * math.sin(rad)
            pygame.draw.line(screen, self.color, (x1, y1), (x2, y2), 4)

        # Center dot
        pygame.draw.circle(screen, BLACK, (px, py), 4)

        # Label
        font = pygame.font.Font(None, 14)
        label = font.render("SPEED+", True, BLACK)
        label_rect = label.get_rect(center=(px, py + 20))

        bg_rect = label_rect.inflate(4, 2)
        pygame.draw.rect(screen, self.color, bg_rect, border_radius=3)
        screen.blit(label, label_rect)


class AnywhereDoor(Gadget):
    """Enhanced Anywhere Door"""

    def __init__(self, row, col, pair_id=0):
        super().__init__(row, col, 'door', COLOR_DOOR)
        self.pair_id = pair_id

    def draw(self, screen, grid):
        if self.collected:
            return

        px, py = grid.grid_to_pixel(self.row, self.col)

        # Glow effect
        glow_surf = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*self.color, 60), 
                         (CELL_SIZE // 2, CELL_SIZE // 2), CELL_SIZE // 3)
        screen.blit(glow_surf, (px - CELL_SIZE // 2, py - CELL_SIZE // 2))

        # Door frame
        door_width = 16
        door_height = 24
        door_rect = pygame.Rect(px - door_width // 2, py - door_height // 2, 
                               door_width, door_height)
        pygame.draw.rect(screen, self.color, door_rect, border_radius=4)
        pygame.draw.rect(screen, BLACK, door_rect, 2, border_radius=4)

        # Door panels
        panel_rect = pygame.Rect(px - door_width // 2 + 2, py - door_height // 2 + 2,
                                door_width - 4, door_height // 2 - 2)
        pygame.draw.rect(screen, (*self.color, 180), panel_rect, border_radius=2)
        pygame.draw.rect(screen, BLACK, panel_rect, 1, border_radius=2)

        panel_rect.y = py + 1
        pygame.draw.rect(screen, (*self.color, 180), panel_rect, border_radius=2)
        pygame.draw.rect(screen, BLACK, panel_rect, 1, border_radius=2)

        # Door knob
        pygame.draw.circle(screen, COLOR_BAMBOO, (px + 4, py), 3)
        pygame.draw.circle(screen, BLACK, (px + 4, py), 3, 1)

        # Label
        font = pygame.font.Font(None, 14)
        label = font.render("TELEPORT", True, WHITE)
        label_rect = label.get_rect(center=(px, py + 20))

        bg_rect = label_rect.inflate(4, 2)
        pygame.draw.rect(screen, self.color, bg_rect, border_radius=3)
        screen.blit(label, label_rect)
