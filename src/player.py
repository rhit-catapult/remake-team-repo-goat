from constant import *
import math
import image
import pygame
import bullet

# 玩家类（优化移动系统）
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.direction = 0  # 角度，0表示向右
        self.weapons = ["Pistol", "Knife"]
        self.current_weapon = 0
        self.ammo = {
            "Pistol": 12,
            "Shotgun": 6,
            "Rifle": 30,
            "Rocket Launcher": 2,
            "Knife": float('inf')  # 无限弹药
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
        self.reload_duration = 60  # 60帧，约1秒
        self.score = 0
        self.melee_attacking = False
        self.melee_time = 0
        self.melee_duration = 10  # 近战攻击持续时间
        self.melee_range = 25  # 近战攻击范围
        self.melee_damage = 10  # 近战伤害
        self.kills = 0
        self.weapon_icons = {
            "Pistol": image.load_image("pistol", (40, 30)),
            "Shotgun": image.load_image("shotgun", (50, 30)),
            "Rifle": image.load_image("rifle", (50, 20)),
            "Rocket Launcher": image.load_image("rocket", (50, 30)),
            "Knife": image.load_image("knife", (40, 40))
        }
        # 移动状态
        self.moving = {"up": False, "down": False, "left": False, "right": False}

    def draw(self, screen):
        # 绘制玩家身体
        pygame.draw.circle(screen, PLAYER_COLOR, (self.x, self.y), self.radius)

        # 绘制玩家方向指示器
        end_x = self.x + (self.radius + 10) * math.cos(math.radians(self.direction))
        end_y = self.y - (self.radius + 10) * math.sin(math.radians(self.direction))
        pygame.draw.line(screen, (30, 30, 30), (self.x, self.y), (end_x, end_y), 4)

        # 绘制当前武器
        font = pygame.font.SysFont(None, 24)
        weapon = self.weapons[self.current_weapon]

        # 绘制弹药（如果是近战武器则不显示弹药）
        if weapon != "Knife":
            ammo_text = font.render(f"Ammo: {self.ammo[weapon]}/{self.max_ammo[weapon]}", True, TEXT_COLOR)
            screen.blit(ammo_text, (self.x - 30, self.y - 70))

        # 绘制生命值条
        pygame.draw.rect(screen, (100, 100, 100), (self.x - 30, self.y - 90, 60, 10))
        pygame.draw.rect(screen, HEALTH_BAR, (self.x - 30, self.y - 90, 60 * (self.health / self.max_health), 10))

        # 如果正在换弹，显示换弹进度
        if self.reloading:
            reload_width = 40 * (1 - self.reload_time / self.reload_duration)
            pygame.draw.rect(screen, (100, 100, 100), (self.x - 20, self.y + 30, 40, 5))
            pygame.draw.rect(screen, AMMO_BAR, (self.x - 20, self.y + 30, reload_width, 5))

        # 绘制近战攻击效果
        if self.melee_attacking:
            angle_rad = math.radians(self.direction)
            start_x = self.x + self.radius * math.cos(angle_rad)
            start_y = self.y - self.radius * math.sin(angle_rad)
            end_x = start_x + self.melee_range * math.cos(angle_rad)
            end_y = start_y - self.melee_range * math.sin(angle_rad)

            # 根据攻击进度调整颜色
            alpha = int(200 * (1 - self.melee_time / self.melee_duration))
            color = (MELEE_COLOR[0], MELEE_COLOR[1], MELEE_COLOR[2], alpha)

            # 创建临时surface绘制半透明线条
            attack_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.line(attack_surf, color, (start_x, start_y), (end_x, end_y), 8)
            screen.blit(attack_surf, (0, 0))

    def update_movement(self, walls):
        # 计算移动向量
        dx, dy = 0, 0

        # 根据移动状态计算方向
        if self.moving["up"]:
            dy -= self.speed
        if self.moving["down"]:
            dy += self.speed
        if self.moving["left"]:
            dx -= self.speed
        if self.moving["right"]:
            dx += self.speed

        # 分别处理X轴和Y轴的移动
        if dx != 0:
            self.move_single_axis(dx, 0, walls)
        if dy != 0:
            self.move_single_axis(0, dy, walls)

    def move_single_axis(self, dx, dy, walls):
        # 计算新位置
        new_x = self.x + dx
        new_y = self.y + dy

        # 创建玩家矩形用于碰撞检测
        player_rect = pygame.Rect(new_x - self.radius, new_y - self.radius,
                                  self.radius * 2, self.radius * 2)

        # 检查墙壁碰撞
        for wall in walls:
            if player_rect.colliderect(wall.rect):
                # 如果碰撞，不移动
                return

        # 边界检查
        if self.radius <= new_x <= WIDTH - self.radius:
            self.x = new_x
        if self.radius <= new_y <= HEIGHT - self.radius:
            self.y = new_y

    def rotate(self, mouse_pos):
        dx = mouse_pos[0] - self.x
        dy = self.y - mouse_pos[1]
        self.direction = math.degrees(math.atan2(dy, dx))

    def shoot(self, bullets, enemies, walls):
        if self.reloading:
            return False

        weapon = self.weapons[self.current_weapon]

        # 近战攻击处理
        if weapon == "Knife":
            if not self.melee_attacking:
                self.melee_attacking = True
                self.melee_time = 0

                # 检测近战攻击范围内的敌人
                angle_rad = math.radians(self.direction)
                start_x = self.x + self.radius * math.cos(angle_rad)
                start_y = self.y - self.radius * math.sin(angle_rad)
                end_x = start_x + self.melee_range * math.cos(angle_rad)
                end_y = start_y - self.melee_range * math.sin(angle_rad)

                # 检测击中的敌人
                for enemy in enemies[:]:
                    # 简单距离检测
                    dx = enemy.x - self.x
                    dy = enemy.y - self.y
                    distance = math.sqrt(dx * dx + dy * dy)

                    # 检查敌人是否在攻击方向和范围内
                    if distance < self.radius + enemy.radius + self.melee_range:
                        # 计算角度差
                        angle_to_enemy = math.degrees(math.atan2(-dy, dx))
                        angle_diff = abs((self.direction - angle_to_enemy + 180) % 360 - 180)

                        if angle_diff < 45:  # 45度锥形攻击范围
                            if enemy.take_damage(self.melee_damage):
                                self.kills += 1
                                enemies.remove(enemy)
                return True

        # 远程武器处理
        if self.ammo[weapon] > 0:
            self.ammo[weapon] -= 1

            # 根据武器类型创建子弹
            if weapon == "Pistol":
                bullets.append(bullet.Bullet(self.x, self.y, self.direction, 10, 5, "Pistol", walls))
            elif weapon == "Shotgun":
                for angle_offset in [-10, 0, 10]:
                    bullets.append(
                        bullet.Bullet(self.x, self.y, self.direction + angle_offset, 8, 12, "Shotgun", walls))
            elif weapon == "Rifle":
                bullets.append(bullet.Bullet(self.x, self.y, self.direction, 25, 10, "Rifle", walls))
            elif weapon == "Rocket Launcher":
                bullets.append(
                    bullet.Bullet(self.x, self.y, self.direction, 5, 30, "Rocket Launcher", walls, is_explosive=True))

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
        # 更新换弹状态
        if self.reloading:
            self.reload_time += 1
            if self.reload_time >= self.reload_duration:
                weapon = self.weapons[self.current_weapon]
                self.ammo[weapon] = self.max_ammo[weapon]
                self.reloading = False

        # 更新近战攻击状态
        if self.melee_attacking:
            self.melee_time += 1
            if self.melee_time >= self.melee_duration:
                self.melee_attacking = False

    def switch_weapon(self, index):
        if index < len(self.weapons):
            self.current_weapon = index

    def add_weapon(self, weapon_name):
        if weapon_name not in self.weapons:
            self.weapons.append(weapon_name)
            self.ammo[weapon_name] = self.max_ammo[weapon_name]
            self.current_weapon = len(self.weapons) - 1
