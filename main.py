import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Asteroids")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define constants
FPS = 60
ship_acceleration = 0.2
ship_rotation_speed = 4
bullet_speed = 10
asteroid_speed = 2

# Load images
ship_img = pygame.image.load("ship.png")
bullet_img = pygame.image.load("bullet.png")
asteroid_img = pygame.image.load("asteroid.png")

# Scale images
ship_img = pygame.transform.scale(ship_img, (50, 50))
bullet_img = pygame.transform.scale(bullet_img, (10, 10))
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))

# Create the ship class
class Ship:
    def __init__(self):
        self.image = ship_img
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.angle = 0
        self.vel_x = 0
        self.vel_y = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle += ship_rotation_speed
        if keys[pygame.K_RIGHT]:
            self.angle -= ship_rotation_speed
        if keys[pygame.K_UP]:
            self.vel_x += ship_acceleration * math.cos(math.radians(self.angle))
            self.vel_y -= ship_acceleration * math.sin(math.radians(self.angle))

        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        self.vel_x *= 0.99
        self.vel_y *= 0.99

        if self.rect.right < 0:
            self.rect.left = screen_width
        elif self.rect.left > screen_width:
            self.rect.right = 0
        elif self.rect.bottom < 0:
            self.rect.top = screen_height
        elif self.rect.top > screen_height:
            self.rect.bottom = 0

    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)

# Create the bullet class
class Bullet:
    def __init__(self, x, y, angle):
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.angle = angle
        self.vel_x = bullet_speed * math.cos(math.radians(self.angle))
        self.vel_y = -bullet_speed * math.sin(math.radians(self.angle))

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def draw(self):
        screen.blit(self.image, self.rect)

# Create the asteroid class
class Asteroid:
    def __init__(self):
        self.image = asteroid_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width)
        self.rect.y = random.randint(0, screen_height)
        self.angle = random.randint(0, 360)
        self.vel_x = asteroid_speed * math.cos(math.radians(self.angle))
        self.vel_y = -asteroid_speed * math.sin(math.radians(self.angle))

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if self.rect.right < 0:
            self.rect.left = screen_width
        elif self.rect.left > screen_width:
            self.rect.right = 0
        elif self.rect.bottom < 0:
            self.rect.top = screen_height
        elif self.rect.top > screen_height:
            self.rect.bottom = 0

    def draw(self):
        screen.blit(self.image, self.rect)

# Create a list to hold all sprites
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
asteroids = pygame.sprite.Group()

# Create the player's ship
player = Ship()
all_sprites.add(player)

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    # Keep loop running at the right speed
    clock.tick(FPS)

    # Process input/events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.centery, player.angle)
                all_sprites.add(bullet)
                bullets.add(bullet)

    # Update
    all_sprites.update()

    # Check for bullet-asteroid collisions
    hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
    for hit in hits:
        asteroid = Asteroid()
        all_sprites.add(asteroid)
        asteroids.add(asteroid)

    # Check for ship-asteroid collisions
    hits = pygame.sprite.spritecollide(player, asteroids, True)
    if hits:
        running = False

    # Draw/render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

# Quit
pygame.quit()
