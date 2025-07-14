import pygame
import sys
import random
import math
import os


pygame.init()


WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game -- GOAT Studio")


BACKGROUND = (40, 44, 52)
PLAYER_COLOR = (70, 130, 180)
ENEMY_COLOR = (220, 20, 60)
BULLET_COLOR = (255, 215, 0)
WALL_COLOR = (100, 100, 100)
TEXT_COLOR = (220, 220, 220)
HEALTH_BAR = (50, 205, 50)
AMMO_BAR = (255, 140, 0)
WEAPON_HIGHLIGHT = (0, 191, 255)
MELEE_COLOR = (30, 144, 255)



def load_image(name, size=None):
    try:
        image = pygame.image.load(f"{name}.png")
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except:

        surf = pygame.Surface((size or (50, 50)))
        surf.fill((100, 100, 100))
        pygame.draw.rect(surf, (150, 150, 150), surf.get_rect(), 2)
        font = pygame.font.SysFont(None, 20)
        text = font.render(name, True, (255, 255, 255))
        surf.blit(text, (surf.get_width() // 2 - text.get_width() // 2,
                         surf.get_height() // 2 - text.get_height() // 2))
        return surf



class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.direction = 0
        self.weapons = ["Pistol", "Knife"]
        self.current_weapon = 0
        self.ammo = {
            "Pistol": 12,
            "Shotgun": 6,
            "Rifle": 30,
            "Rocket Launcher": 2,
            "Knife": float('inf')
        }
        self.max_ammo = {
            "Pistol": 12,
            "Shotgun": 6,
            "Rifle": 30,
            "Rocket Launcher": 2,
            "Knife": float('inf')
        }
        self.reloading = False
        self.reload_time = 0
        self.reload_duration = 60
        self.score = 0
        self.melee_attacking = False
        self.melee_time = 0
        self.melee_duration = 20
        self.melee_range = 50
        self.melee_damage = 25
        self.kills = 0
        self.weapon_icons = {
            "Pistol": load_image("pistol", (40, 30)),
            "Shotgun": load_image("shotgun", (50, 30)),
            "Rifle": load_image("rifle", (50, 20)),
            "Rocket Launcher": load_image("rocket", (50, 30)),
            "Knife": load_image("knife", (40, 40))
        }

        self.moving = {"up": False, "down": False, "left": False, "right": False}

    def draw(self, screen):

        pygame.draw.circle(screen, PLAYER_COLOR, (self.x, self.y), self.radius)


        end_x = self.x + (self.radius + 10) * math.cos(math.radians(self.direction))
        end_y = self.y - (self.radius + 10) * math.sin(math.radians(self.direction))
        pygame.draw.line(screen, (30, 30, 30), (self.x, self.y), (end_x, end_y), 4)


        font = pygame.font.SysFont(None, 24)
        weapon = self.weapons[self.current_weapon]


        if weapon != "Knife":
            ammo_text = font.render(f"Ammo: {self.ammo[weapon]}/{self.max_ammo[weapon]}", True, TEXT_COLOR)
            screen.blit(ammo_text, (self.x - 30, self.y - 70))


        pygame.draw.rect(screen, (100, 100, 100), (self.x - 30, self.y - 90, 60, 10))
        pygame.draw.rect(screen, HEALTH_BAR, (self.x - 30, self.y - 90, 60 * (self.health / self.max_health), 10))


        if self.reloading:
            reload_width = 40 * (1 - self.reload_time / self.reload_duration)
            pygame.draw.rect(screen, (100, 100, 100), (self.x - 20, self.y + 30, 40, 5))
            pygame.draw.rect(screen, AMMO_BAR, (self.x - 20, self.y + 30, reload_width, 5))


        if self.melee_attacking:
            angle_rad = math.radians(self.direction)
            start_x = self.x + self.radius * math.cos(angle_rad)
            start_y = self.y - self.radius * math.sin(angle_rad)
            end_x = start_x + self.melee_range * math.cos(angle_rad)
            end_y = start_y - self.melee_range * math.sin(angle_rad)


            alpha = int(200 * (1 - self.melee_time / self.melee_duration))
            color = (MELEE_COLOR[0], MELEE_COLOR[1], MELEE_COLOR[2], alpha)


            attack_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.line(attack_surf, color, (start_x, start_y), (end_x, end_y), 8)
            screen.blit(attack_surf, (0, 0))

    def update_movement(self, walls):

        dx, dy = 0, 0


        if self.moving["up"]:
            dy -= 1
        if self.moving["down"]:
            dy += 1
        if self.moving["left"]:
            dx -= 1
        if self.moving["right"]:
            dx += 1


        if dx != 0 and dy != 0:
            dx *= 0.7071  # 1/sqrt(2)
            dy *= 0.7071


        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed


        player_rect = pygame.Rect(new_x - self.radius, new_y - self.radius,
                                  self.radius * 2, self.radius * 2)


        collision_x, collision_y = False, False

        for wall in walls:
            if player_rect.colliderect(wall.rect):

                test_rect_x = pygame.Rect(new_x - self.radius, self.y - self.radius,
                                          self.radius * 2, self.radius * 2)
                if not test_rect_x.colliderect(wall.rect):
                    new_y = self.y
                else:

                    test_rect_y = pygame.Rect(self.x - self.radius, new_y - self.radius,
                                              self.radius * 2, self.radius * 2)
                    if not test_rect_y.colliderect(wall.rect):
                        new_x = self.x
                    else:

                        new_x, new_y = self.x, self.y


        if 30 <= new_x <= WIDTH - 30:
            self.x = new_x
        if 30 <= new_y <= HEIGHT - 30:
            self.y = new_y

    def rotate(self, mouse_pos):
        dx = mouse_pos[0] - self.x
        dy = self.y - mouse_pos[1]
        self.direction = math.degrees(math.atan2(dy, dx))

    def shoot(self, bullets, enemies, walls):
        if self.reloading:
            return False

        weapon = self.weapons[self.current_weapon]


        if weapon == "Knife":
            if not self.melee_attacking:
                self.melee_attacking = True
                self.melee_time = 0


                angle_rad = math.radians(self.direction)
                start_x = self.x + self.radius * math.cos(angle_rad)
                start_y = self.y - self.radius * math.sin(angle_rad)
                end_x = start_x + self.melee_range * math.cos(angle_rad)
                end_y = start_y - self.melee_range * math.sin(angle_rad)


                attack_line = pygame.Rect(min(start_x, end_x) - 10, min(start_y, end_y) - 10,
                                          abs(end_x - start_x) + 20, abs(end_y - start_y) + 20)


                for enemy in enemies[:]:
                    enemy_rect = pygame.Rect(enemy.x - enemy.radius, enemy.y - enemy.radius,
                                             enemy.radius * 2, enemy.radius * 2)


                    dx = enemy.x - self.x
                    dy = enemy.y - self.y
                    distance = math.sqrt(dx * dx + dy * dy)


                    if distance < self.radius + enemy.radius + self.melee_range:

                        angle_to_enemy = math.degrees(math.atan2(-dy, dx))
                        angle_diff = abs((self.direction - angle_to_enemy + 180) % 360 - 180)

                        if angle_diff < 45:
                            if enemy.take_damage(self.melee_damage):
                                self.kills += 1
                                enemies.remove(enemy)
                return True


        if self.ammo[weapon] > 0:
            self.ammo[weapon] -= 1


            if weapon == "Pistol":
                bullets.append(Bullet(self.x, self.y, self.direction, 10, 20, "Pistol", walls))
            elif weapon == "Shotgun":
                for angle_offset in [-10, 0, 10]:
                    bullets.append(Bullet(self.x, self.y, self.direction + angle_offset, 8, 15, "Shotgun", walls))
            elif weapon == "Rifle":
                bullets.append(Bullet(self.x, self.y, self.direction, 15, 15, "Rifle", walls))
            elif weapon == "Rocket Launcher":
                bullets.append(
                    Bullet(self.x, self.y, self.direction, 5, 30, "Rocket Launcher", walls, is_explosive=True))

            return True
        return False

    def reload(self):
        weapon = self.weapons[self.current_weapon]
        if weapon == "Knife":
            return

        if not self.reloading and self.ammo[weapon] < self.max_ammo[weapon]:
            self.reloading = True
            self.reload_time = 0

    def update(self):

        if self.reloading:
            self.reload_time += 1
            if self.reload_time >= self.reload_duration:
                weapon = self.weapons[self.current_weapon]
                self.ammo[weapon] = self.max_ammo[weapon]
                self.reloading = False


        if self.melee_attacking:
            self.melee_time += 1
            if self.melee_time >= self.melee_duration:
                self.melee_attacking = False

    def switch_weapon(self, direction):
        new_index = (self.current_weapon + direction) % len(self.weapons)
        self.current_weapon = new_index

    def add_weapon(self, weapon_name):
        if weapon_name not in self.weapons:
            self.weapons.append(weapon_name)
            self.ammo[weapon_name] = self.max_ammo[weapon_name]
            self.current_weapon = len(self.weapons) - 1



class Bullet:
    def __init__(self, x, y, direction, speed, damage, weapon_type, walls, is_explosive=False):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.radius = 4
        self.weapon_type = weapon_type
        self.is_explosive = is_explosive
        self.explosion_radius = 60 if is_explosive else 0
        self.lifetime = 120
        self.walls = walls


        if weapon_type == "Pistol":
            self.color = (255, 215, 0)
        elif weapon_type == "Shotgun":
            self.color = (255, 140, 0)
        elif weapon_type == "Rifle":
            self.color = (50, 205, 50)
        elif weapon_type == "Rocket Launcher":
            self.color = (255, 0, 0)

    def move(self):
        rad = math.radians(self.direction)
        dx = self.speed * math.cos(rad)
        dy = -self.speed * math.sin(rad)


        new_x = self.x + dx
        new_y = self.y + dy

        bullet_rect = pygame.Rect(new_x - self.radius, new_y - self.radius,
                                  self.radius * 2, self.radius * 2)

        hit_wall = False
        for wall in self.walls:
            if bullet_rect.colliderect(wall.rect):
                hit_wall = True
                break

        if not hit_wall:
            self.x = new_x
            self.y = new_y
        else:
            self.lifetime = 0  #

        self.lifetime -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        if self.is_explosive:
            pygame.draw.circle(screen, (255, 100, 0), (int(self.x), int(self.y)), self.radius + 2, 1)

    def is_out_of_bounds(self):
        return (self.x < 0 or self.x > WIDTH or
                self.y < 0 or self.y > HEIGHT or
                self.lifetime <= 0)



class Enemy:
    def __init__(self, x, y, enemy_type="normal"):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type


        if enemy_type == "normal":
            self.radius = 18
            self.speed = 2
            self.health = 30
            self.damage = 10
            self.color = (220, 20, 60)
            self.score_value = 50
        elif enemy_type == "fast":
            self.radius = 15
            self.speed = 3.5
            self.health = 20
            self.damage = 5
            self.color = (255, 105, 180)
            self.score_value = 75
        elif enemy_type == "tank":
            self.radius = 25
            self.speed = 1.2
            self.health = 80
            self.damage = 20
            self.color = (139, 0, 0)
            self.score_value = 150
        elif enemy_type == "sniper":
            self.radius = 16
            self.speed = 1.8
            self.health = 25
            self.damage = 35
            self.color = (0, 191, 255)
            self.score_value = 100
        elif enemy_type == "boss":
            self.radius = 40
            self.speed = 1.5
            self.health = 200
            self.damage = 30
            self.color = (128, 0, 128)
            self.score_value = 500

        self.max_health = self.health
        self.attack_cooldown = 0
        self.direction = 0
        self.attack_range = 250 if enemy_type == "sniper" else 150

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


        dx = math.cos(math.radians(self.direction))
        dy = -math.sin(math.radians(self.direction))
        eye_x = self.x + dx * self.radius * 0.6
        eye_y = self.y + dy * self.radius * 0.6
        pygame.draw.circle(screen, (30, 30, 30), (int(eye_x), int(eye_y)), self.radius // 3)


        pygame.draw.rect(screen, (100, 100, 100), (self.x - self.radius, self.y - self.radius - 10, self.radius * 2, 5))
        pygame.draw.rect(screen, HEALTH_BAR, (self.x - self.radius, self.y - self.radius - 10,
                                              self.radius * 2 * (self.health / self.max_health), 5))


        if self.enemy_type == "sniper" and self.attack_cooldown > 30:
            player_pos = (self.target_x, self.target_y)
            pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), player_pos, 2)

    def move_towards_player(self, player_x, player_y, walls):
        dx = player_x - self.x
        dy = player_y - self.y
        distance = max(1, math.sqrt(dx * dx + dy * dy))

        self.direction = math.degrees(math.atan2(-dy, dx))

        move_x = (dx / distance) * self.speed
        move_y = (dy / distance) * self.speed

        new_x = self.x + move_x
        new_y = self.y + move_y


        enemy_rect = pygame.Rect(new_x - self.radius, new_y - self.radius,
                                 self.radius * 2, self.radius * 2)


        can_move = True
        for wall in walls:
            if enemy_rect.colliderect(wall.rect):
                can_move = False
                break

        if can_move and distance > self.radius + 20:
            self.x = new_x
            self.y = new_y
        elif distance < self.radius + 20:
            self.x -= move_x * 0.5
            self.y -= move_y * 0.5

    def can_attack(self, player_x, player_y):
        if self.enemy_type == "sniper":

            if self.attack_cooldown == 0:
                self.target_x = player_x
                self.target_y = player_y
                self.attack_cooldown = 90
                return False
            elif self.attack_cooldown == 1:
                return True

        if self.attack_cooldown <= 0:

            dx = player_x - self.x
            dy = player_y - self.y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < self.attack_range:
                self.attack_cooldown = 60
                return True
        return False

    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0



class WeaponDrop:
    def __init__(self, x, y, weapon_type):
        self.x = x
        self.y = y
        self.weapon_type = weapon_type
        self.radius = 15
        self.color = (50, 205, 50) if weapon_type != "Knife" else (30, 144, 255)
        self.icon = None


        if weapon_type == "Shotgun":
            self.icon = load_image("shotgun_icon", (20, 20))
        elif weapon_type == "Rifle":
            self.icon = load_image("rifle_icon", (25, 15))
        elif weapon_type == "Rocket Launcher":
            self.icon = load_image("rocket_icon", (20, 20))
        elif weapon_type == "Knife":
            self.icon = load_image("knife_icon", (20, 20))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


        if self.icon:
            screen.blit(self.icon, (self.x - self.icon.get_width() // 2,
                                    self.y - self.icon.get_height() // 2))
        else:
            font = pygame.font.SysFont(None, 24)
            text = font.render(self.weapon_type[0], True, (255, 255, 255))
            screen.blit(text, (self.x - text.get_width() // 2, self.y - text.get_height() // 2))

    def check_collision(self, player):
        dx = self.x - player.x
        dy = self.y - player.y
        distance = math.sqrt(dx * dx + dy * dy)
        return distance < (self.radius + player.radius)



class Wall:
    def __init__(self, x, y, width, height, wall_type="normal"):
        self.rect = pygame.Rect(x, y, width, height)
        self.wall_type = wall_type
        self.color = WALL_COLOR


        if wall_type == "breakable":
            self.color = (139, 69, 19)
        elif wall_type == "metal":
            self.color = (169, 169, 169)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (70, 70, 70), self.rect, 2)



class Level:
    def __init__(self, level_num):
        self.level_num = level_num
        self.walls = []
        self.enemies = []
        self.initial_player_pos = (WIDTH // 2, HEIGHT // 2)
        self.weapon_drops = []


        if level_num == 1:
            self._create_level_1()
        elif level_num == 2:
            self._create_level_2()
        elif level_num == 3:
            self._create_level_3()
        elif level_num == 4:
            self._create_level_4()
        else:
            self._create_final_level()

    def _create_level_1(self):

        self.walls = [
            Wall(200, 150, 100, 30, "normal"),
            Wall(400, 300, 30, 200, "normal"),
            Wall(600, 100, 200, 30, "normal"),
            Wall(700, 400, 100, 30, "normal"),
            Wall(150, 500, 300, 30, "normal"),
            Wall(800, 200, 30, 150, "normal"),
        ]


        self.enemies = [
            Enemy(300, 300, "normal"),
            Enemy(700, 300, "normal"),
            Enemy(500, 500, "normal")
        ]


        self.weapon_drops = [
            WeaponDrop(200, 200, "Shotgun")
        ]

    def _create_level_2(self):

        self.walls = [
            Wall(100, 100, 50, 300, "normal"),
            Wall(100, 100, 300, 50, "normal"),
            Wall(350, 100, 50, 200, "normal"),
            Wall(200, 250, 200, 50, "normal"),
            Wall(500, 150, 50, 300, "breakable"),
            Wall(650, 150, 200, 50, "normal"),
            Wall(650, 300, 200, 50, "normal"),
            Wall(800, 150, 50, 200, "normal"),
            Wall(200, 450, 400, 50, "normal"),
            Wall(700, 450, 200, 50, "normal"),
        ]


        self.enemies = [
            Enemy(300, 200, "normal"),
            Enemy(400, 400, "fast"),
            Enemy(600, 200, "normal"),
            Enemy(750, 400, "normal"),
            Enemy(500, 350, "sniper")
        ]


        self.weapon_drops = [
            WeaponDrop(600, 400, "Rifle"),
            WeaponDrop(400, 200, "Knife")
        ]

    def _create_level_3(self):

        self.walls = [
            Wall(100, 100, 800, 50, "normal"),  # 顶部
            Wall(100, 550, 800, 50, "normal"),  # 底部
            Wall(100, 100, 50, 500, "normal"),  # 左侧
            Wall(850, 100, 50, 500, "normal"),  # 右侧


            Wall(250, 200, 50, 300, "metal"),
            Wall(700, 200, 50, 300, "metal"),
            Wall(350, 150, 300, 50, "normal"),
            Wall(350, 500, 300, 50, "normal"),
            Wall(450, 250, 100, 200, "breakable"),
        ]


        self.enemies = [
            Enemy(200, 200, "fast"),
            Enemy(200, 500, "fast"),
            Enemy(800, 200, "fast"),
            Enemy(800, 500, "fast"),
            Enemy(500, 300, "tank"),
            Enemy(400, 400, "sniper"),
            Enemy(600, 400, "sniper")
        ]


        self.weapon_drops = [
            WeaponDrop(500, 200, "Rocket Launcher"),
            WeaponDrop(500, 500, "Knife")
        ]

    def _create_level_4(self):

        self.walls = [

            Wall(50, 50, 900, 30, "metal"),
            Wall(50, 50, 30, 600, "metal"),
            Wall(50, 620, 900, 30, "metal"),
            Wall(920, 50, 30, 600, "metal"),


            Wall(150, 150, 200, 30, "normal"),
            Wall(150, 150, 30, 200, "normal"),
            Wall(650, 150, 200, 30, "normal"),
            Wall(820, 150, 30, 200, "normal"),
            Wall(150, 500, 200, 30, "normal"),
            Wall(150, 330, 30, 200, "normal"),
            Wall(650, 500, 200, 30, "normal"),
            Wall(820, 330, 30, 200, "normal"),

            Wall(400, 250, 200, 30, "breakable"),
            Wall(400, 450, 200, 30, "breakable"),
            Wall(350, 300, 30, 150, "breakable"),
            Wall(620, 300, 30, 150, "breakable"),


            Wall(450, 350, 100, 100, "metal")
        ]


        self.enemies = [
            Enemy(200, 200, "tank"),
            Enemy(800, 200, "tank"),
            Enemy(200, 550, "tank"),
            Enemy(800, 550, "tank"),
            Enemy(300, 300, "sniper"),
            Enemy(700, 300, "sniper"),
            Enemy(300, 500, "sniper"),
            Enemy(700, 500, "sniper"),
            Enemy(500, 400, "boss")
        ]


        self.weapon_drops = [
            WeaponDrop(200, 400, "Rocket Launcher"),
            WeaponDrop(800, 400, "Rocket Launcher"),
            WeaponDrop(500, 200, "Rifle")
        ]

    def _create_final_level(self):

        self.walls = [

            Wall(100, 100, 800, 30, "metal"),
            Wall(100, 100, 30, 500, "metal"),
            Wall(100, 570, 800, 30, "metal"),
            Wall(870, 100, 30, 500, "metal"),


            Wall(200, 200, 100, 300, "breakable"),
            Wall(700, 200, 100, 300, "breakable"),
            Wall(350, 150, 300, 50, "normal"),
            Wall(350, 500, 300, 50, "normal"),

            Wall(400, 250, 50, 200, "metal"),
            Wall(550, 250, 50, 200, "metal"),

            Wall(475, 350, 50, 50, "metal")
        ]


        enemy_types = ["normal", "fast", "tank", "sniper"]
        for i in range(12):
            x = random.randint(150, 850)
            y = random.randint(150, 550)

            valid_pos = True
            enemy_rect = pygame.Rect(x - 25, y - 25, 50, 50)
            for wall in self.walls:
                if enemy_rect.colliderect(wall.rect):
                    valid_pos = False
                    break

            if valid_pos:
                enemy_type = random.choice(enemy_types)
                self.enemies.append(Enemy(x, y, enemy_type))


        self.enemies.append(Enemy(500, 350, "boss"))

        self.weapon_drops = [
            WeaponDrop(150, 150, "Rocket Launcher"),
            WeaponDrop(850, 150, "Rocket Launcher"),
            WeaponDrop(150, 550, "Rocket Launcher"),
            WeaponDrop(850, 550, "Rocket Launcher"),
            WeaponDrop(500, 300, "Knife")
        ]



def main():
    clock = pygame.time.Clock()


    player = Player(WIDTH // 2, HEIGHT // 2)


    current_level = 1
    level = Level(current_level)
    walls = level.walls
    enemies = level.enemies
    weapon_drops = level.weapon_drops
    player.x, player.y = level.initial_player_pos


    bullets = []


    game_over = False
    level_complete = False
    score = 0
    level_transition_timer = 0


    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.moving["up"] = True
                if event.key == pygame.K_s:
                    player.moving["down"] = True
                if event.key == pygame.K_a:
                    player.moving["left"] = True
                if event.key == pygame.K_d:
                    player.moving["right"] = True

                if event.key == pygame.K_r and not game_over:
                    player.reload()
                if event.key == pygame.K_j and not game_over:
                    player.shoot(bullets, enemies, walls)
                if event.key == pygame.K_q:
                    player.switch_weapon(-1)
                if event.key == pygame.K_e:
                    player.switch_weapon(1)
                if event.key == pygame.K_SPACE and (game_over or level_complete):
                    if game_over:
                        return main()
                    elif level_complete:
                        level_complete = False
                        current_level += 1
                        if current_level > 5:
                            current_level = 1
                        level = Level(current_level)
                        walls = level.walls
                        enemies = level.enemies
                        weapon_drops = level.weapon_drops
                        player.x, player.y = level.initial_player_pos
                        player.health = min(player.max_health, player.health + 30)
                        bullets = []


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.moving["up"] = False
                if event.key == pygame.K_s:
                    player.moving["down"] = False
                if event.key == pygame.K_a:
                    player.moving["left"] = False
                if event.key == pygame.K_d:
                    player.moving["right"] = False

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if event.button == 1:
                    player.shoot(bullets, enemies, walls)

        if game_over:

            screen.fill(BACKGROUND)


            font_large = pygame.font.SysFont(None, 72)
            font_medium = pygame.font.SysFont(None, 48)
            font_small = pygame.font.SysFont(None, 36)

            game_over_text = font_large.render("GAME OVER", True, (220, 20, 60))
            score_text = font_medium.render(f"Final Score: {score}", True, TEXT_COLOR)
            level_text = font_medium.render(f"Reached Level: {current_level}", True, TEXT_COLOR)
            restart_text = font_small.render("Press SPACE to Restart", True, TEXT_COLOR)

            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 150))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))

            pygame.display.flip()
            clock.tick(60)
            continue

        if level_complete:

            screen.fill(BACKGROUND)

            font_large = pygame.font.SysFont(None, 72)
            font_medium = pygame.font.SysFont(None, 48)
            font_small = pygame.font.SysFont(None, 36)

            level_text = font_large.render(f"LEVEL {current_level} COMPLETE!", True, (50, 205, 50))
            score_text = font_medium.render(f"Score: {score}", True, TEXT_COLOR)
            next_text = font_small.render("Press SPACE to Continue to Next Level", True, TEXT_COLOR)

            screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2 - 100))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
            screen.blit(next_text, (WIDTH // 2 - next_text.get_width() // 2, HEIGHT // 2 + 100))

            pygame.display.flip()
            clock.tick(60)
            continue


        mouse_pos = pygame.mouse.get_pos()
        player.rotate(mouse_pos)


        player.update_movement(walls)


        player.update()


        for enemy in enemies[:]:
            enemy.move_towards_player(player.x, player.y, walls)
            enemy.update()


            dx = enemy.x - player.x
            dy = enemy.y - player.y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < enemy.radius + player.radius:
                if enemy.can_attack(player.x, player.y):
                    player.health -= enemy.damage
                    if player.health <= 0:
                        game_over = True
            elif enemy.enemy_type == "sniper" and enemy.attack_cooldown > 0:

                enemy.target_x = player.x
                enemy.target_y = player.y


        for bullet in bullets[:]:
            bullet.move()


            for enemy in enemies[:]:
                dx = bullet.x - enemy.x
                dy = bullet.y - enemy.y
                distance = math.sqrt(dx * dx + dy * dy)

                if distance < bullet.radius + enemy.radius:
                    if bullet.is_explosive:

                        for e in enemies[:]:
                            edx = bullet.x - e.x
                            edy = bullet.y - e.y
                            edist = math.sqrt(edx * edx + edy * edy)
                            if edist < bullet.explosion_radius:
                                if e.take_damage(bullet.damage):
                                    player.kills += 1
                                    score += e.score_value

                                    if random.random() < 0.3 and len(player.weapons) < 5:
                                        weapon_types = ["Shotgun", "Rifle", "Rocket Launcher", "Knife"]
                                        for wt in weapon_types:
                                            if wt not in player.weapons:
                                                weapon_drops.append(WeaponDrop(e.x, e.y, wt))
                                                break
                                    enemies.remove(e)
                        bullets.remove(bullet)
                        break
                    else:
                        if enemy.take_damage(bullet.damage):
                            player.kills += 1
                            score += enemy.score_value

                            if random.random() < 0.3 and len(player.weapons) < 5:
                                weapon_types = ["Shotgun", "Rifle", "Rocket Launcher", "Knife"]
                                for wt in weapon_types:
                                    if wt not in player.weapons:
                                        weapon_drops.append(WeaponDrop(enemy.x, enemy.y, wt))
                                        break
                            enemies.remove(enemy)
                        bullets.remove(bullet)
                        break


            if bullet.is_out_of_bounds():
                bullets.remove(bullet)


        for drop in weapon_drops[:]:
            if drop.check_collision(player):
                player.add_weapon(drop.weapon_type)
                weapon_drops.remove(drop)

        if len(enemies) == 0 and not level_complete:
            level_complete = True


        screen.fill(BACKGROUND)


        for wall in walls:
            wall.draw(screen)


        for drop in weapon_drops:
            drop.draw(screen)


        for bullet in bullets:
            bullet.draw(screen)


        for enemy in enemies:
            enemy.draw(screen)


        player.draw(screen)


        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
        level_text = font.render(f"Level: {current_level}", True, TEXT_COLOR)
        health_text = font.render(f"Health: {player.health}", True, TEXT_COLOR)
        kills_text = font.render(f"Kills: {player.kills}", True, TEXT_COLOR)

        screen.blit(score_text, (20, 20))
        screen.blit(level_text, (20, 60))
        screen.blit(health_text, (20, 100))
        screen.blit(kills_text, (20, 140))


        controls_font = pygame.font.SysFont(None, 24)
        controls = [
            "Controls: WASD - Move, Mouse - Aim, LMB/J - Shoot",
            "R - Reload, Q/E - Switch Weapon, SPACE - Next Level"
        ]

        for i, text in enumerate(controls):
            ctrl_text = controls_font.render(text, True, TEXT_COLOR)
            screen.blit(ctrl_text, (WIDTH - ctrl_text.get_width() - 20, 20 + i * 30))


        weapon_y = HEIGHT - 50
        for i, weapon in enumerate(player.weapons):
            color = WEAPON_HIGHLIGHT if i == player.current_weapon else (100, 100, 100)
            pygame.draw.rect(screen, color, (20 + i * 150, weapon_y, 140, 40))
            pygame.draw.rect(screen, (50, 50, 50), (20 + i * 150, weapon_y, 140, 40), 2)

            weapon_text = controls_font.render(weapon, True, (255, 255, 255))


            if weapon in player.weapon_icons:
                icon = player.weapon_icons[weapon]
                screen.blit(icon, (20 + i * 150 + 70 - icon.get_width() // 2,
                                   weapon_y + 20 - icon.get_height() // 2))
            else:
                screen.blit(weapon_text, (20 + i * 150 + 70 - weapon_text.get_width() // 2, weapon_y + 15))

            if weapon != "Knife":
                ammo_text = controls_font.render(f"{player.ammo[weapon]}/{player.max_ammo[weapon]}", True,
                                                 (255, 255, 255))
                screen.blit(ammo_text, (20 + i * 150 + 70 - ammo_text.get_width() // 2, weapon_y + 25))


        if player.health <= 0:
            game_over = True

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()