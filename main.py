"""
FIXED - Gian Cannot Move Through Walls
Wall collision checking for all Gian movement
"""

import pygame
import sys
import time
import math
from constants import *
from grid import Grid
from ultimate_astar_heuristic import UltimateAStar
from entities import Nobita, School, Gian, BambooCopter, AnywhereDoor


class SmartGian(Gian):
    """
    FIX: Intelligent Gian that CANNOT move through walls
    """
    def __init__(self, row, col, patrol_points, chase_range=8):
        super().__init__(row, col, patrol_points)
        self.chase_range = chase_range
        self.mode = "patrol"
        self.chase_target = None

    def update(self, dt, nobita_pos, grid):
        """
        FIX: Added grid parameter for wall checking
        """
        distance = abs(self.row - nobita_pos[0]) + abs(self.col - nobita_pos[1])

        if distance <= self.chase_range:
            self.mode = "chase"
            self.chase_target = nobita_pos
        else:
            self.mode = "patrol"
            self.chase_target = None

        if self.paused:
            if time.time() - self.pause_start > self.pause_time:
                self.paused = False
                if self.mode == "patrol":
                    self.current_target = (self.current_target + 1) % len(self.patrol_points)
            return

        target = self.chase_target if self.mode == "chase" else self.patrol_points[self.current_target]

        if (self.row, self.col) == target:
            if self.mode == "patrol":
                self.paused = True
                self.pause_start = time.time()
            return

        current_time = time.time()
        if current_time - self.last_move_time >= 1.0 / self.speed:
            self.last_move_time = current_time

            # FIX: Move with wall checking
            self.move_toward_target(target, grid)

    def move_toward_target(self, target, grid):
        """
        FIX: Smart movement that avoids walls
        Tries to move in direction of target, but only if valid
        """
        target_row, target_col = target

        # Try all 4 directions, prioritize those closer to target
        directions = []

        # Vertical movement
        if self.row < target_row:
            directions.append((1, 0, "down"))  # Move down
        elif self.row > target_row:
            directions.append((-1, 0, "up"))  # Move up

        # Horizontal movement
        if self.col < target_col:
            directions.append((0, 1, "right"))  # Move right
        elif self.col > target_col:
            directions.append((0, -1, "left"))  # Move left

        # Try primary directions first
        for dr, dc, direction in directions:
            new_row = self.row + dr
            new_col = self.col + dc

            # FIX: Check if move is valid (not wall, in bounds)
            if grid.is_walkable(new_row, new_col):
                self.row = new_row
                self.col = new_col
                return  # Success!

        # If primary directions blocked, try other directions
        all_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in all_directions:
            new_row = self.row + dr
            new_col = self.col + dc

            if grid.is_walkable(new_row, new_col):
                # Move to any valid adjacent cell
                self.row = new_row
                self.col = new_col
                return

        # If completely stuck, stay in place
        # This should rarely happen with good level design


class Button:
    """Polished button with smooth animations"""
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.enabled = True
        self.hover_scale = 1.0

    def update(self):
        target_scale = 1.05 if self.is_hovered and self.enabled else 1.0
        self.hover_scale += (target_scale - self.hover_scale) * 0.3

    def draw(self, screen, font):
        self.update()

        if not self.enabled:
            color = (100, 100, 100)
            text_color = (150, 150, 150)
        else:
            color = self.hover_color if self.is_hovered else self.color
            text_color = self.text_color

        scaled_rect = self.rect.inflate(
            int((self.hover_scale - 1.0) * self.rect.width),
            int((self.hover_scale - 1.0) * self.rect.height)
        )

        shadow_rect = scaled_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, (0, 0, 0, 80), shadow_surface.get_rect(), border_radius=10)
        screen.blit(shadow_surface, shadow_rect)

        pygame.draw.rect(screen, color, scaled_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, scaled_rect, 2, border_radius=10)

        text_surf = font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=scaled_rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if not self.enabled:
            return False
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False


class FixedGame:
    """Game with Gian wall collision fix"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE + " - A* Pathfinding Demo")
        self.clock = pygame.time.Clock()

        self.font_title = pygame.font.Font(None, 48)
        self.font_large = pygame.font.Font(None, 32)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)

        self.grid = Grid()
        self.astar = UltimateAStar(self.grid)

        self.state = STATE_MENU
        self.current_level = 1
        self.max_level = 3

        self.nobita = None
        self.school = None
        self.gian = None
        self.gadgets = []

        self.moves = 0
        self.max_moves = 40
        self.optimal_moves = 20
        self.start_time = None
        self.elapsed_time = 0

        self.path = []
        self.path_index = 0
        self.is_moving = False
        self.move_timer = 0

        self.bamboo_available = False
        self.bamboo_active = False
        self.door_positions = []

        self.score = 0
        self.stars = 0

        self.create_buttons()

    def create_buttons(self):
        button_y = SCREEN_HEIGHT - 60

        self.btn_find_path = Button(60, button_y, 180, 50,
            "Find Path", (60, 200, 60), (100, 255, 100), BLACK)

        self.btn_auto_move = Button(260, button_y, 180, 50,
            "Auto Move", (60, 150, 255), (100, 200, 255), WHITE)

        self.btn_toggle_bamboo = Button(460, button_y, 180, 50,
            "Bamboo OFF", (255, 180, 0), (255, 220, 100), BLACK)

        self.btn_reset = Button(660, button_y, 180, 50,
            "Reset", (220, 60, 60), (255, 100, 100), WHITE)

        self.buttons = [self.btn_find_path, self.btn_auto_move, 
                       self.btn_toggle_bamboo, self.btn_reset]

    def load_level(self, level_num):
        levels = {
            1: {
                "map": [
                    "####################",
                    "#N........#.......S#",
                    "#.###.....#...G....#",
                    "#.#.#.....#........#",
                    "#.#.#.....#...B....#",
                    "#..................#",
                    "#..................#",
                    "#....D.....D.......#",
                    "#..................#",
                    "####################",
                ],
                "max_moves": 40,
                "optimal_moves": 22,
                "gian_speed": 1.5,
                "gian_patrol": [(2, 10), (2, 15), (6, 15), (6, 10)],
                "door_pairs": [((7, 5), (7, 11))]
            },
            2: {
                "map": [
                    "####################",
                    "#N................D#",
                    "#..####.....####...#",
                    "#..#..B.......G#...#",
                    "#..#...........#...#",
                    "#..#...........#...#",
                    "#..############...D#",
                    "#..................#",
                    "#.................S#",
                    "####################",
                ],
                "max_moves": 40,
                "optimal_moves": 25,
                "gian_speed": 2.0,
                "gian_patrol": [(3, 14), (3, 10), (5, 10), (5, 14)],
                "door_pairs": [( (1, 18),(6, 18) )]
            },
            3: {
                "map": [
                    "####################",
                    "#N.#.....G........S#",
                    "##.#.###.#####.#.#.#",
                    "#..#...#.#...#.#.#.#",
                    "#.##.#.#.#.#B#.#.#.#",
                    "#....#.#...#.#...#.#",
                    "#.####.#####.#####.#",
                    "#D..........D......#",
                    "#..................#",
                    "####################",
                ],
                "max_moves": 40,
                "optimal_moves": 25,
                "gian_speed": 2.0,
                # FIX: Better patrol that stays in open areas
                "gian_patrol": [(1, 10), (3, 10), (5, 10), (5, 2)],
                "door_pairs": [((7, 1), (7, 12))]
            }
        }

        level_data = levels.get(level_num, levels[1])
        self.grid.load_level(level_data["map"])

        self.max_moves = level_data["max_moves"]
        self.optimal_moves = level_data["optimal_moves"]

        self.nobita = Nobita(*self.grid.nobita_pos)
        self.school = School(*self.grid.school_pos)

        # FIX: Create SmartGian with wall checking
        if self.grid.gian_pos:
            self.gian = SmartGian(*self.grid.gian_pos, level_data["gian_patrol"])
            self.gian.speed = level_data["gian_speed"]

        self.gadgets = []
        for pos in self.grid.gadget_positions:
            self.gadgets.append(BambooCopter(*pos))
        for pos in self.grid.door_positions:
            self.gadgets.append(AnywhereDoor(*pos))

        self.astar.door_positions = []
        self.door_positions = level_data.get("door_pairs", [])
        for door1, door2 in self.door_positions:
            self.astar.add_door_pair(door1, door2)

        self.moves = 0
        self.path = []
        self.is_moving = False
        self.start_time = time.time()
        self.bamboo_available = False
        self.bamboo_active = False
        self.state = STATE_PLAYING

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            for button in self.buttons:
                if button.handle_event(event):
                    if button == self.btn_find_path:
                        self.find_path()
                    elif button == self.btn_auto_move:
                        self.auto_move()
                    elif button == self.btn_toggle_bamboo:
                        self.toggle_bamboo()
                    elif button == self.btn_reset:
                        self.reset_level()

            if event.type == pygame.KEYDOWN:
                if self.state == STATE_MENU:
                    if event.key == pygame.K_RETURN:
                        self.load_level(1)

                elif self.state in [STATE_PLAYING, STATE_PATHFINDING]:
                    if event.key == pygame.K_ESCAPE:
                        self.state = STATE_MENU
                    elif event.key == pygame.K_SPACE:
                        self.find_path()
                    elif event.key == pygame.K_a:
                        self.auto_move()
                    elif event.key == pygame.K_b:
                        self.toggle_bamboo()
                    elif event.key == pygame.K_r:
                        self.reset_level()
                    elif not self.is_moving:
                        row, col = self.nobita.row, self.nobita.col
                        moved = False

                        if event.key == pygame.K_UP:
                            row -= 1
                            moved = True
                        elif event.key == pygame.K_DOWN:
                            row += 1
                            moved = True
                        elif event.key == pygame.K_LEFT:
                            col -= 1
                            moved = True
                        elif event.key == pygame.K_RIGHT:
                            col += 1
                            moved = True

                        if moved:
                            self.move_nobita(row, col)

                elif self.state in [STATE_WON, STATE_LOST]:
                    if event.key == pygame.K_r:
                        self.reset_level()
                    elif event.key == pygame.K_n and self.state == STATE_WON:
                        self.next_level()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = STATE_MENU

        return True

    def toggle_bamboo(self):
        if not self.bamboo_available:
            print("❌ Collect Bamboo Copter first!")
            return

        self.bamboo_active = not self.bamboo_active
        self.astar.set_bamboo_collected(self.bamboo_active)

        if self.bamboo_active:
            print("🚁 Bamboo ACTIVATED - Moves cost 0.5x!")
        else:
            print("Bamboo DEACTIVATED - Normal cost")

        if self.path:
            self.find_path()

    def find_path(self):
        if self.is_moving:
            return

        start = (self.nobita.row, self.nobita.col)
        goal = (self.school.row, self.school.col)

        if not self.grid.in_bounds(*start) or not self.grid.in_bounds(*goal):
            print("❌ Invalid start or goal position!")
            return

        print(f"\n🔍 Finding path with A*...")

        try:
            self.path = self.astar.find_path(start, goal, record_exploration=True)

            if self.path:
                self.grid.set_path(self.path)
                self.state = STATE_PATHFINDING

                path_steps = len(self.path) - 1
                effective_moves = path_steps * (0.5 if self.bamboo_active else 1.0)

                print(f"✓ Path: {path_steps} steps = {effective_moves:.1f} moves")
            else:
                print("❌ No path found!")
        except Exception as e:
            print(f"❌ A* Error: {e}")
            self.path = []

    def auto_move(self):
        if self.path and not self.is_moving:
            self.is_moving = True
            self.path_index = 1
            self.move_timer = 0

    def check_door_teleport(self, row, col):
        for door1, door2 in self.door_positions:
            if (row, col) == door1:
                print(f"🚪 TELEPORTED! {door1} → {door2}")
                return door2
            elif (row, col) == door2:
                print(f"🚪 TELEPORTED! {door2} → {door1}")
                return door1
        return None

    def move_nobita(self, new_row, new_col):
        if not self.grid.is_walkable(new_row, new_col):
            return False

        move_cost = 0.5 if self.bamboo_active else 1.0

        if self.moves + move_cost > self.max_moves:
            self.state = STATE_LOST
            print(f"❌ OUT OF MOVES!")
            return False

        self.grid.set_cell(self.nobita.row, self.nobita.col, CELL_EMPTY)
        self.nobita.row = new_row
        self.nobita.col = new_col
        self.grid.set_cell(new_row, new_col, CELL_NOBITA)

        self.moves += move_cost

        for gadget in self.gadgets:
            if not gadget.collected and isinstance(gadget, BambooCopter):
                if (new_row, new_col) == (gadget.row, gadget.col):
                    gadget.collected = True
                    self.bamboo_available = True
                    print("✨ Bamboo Copter collected! Press B to toggle")

        door_dest = self.check_door_teleport(new_row, new_col)
        if door_dest:
            self.grid.set_cell(new_row, new_col, CELL_EMPTY)
            self.nobita.row, self.nobita.col = door_dest
            self.grid.set_cell(*door_dest, CELL_NOBITA)
            self.moves += move_cost

        if (self.nobita.row, self.nobita.col) == (self.school.row, self.school.col):
            self.calculate_score()
            self.state = STATE_WON
            return True

        if self.gian and (self.nobita.row, self.nobita.col) == (self.gian.row, self.gian.col):
            self.state = STATE_LOST
            print("❌ CAUGHT BY GIAN!")
            return False

        return True

    def calculate_score(self):
        if self.moves <= self.optimal_moves:
            self.stars = 3
        elif self.moves <= self.optimal_moves + 5:
            self.stars = 2
        else:
            self.stars = 1

        self.score = int((self.max_moves - self.moves) * 10 + self.stars * 100)

    def update(self, dt):
        if self.state in [STATE_PLAYING, STATE_PATHFINDING]:
            # FIX: Pass grid to Gian for wall checking
            if self.gian:
                old_pos = (self.gian.row, self.gian.col)
                nobita_pos = (self.nobita.row, self.nobita.col)

                # FIX: Pass grid parameter!
                self.gian.update(dt, nobita_pos, self.grid)

                new_pos = (self.gian.row, self.gian.col)

                if old_pos != new_pos:
                    self.grid.set_cell(*old_pos, CELL_EMPTY)
                    self.grid.set_cell(*new_pos, CELL_GIAN)
                    self.grid.gian_pos = new_pos

                    if new_pos == nobita_pos:
                        self.state = STATE_LOST

            if self.is_moving and self.path:
                self.move_timer += dt

                if self.move_timer >= MOVEMENT_SPEED:
                    self.move_timer = 0

                    if self.path_index < len(self.path):
                        next_pos = self.path[self.path_index]
                        success = self.move_nobita(*next_pos)

                        if not success:
                            self.is_moving = False
                            self.grid.clear_path()
                        else:
                            self.grid.current_path_index = self.path_index
                            self.path_index += 1
                    else:
                        self.is_moving = False
                        self.grid.clear_path()

            if self.start_time:
                self.elapsed_time = time.time() - self.start_time

    def draw(self):
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(230 + (240 - 230) * color_ratio)
            g = int(230 + (245 - 230) * color_ratio)
            b = int(250 + (255 - 250) * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        if self.state == STATE_MENU:
            self.draw_menu()
        else:
            self.draw_game()

        pygame.display.flip()

    def draw_menu(self):
        title_shadow = self.font_title.render("NOBITA'S LATE DASH", True, (100, 100, 100))
        title = self.font_title.render("NOBITA'S LATE DASH", True, COLOR_NOBITA)

        self.screen.blit(title_shadow, title_shadow.get_rect(center=(SCREEN_WIDTH//2 + 2, 152)))
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 150)))

        subtitle = self.font_large.render("A* Pathfinding with Heuristics", True, (80, 80, 100))
        self.screen.blit(subtitle, subtitle.get_rect(center=(SCREEN_WIDTH//2, 200)))

        instructions = [
            "🧠 Gadgets modify A* cost function!",
            "",
            "SPACE - Find path | A - Auto-move | B - Toggle Bamboo",
            "Arrow Keys - Manual movement",
            "",
            "🚁 Bamboo: 0.5x cost | 🚪 Doors: Teleportation",
            "",
            "FIX: Gian cannot move through walls!",
            "",
            "PRESS ENTER TO START"
        ]

        y = 260
        for line in instructions:
            if line == "PRESS ENTER TO START":
                size = self.font_medium
                color = COLOR_NOBITA
            elif line == "FIX: Gian cannot move through walls!":
                size = self.font_small
                color = COLOR_SUCCESS
            else:
                size = self.font_small
                color = (60, 60, 80)

            text = size.render(line, True, color)
            self.screen.blit(text, text.get_rect(center=(SCREEN_WIDTH//2, y)))
            y += 30

    def draw_game(self):
        self.grid.draw(self.screen)

        for gadget in self.gadgets:
            if not gadget.collected:
                gadget.draw(self.screen, self.grid)

        self.nobita.draw(self.screen, self.grid)
        self.school.draw(self.screen, self.grid)
        if self.gian:
            self.gian.draw(self.screen, self.grid)

        self.draw_status()
        self.draw_buttons()

        if self.state == STATE_WON:
            self.draw_win_screen()
        elif self.state == STATE_LOST:
            self.draw_lose_screen()

    def draw_status(self):
        gradient_surface = pygame.Surface((SCREEN_WIDTH, 75), pygame.SRCALPHA)
        for y in range(75):
            alpha = 200 + int(55 * (1 - y / 75))
            pygame.draw.line(gradient_surface, (35, 35, 55, alpha), (0, y), (SCREEN_WIDTH, y))
        self.screen.blit(gradient_surface, (0, 0))
        pygame.draw.line(self.screen, (80, 80, 100), (0, 75), (SCREEN_WIDTH, 75), 2)

        level_text = self.font_medium.render(f"Level {self.current_level}/{self.max_level}", True, WHITE)
        self.screen.blit(level_text, (15, 12))

        ratio = self.moves / self.max_moves
        moves_color = COLOR_SUCCESS if ratio < 0.6 else (COLOR_BAMBOO if ratio < 0.85 else COLOR_DANGER)

        moves_text = self.font_large.render(f"{self.moves:.1f}/{self.max_moves}", True, moves_color)
        self.screen.blit(moves_text, (15, 42))

        if self.bamboo_available:
            status = "🚁 ON" if self.bamboo_active else "🚁 OFF"
            color = COLOR_BAMBOO if self.bamboo_active else (150, 150, 150)
            detail = "(0.5x cost)" if self.bamboo_active else "(Press B)"
        else:
            status = "🚁 Not found"
            color = (120, 120, 120)
            detail = "(Find yellow)"

        bamboo_text = self.font_medium.render(status, True, color)
        self.screen.blit(bamboo_text, (280, 20))
        detail_text = self.font_small.render(detail, True, (200, 200, 200))
        self.screen.blit(detail_text, (280, 48))

        if self.door_positions:
            door_text = self.font_small.render(f"🚪 {len(self.door_positions)} Door pair(s)", True, COLOR_DOOR)
            self.screen.blit(door_text, (520, 20))

        if self.gian:
            mode_color = COLOR_DANGER if self.gian.mode == "chase" else COLOR_SUCCESS
            mode_text = self.font_medium.render(f"Gian: {self.gian.mode.upper()}", True, mode_color)
            self.screen.blit(mode_text, (750, 28))

    def draw_buttons(self):
        if self.bamboo_available:
            self.btn_toggle_bamboo.text = "Bamboo ON" if self.bamboo_active else "Bamboo OFF"
            self.btn_toggle_bamboo.enabled = True
        else:
            self.btn_toggle_bamboo.text = "Find Bamboo"
            self.btn_toggle_bamboo.enabled = False

        self.btn_auto_move.enabled = len(self.path) > 0 and not self.is_moving

        for button in self.buttons:
            button.draw(self.screen, self.font_small)

    def draw_win_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(230)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        win = self.font_title.render("LEVEL COMPLETE!", True, COLOR_SUCCESS)
        win_rect = win.get_rect(center=(SCREEN_WIDTH//2, 240))

        for i in range(3):
            glow = pygame.Surface((win.get_width() + i*10, win.get_height() + i*10), pygame.SRCALPHA)
            glow_rect = glow.get_rect(center=win_rect.center)
            pygame.draw.rect(glow, (*COLOR_SUCCESS, 30 - i*10), glow.get_rect(), border_radius=15)
            self.screen.blit(glow, glow_rect)

        self.screen.blit(win, win_rect)

        for i in range(3):
            color = COLOR_BAMBOO if i < self.stars else (80, 80, 80)
            pygame.draw.circle(self.screen, color, (SCREEN_WIDTH//2 - 60 + i*60, 320), 20)
            pygame.draw.circle(self.screen, BLACK, (SCREEN_WIDTH//2 - 60 + i*60, 320), 20, 2)

        stats = self.font_large.render(f"Moves: {self.moves:.1f} / {self.max_moves}", True, WHITE)
        self.screen.blit(stats, stats.get_rect(center=(SCREEN_WIDTH//2, 390)))

        score_text = self.font_large.render(f"Score: {self.score}", True, COLOR_BAMBOO)
        self.screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH//2, 430)))

        controls = "N - Next | R - Replay | ESC - Menu" if self.current_level < self.max_level else "Complete! | R - Replay | ESC - Menu"
        ctrl_text = self.font_medium.render(controls, True, WHITE)
        self.screen.blit(ctrl_text, ctrl_text.get_rect(center=(SCREEN_WIDTH//2, 490)))

    def draw_lose_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(230)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        lose = self.font_title.render("GAME OVER", True, COLOR_DANGER)
        self.screen.blit(lose, lose.get_rect(center=(SCREEN_WIDTH//2, 280)))

        hint1 = "🚁 Collect Bamboo to reduce move cost!"
        hint2 = "🚪 Use Doors to teleport and save moves!"

        hint1_text = self.font_medium.render(hint1, True, COLOR_BAMBOO)
        hint2_text = self.font_medium.render(hint2, True, COLOR_DOOR)

        self.screen.blit(hint1_text, hint1_text.get_rect(center=(SCREEN_WIDTH//2, 360)))
        self.screen.blit(hint2_text, hint2_text.get_rect(center=(SCREEN_WIDTH//2, 400)))

        controls = "R - Retry | ESC - Menu"
        ctrl_text = self.font_medium.render(controls, True, WHITE)
        self.screen.blit(ctrl_text, ctrl_text.get_rect(center=(SCREEN_WIDTH//2, 470)))

    def reset_level(self):
        self.load_level(self.current_level)

    def next_level(self):
        if self.current_level < self.max_level:
            self.current_level += 1
            self.load_level(self.current_level)
        else:
            self.state = STATE_MENU

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            running = self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = FixedGame()
    game.run()
