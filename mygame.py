import pgzrun
import random
from math import sin, cos, radians

# Configurações iniciais
WIDTH = 800
HEIGHT = 600
TITLE = "Platformer Game - Surviving the Apocalypse"
MUSIC_ON = True
GRAVITY = 0.5
GROUND_LEVEL = HEIGHT - 150  

# Imagens de sprites
HERO_SPRITES = ["hero_walk1", "hero_walk2", "hero_idle"]
ENEMY_SPRITES = ["enemy_walk1", "enemy_walk2", "enemy_idle"]
NEW_ENEMY_SPRITES = ["enemy2_walk1", "enemy2_walk2", "enemy2_idle"]  
BACKGROUND_IMAGE = "background"  

collision_sound = sounds.load("combat-clash.wav") 

# Classes
class Character:
    def __init__(self, x, y, sprites):
        self.x = x
        self.y = y
        self.sprites = sprites
        self.image = sprites[2]
        self.frame = 0
        self.speed_x = 0
        self.speed_y = 0
        self.on_ground = False

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def animate(self):
        self.frame += 1
        if self.frame >= len(self.sprites) * 10:
            self.frame = 0
        self.image = self.sprites[self.frame // 10]

class Hero(Character):
    def update(self):
        self.speed_y += GRAVITY
        self.y += self.speed_y

        if self.y >= GROUND_LEVEL:
            self.y = GROUND_LEVEL
            self.speed_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        # Movimentação horizontal
        self.x += self.speed_x
        self.x = max(0, min(WIDTH - 50, self.x))
        self.animate()

        # Verificar colisão com inimigo
        for enemy in enemies:
            if self.collides_with(enemy):
                self.die()

    def collides_with(self, enemy):
        # Verificar colisão simples entre o herói e o inimigo
        if self.x < enemy.x + 50 and self.x + 50 > enemy.x and self.y < enemy.y + 50 and self.y + 50 > enemy.y:
            # Tocar som de colisão
            collision_sound.play()
            return True
        return False

    def die(self):
        # Reiniciar o jogo (o herói morre)
        global hero
        hero = Hero(WIDTH // 2 - 400, GROUND_LEVEL, HERO_SPRITES)

class Enemy(Character):
    def __init__(self, x, y, sprites, patrol_range):
        super().__init__(x, y, sprites)
        self.patrol_range = patrol_range
        self.direction = random.choice([-1, 1])

    def update(self):
        self.x += self.speed_x
        if self.x < self.patrol_range[0] or self.x > self.patrol_range[1]:
            self.direction *= -1
        self.speed_x = self.direction * 2
        self.animate()

class NewEnemy(Character):  # Novo tipo de inimigo
    def __init__(self, x, y, sprites, patrol_range):
        super().__init__(x, y, sprites)
        self.patrol_range = patrol_range
        self.direction = random.choice([-1, 1])

    def update(self):
        self.x += self.speed_x
        if self.x < self.patrol_range[0] or self.x > self.patrol_range[1]:
            self.direction *= -1
        self.speed_x = self.direction * 3  # Velocidade diferente do inimigo anterior
        self.animate()

# Objetos principais
hero = Hero(WIDTH // 2 - 400, GROUND_LEVEL, HERO_SPRITES) 
enemies = [
    Enemy(200, GROUND_LEVEL, ENEMY_SPRITES, (150, 300)),
    Enemy(500, GROUND_LEVEL, ENEMY_SPRITES, (450, 650)),
    NewEnemy(300, GROUND_LEVEL, NEW_ENEMY_SPRITES, (250, 400)),  # Novo inimigo adicionado
]

# Estados do jogo
current_screen = "menu"
sounds_enabled = True

# Funções auxiliares
def draw_menu():
    screen.clear()
    screen.blit(BACKGROUND_IMAGE, (0, 0))

    # Desenhar a borda manualmente usando retângulos (simulando linhas)
    border_rect = Rect(WIDTH // 2 - 200, HEIGHT // 2 - 100, 400, 300)
    
    # Desenhando as bordas do retângulo (simulando a espessura)
    screen.draw.rect(Rect(border_rect.topleft, (border_rect.width, 5)), (255, 255, 255))  # Top
    screen.draw.rect(Rect((border_rect.left, border_rect.top), (5, border_rect.height)), (255, 255, 255))  # Left
    screen.draw.rect(Rect((border_rect.right - 5, border_rect.top), (5, border_rect.height)), (255, 255, 255))  # Right
    screen.draw.rect(Rect((border_rect.left, border_rect.bottom - 5), (border_rect.width, 5)), (255, 255, 255))  # Bottom

    # Texto do menu
    screen.draw.text("Surviving the Apocalypse", center=(WIDTH // 2, HEIGHT // 4), fontsize=50, color="black")
    screen.draw.text("1. Start Game", center=(WIDTH // 2, HEIGHT // 2), fontsize=40, color="black")
    screen.draw.text("2. Toggle Music (On/Off)", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=40, color="black")
    screen.draw.text("3. Exit", center=(WIDTH // 2, HEIGHT // 2 + 100), fontsize=40, color="black")

def draw_game():
    screen.clear()
    screen.blit(BACKGROUND_IMAGE, (0, 0))

    screen.draw.filled_rect(Rect((0, GROUND_LEVEL + 10), (WIDTH, HEIGHT - GROUND_LEVEL)), (100, 200, 100))  # Grama

    hero.draw()
    for enemy in enemies:
        enemy.draw()

def update_game():
    hero.update()
    for enemy in enemies:
        enemy.update()

def toggle_music():
    global MUSIC_ON
    if MUSIC_ON:
        music.stop()
    else:
        music.play("background")
    MUSIC_ON = not MUSIC_ON

# Eventos de teclado e mouse
def on_key_down(key):
    if current_screen == "game":
        if key == keys.LEFT:
            hero.speed_x = -5
        elif key == keys.RIGHT:
            hero.speed_x = 5
        elif key == keys.SPACE and hero.on_ground:
            hero.speed_y = -15  

def on_key_up(key):
    if current_screen == "game":
        if key in (keys.LEFT, keys.RIGHT):
            hero.speed_x = 0

def on_mouse_down(pos):
    global current_screen
    if current_screen == "menu":
        if HEIGHT // 2 - 20 < pos[1] < HEIGHT // 2 + 20:
            current_screen = "game"
            if MUSIC_ON:
                music.play("background")
        elif HEIGHT // 2 + 30 < pos[1] < HEIGHT // 2 + 70:
            toggle_music()
        elif HEIGHT // 2 + 80 < pos[1] < HEIGHT // 2 + 120:
            exit()

# Funções principais
def update():
    if current_screen == "game":
        update_game()

def draw():
    if current_screen == "menu":
        draw_menu()
    elif current_screen == "game":
        draw_game()

# Inicia o jogo
pgzrun.go()
