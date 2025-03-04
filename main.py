# Сбор предметов (Collect Items)
# Механика: Перемещайте персонажа, собирайте предметы, чтобы завершить уровень.

import pygame
import random
import os

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collect Items")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Звуки
pygame.mixer.init()
collect_sound = pygame.mixer.Sound("collect.wav")  # Звук сбора предмета
level_up_sound = pygame.mixer.Sound("243432342.mp3")  # Звук перехода на новый уровень

# Загрузка спрайтов
player_image = pygame.image.load("player.png")
item_image = pygame.image.load("item.png")
player_image = pygame.transform.scale(player_image, (50, 50))
item_image = pygame.transform.scale(item_image, (30, 30))

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 5
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= 5
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += 5

# Класс предмета
class Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = item_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)

# Группы спрайтов
all_sprites = pygame.sprite.Group()
items = pygame.sprite.Group()

# Создание игрока
player = Player()
all_sprites.add(player)

# Уровни
current_level = 1
items_to_collect = 5
score = 0

# Шрифт
font = pygame.font.Font(None, 36)

# Функция для создания предметов
def create_items(count):
    for _ in range(count):
        item = Item()
        all_sprites.add(item)
        items.add(item)

# Создание предметов для первого уровня
create_items(items_to_collect)

# Основной цикл
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление спрайтов
    all_sprites.update()

    # Проверка сбора предметов
    collected_items = pygame.sprite.spritecollide(player, items, True)
    for item in collected_items:
        collect_sound.play()
        score += 1

    # Проверка завершения уровня
    if len(items) == 0:
        level_up_sound.play()
        current_level += 1
        items_to_collect += 2  # Увеличиваем количество предметов на следующем уровне
        create_items(items_to_collect)

    # Отрисовка
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Отображение счёта и уровня
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {current_level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()