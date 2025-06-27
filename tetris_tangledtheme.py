import pygame
import random
import numpy as np  # For matrix operations (linear algebra)

# --- Constants --- #
CELL_SIZE = 27


# Load background image
background_image = pygame.image.load('tangledTheme.png')
SCREEN_WIDTH, SCREEN_HEIGHT = background_image.get_size()

colors = [
    (255, 255, 0),    # O - Yellow
    (255, 0, 0),      # Z - Red
    (0, 255, 0),      # S - Green
    (255, 165, 0),    # L - Orange
    (0, 0, 255),      # J - Blue
    (128, 0, 128),    # T - Purple
    (0, 255, 255)     # I - Cyan
]


# Tetrominoes defined using (x, y) vectors relative to a top-left origin
#Each shape is a list of 2D coordinates relative to a top-left origin.
# They are grouped into one list per type (for rotation expansion if needed later).

tetromino_shapes = [
    [[(0, 0), (1, 0), (0, 1), (1, 1)]],  # O
    [[(0, 0), (0, 1), (1, 1), (1, 2)]],  # Z
    [[(0, 1), (1, 1), (1, 0), (2, 0)]],  # S
    [[(0, 0), (1, 0), (1, 1), (1, 2)]],  # L
    [[(0, 2), (1, 0), (1, 1), (1, 2)]],  # J
    [[(0, 1), (1, 0), (1, 1), (2, 1)]],  # T
    [[(0, 0), (1, 0), (2, 0), (3, 0)]],  # I
]

def rotate_point_90(x, y):
    return -y, x

class Figure:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(tetromino_shapes) - 1)
        self.color = random.randint(0, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return tetromino_shapes[self.type][0]

    def rotated_image(self):
        rotated = [rotate_point_90(x, y) for (x, y) in self.image()]
        min_x = min(p[0] for p in rotated)
        min_y = min(p[1] for p in rotated)
        return [(x - min_x, y - min_y) for (x, y) in rotated]

    def rotate(self):
        tetromino_shapes[self.type][0] = self.rotated_image()

class Tetris:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = [[0 for _ in range(width)] for _ in range(height)]
        self.figure = None
        self.level = 2
        self.score = 0
        self.state = "start"

    def new_figure(self):
        temp_figure = Figure(self.width // 2 - 2, 0)
        for x, y in temp_figure.image():
            px = temp_figure.x + x
            py = temp_figure.y + y
            if py < 0 or py >= self.height or px < 0 or px >= self.width:
               continue
            if self.field[py][px]:
               self.state = "gameover"
               return
        self.figure = temp_figure


    def intersects(self):
        for x, y in self.figure.image():
            px = self.figure.x + x
            py = self.figure.y + y
            if px < 0 or px >= self.width or py >= self.height or self.field[py][px]:
                return True
        return False

    def freeze(self):
        for x, y in self.figure.image():
            self.field[self.figure.y + y][self.figure.x + x] = self.figure.color + 1
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def break_lines(self):
        lines = 0
        new_field = [row for row in self.field if any(cell == 0 for cell in row)]
        lines = self.height - len(new_field)
        for _ in range(lines):
            new_field.insert(0, [0 for _ in range(self.width)])
        self.field = new_field
        self.score += lines ** 2

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def go_side(self, dx):
        self.figure.x += dx
        if self.intersects():
            self.figure.x -= dx

    def rotate(self):
        old = self.figure.image()[:]
        self.figure.rotate()
        if self.intersects():
            tetromino_shapes[self.figure.type][0] = old

# --- Game Loop --- #
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
done = False
clock = pygame.time.Clock()
game = Tetris(20, 10)
fps = 25
counter = 0
pressing_down = False

while not done:
    if game.figure is None:
        game.new_figure()

    counter += 1
    if counter > 10000:
        counter = 0

    if counter % (fps // game.level) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                while not game.intersects():
                    game.figure.y += 1
                game.figure.y -= 1
                game.freeze()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    screen.blit(background_image, (0, 0))

    grid_width = game.width * CELL_SIZE
    grid_height = game.height * CELL_SIZE

    offset_x = (SCREEN_WIDTH - grid_width) // 2
    offset_y = (SCREEN_HEIGHT - grid_height) // 2

    for y in range(game.height):
        for x in range(game.width):
            pygame.draw.rect(screen, ((200,200,200)),
                             [offset_x + CELL_SIZE * x, offset_y + CELL_SIZE * y, CELL_SIZE, CELL_SIZE], 1)
            if game.field[y][x]:
                pygame.draw.rect(screen, colors[game.field[y][x] - 1],
                                 [offset_x + CELL_SIZE * x + 1, offset_y + CELL_SIZE * y + 1,
                                  CELL_SIZE - 2, CELL_SIZE - 2])

    if game.figure:
        for x, y in game.figure.image():
            pygame.draw.rect(screen, colors[game.figure.color],
                             [offset_x + CELL_SIZE * (game.figure.x + x),
                              offset_y + CELL_SIZE * (game.figure.y + y),
                              CELL_SIZE - 2, CELL_SIZE - 2])

    font = pygame.font.SysFont('CinzelDecorative', 34, True, False)
    text = font.render("SCORE: " + str(game.score), True, (224,83,50))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, offset_y - 30))
    screen.blit(text, text_rect)

    if game.state == "gameover":
        font1 = pygame.font.SysFont('CinzelDecorative', 47, True, False)
        go_text = font1.render("Game Over", True, (246,200,73))
        esc_text = font1.render("Press ESC", True, (246,200,73))
        go_rect = go_text.get_rect(center=(SCREEN_WIDTH // 2, offset_y + grid_height + 20))
        esc_rect = esc_text.get_rect(center=(SCREEN_WIDTH // 2, offset_y + grid_height + 60))
        screen.blit(go_text, go_rect)
        screen.blit(esc_text, esc_rect)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()



