#!/usr/bin/env python3
"""Space Transport - 3D Version with Pygame and Interactive Decision Windows"""

import pygame
import sys
import math
import random
from game.engine import GameEngine
from game.story import Story
from game.decisions import DecisionHandler

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Transporte Espacial - 3D")
clock = pygame.time.Clock()

# Colors
BLACK = (10, 14, 39)
DARK_BLUE = (26, 31, 58)
CYAN = (0, 255, 136)
GREEN = (0, 255, 0)
ORANGE = (255, 170, 0)
RED = (255, 107, 53)
WHITE = (255, 255, 255)
LIGHT_CYAN = (100, 220, 200)

class Particle:
    def __init__(self, x, y, vx, vy, color, lifetime):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
    
    def draw(self, surface):
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        size = max(1, int(3 * (self.lifetime / self.max_lifetime)))
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), size)

class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT // 2)
        self.brightness = random.randint(100, 255)
        self.pulse = random.randint(0, 100)
    
    def update(self):
        self.pulse = (self.pulse + 1) % 100
        self.brightness = 150 + int(105 * math.sin(self.pulse * 0.1))
    
    def draw(self, surface):
        pygame.draw.circle(surface, (self.brightness, self.brightness, self.brightness),
                         (self.x, self.y), 1)

class SpaceShip3D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.velocity = 2
        self.particles = []
    
    def update(self):
        self.angle += 0.02
        self.x += math.cos(self.angle) * 0.5
        self.y += math.sin(self.angle) * 0.3
        
        # Generate engine particles
        if random.random() < 0.3:
            particle_x = self.x - 20 * math.cos(self.angle)
            particle_y = self.y - 20 * math.sin(self.angle)
            vx = random.uniform(-3, 3) - math.cos(self.angle) * 5
            vy = random.uniform(-3, 3) - math.sin(self.angle) * 5
            self.particles.append(Particle(particle_x, particle_y, vx, vy, RED, 30))
        
        # Update and remove dead particles
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for p in self.particles:
            p.update()
    
    def draw(self, surface):
        # Draw particles
        for p in self.particles:
            p.draw(surface)
        
        # Draw main hull (3D perspective)
        nose_x = self.x + 30 * math.cos(self.angle)
        nose_y = self.y + 30 * math.sin(self.angle)
        
        right_x = self.x + 15 * math.cos(self.angle + math.pi/2)
        right_y = self.y + 15 * math.sin(self.angle + math.pi/2)
        
        left_x = self.x + 15 * math.cos(self.angle - math.pi/2)
        left_y = self.y + 15 * math.sin(self.angle - math.pi/2)
        
        points = [
            (nose_x, nose_y),
            (right_x, right_y),
            (self.x - 20 * math.cos(self.angle), self.y - 20 * math.sin(self.angle)),
            (left_x, left_y)
        ]
        
        pygame.draw.polygon(surface, LIGHT_CYAN, points, 2)
        pygame.draw.polygon(surface, (0, 150, 200), points)
        
        # Draw window
        pygame.draw.circle(surface, ORANGE, (int(nose_x * 0.8 + self.x * 0.2),
                                            int(nose_y * 0.8 + self.y * 0.2)), 4)

class DecisionWindow:
    def __init__(self, choice, index, total_choices, scene_data):
        self.choice = choice
        self.index = index
        self.total_choices = total_choices
        self.scene_data = scene_data
        
        # Window positioning
        window_width = 300
        window_height = 100
        spacing = 20
        total_width = (window_width + spacing) * total_choices - spacing
        start_x = (SCREEN_WIDTH - total_width) / 2
        
        self.x = start_x + index * (window_width + spacing)
        self.y = SCREEN_HEIGHT - 180
        self.width = window_width
        self.height = window_height
        
        self.hover = False
        self.particles = []
        self.selected = False
    
    def update(self, mouse_pos):
        self.hover = (self.x <= mouse_pos[0] <= self.x + self.width and
                     self.y <= mouse_pos[1] <= self.y + self.height)
        
        if self.hover:
            for _ in range(2):
                vx = random.uniform(-2, 2)
                vy = random.uniform(-3, -1)
                self.particles.append(Particle(
                    random.uniform(self.x, self.x + self.width),
                    self.y + self.height,
                    vx, vy, CYAN, 30
                ))
        
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for p in self.particles:
            p.update()
    
    def draw(self, surface):
        # Draw particles
        for p in self.particles:
            p.draw(surface)
        
        # Border color based on hover
        border_color = GREEN if self.hover else CYAN
        border_width = 3 if self.hover else 2
        
        # Draw window background
        pygame.draw.rect(surface, DARK_BLUE, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, border_color, (self.x, self.y, self.width, self.height), border_width)
        
        # Draw choice number
        font_title = pygame.font.Font(None, 24)
        title = font_title.render(f"OPCIÓN {self.choice['id']}", True, ORANGE)
        surface.blit(title, (self.x + 10, self.y + 10))
        
        # Draw choice text (wrapped)
        font_text = pygame.font.Font(None, 14)
        words = self.choice['text'].split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            line_text = ' '.join(current_line)
            if len(line_text) > 30:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))
        
        y_offset = self.y + 35
        for line in lines[:2]:
            text = font_text.render(line, True, CYAN)
            surface.blit(text, (self.x + 10, y_offset))
            y_offset += 18
    
    def is_clicked(self, mouse_pos):
        return (self.x <= mouse_pos[0] <= self.x + self.width and
               self.y <= mouse_pos[1] <= self.y + self.height)

class GameScreen:
    def __init__(self):
        self.engine = GameEngine()
        self.story = Story()
        self.decision_handler = DecisionHandler(self.engine)
        self.current_scene = "intro"
        
        # Graphics
        self.stars = [Star() for _ in range(100)]
        self.ship = SpaceShip3D(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        self.decision_windows = []
        
        # Display
        self.scene_data = None
        self.load_scene()
    
    def load_scene(self):
        self.scene_data = self.story.get_scene(self.current_scene)
        if not self.scene_data:
            return
        
        # Create decision windows
        self.decision_windows = []
        for i, choice in enumerate(self.scene_data["choices"]):
            window = DecisionWindow(choice, i, len(self.scene_data["choices"]), self.scene_data)
            self.decision_windows.append(window)
    
    def handle_click(self, mouse_pos):
        for window in self.decision_windows:
            if window.is_clicked(mouse_pos):
                choice_id = window.choice['id']
                next_scene = self.decision_handler.handle_decision(self.current_scene, choice_id)
                if next_scene:
                    self.current_scene = next_scene
                    self.load_scene()
                break
    
    def update(self, mouse_pos):
        for star in self.stars:
            star.update()
        
        self.ship.update()
        
        for window in self.decision_windows:
            window.update(mouse_pos)
    
    def draw(self, surface):
        surface.fill(BLACK)
        
        # Draw space background
        for star in self.stars:
            star.draw(surface)
        
        # Draw planets
        pygame.draw.circle(surface, (255, 107, 53), (150, 100), 40)
        pygame.draw.circle(surface, (78, 205, 196), (1200, 120), 35)
        
        # Draw planet names
        font = pygame.font.Font(None, 16)
        mars_text = font.render("Marte", True, ORANGE)
        proxima_text = font.render("Próxima", True, ORANGE)
        surface.blit(mars_text, (120, 155))
        surface.blit(proxima_text, (1150, 160))
        
        # Draw ship
        self.ship.draw(surface)
        
        # Draw HUD frame
        pygame.draw.rect(surface, CYAN, (20, 20, SCREEN_WIDTH - 40, SCREEN_HEIGHT - 240), 2)
        
        # Draw narrative panel
        pygame.draw.rect(surface, DARK_BLUE, (40, 40, SCREEN_WIDTH - 80, 150))
        pygame.draw.rect(surface, CYAN, (40, 40, SCREEN_WIDTH - 80, 150), 2)
        
        # Draw narrative text
        if self.scene_data:
            font = pygame.font.Font(None, 14)
            narrative_lines = self.scene_data["text"].strip().split('\n')
            y_offset = 50
            for line in narrative_lines[:6]:
                if y_offset > 170:
                    break
                text = font.render(line.strip(), True, CYAN)
                surface.blit(text, (60, y_offset))
                y_offset += 18
        
        # Draw status bar
        status_y = SCREEN_HEIGHT - 200
        pygame.draw.rect(surface, DARK_BLUE, (40, status_y, SCREEN_WIDTH - 80, 50))
        pygame.draw.rect(surface, CYAN, (40, status_y, SCREEN_WIDTH - 80, 50), 2)
        
        font_status = pygame.font.Font(None, 12)
        fuel_text = font_status.render(f"Combustible: {self.engine.game_state['fuel']}%", True, ORANGE)
        morale_text = font_status.render(f"Moral: {self.engine.game_state['crew_morale']}%", True, ORANGE)
        time_text = font_status.render(f"Días: {self.engine.game_state['time_elapsed']}", True, ORANGE)
        
        surface.blit(fuel_text, (60, status_y + 10))
        surface.blit(morale_text, (60, status_y + 28))
        surface.blit(time_text, (400, status_y + 10))
        
        # Draw decision windows
        for window in self.decision_windows:
            window.draw(surface)
        
        # Draw title
        font_title = pygame.font.Font(None, 36)
        title = font_title.render("TRANSPORTE ESPACIAL", True, GREEN)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 10))

def main():
    game = GameScreen()
    running = True
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        game.update(mouse_pos)
        game.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
