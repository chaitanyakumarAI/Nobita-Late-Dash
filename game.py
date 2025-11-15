"""Main game logic and state management"""
import pygame
import time
from constants import *
from grid import Grid
from ultimate_astar_heuristic import AStar, PathfindingVisualizer
from entities import Nobita, School, Gian, BambooCopter, AnywhereDoor


class Game:
    """Main game controller"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        
        # Game components
        self.grid = Grid()
        self.astar = AStar(self.grid)
        self.visualizer = PathfindingVisualizer(self.astar)
        
        # Game state
        self.state = STATE_MENU
        self.entities = []
        self.nobita = None
        self.school = None
        self.gian = None
        
        # Stats
        self.moves = 0
        self.start_time = None
        self.elapsed_time = 0
        
        # Load default level
        self.load_level(1)

    def load_level(self, level_num):
        """Load a specific level"""
        # Example level data
        level_1 = [
            "####################",
            "#N.................#",
            "#.###.............S#",
            "#.#.#..............#",
            "#.#.#.....B........#",
            "#.....G............#",
            "#..................#",
            "#....D.............#",
            "####################"
        ]
        
        self.grid.load_level(level_1)
        
        # Create entities
        self.nobita = Nobita(*self.grid.nobita_pos)
        self.school = School(*self.grid.school_pos)
        
        if self.grid.gian_pos:
            patrol = [self.grid.gian_pos, (5, 10), (8, 10)]
            self.gian = Gian(*self.grid.gian_pos, patrol)
        
        self.entities = [self.nobita, self.school]
        if self.gian:
            self.entities.append(self.gian)

    def handle_events(self):
        """Process input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE and self.state == STATE_PLAYING:
                    self.find_and_follow_path()
                elif event.key == pygame.K_r:
                    self.reset()
        
        return True

    def find_and_follow_path(self):
        """Calculate path and start moving"""
        start = self.nobita.get_position()
        goal = self.school.get_position()
        
        path = self.astar.find_path(start, goal)
        if path:
            self.grid.set_path(path)
            self.state = STATE_MOVING

    def update(self, dt):
        """Update game state"""
        if self.state == STATE_MOVING:
            # Move along path (simplified)
            pass
        
        if self.gian:
            self.gian.update(dt)
            self.grid.set_cell(*self.gian.get_position(), CELL_GIAN)

    def draw(self):
        """Render game"""
        self.screen.fill(COLOR_BG)
        self.grid.draw(self.screen)
        
        for entity in self.entities:
            entity.draw(self.screen, self.grid)
        
        self.draw_ui()
        pygame.display.flip()

    def draw_ui(self):
        """Draw UI elements"""
        font = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        text = font.render(f"Moves: {self.moves}", True, COLOR_TEXT)
        self.screen.blit(text, (10, 10))

    def reset(self):
        """Reset game to initial state"""
        self.load_level(1)
        self.moves = 0
        self.state = STATE_PLAYING

    def run(self):
        """Main game loop"""
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            running = self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()
