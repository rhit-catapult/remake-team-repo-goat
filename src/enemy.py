import math

import pygame

from constant import *
import os
import pygame
from image import *  # 确保导入image模块



# 敌人类
class Enemy:
    def __init__(self, x, y, enemy_type="normal"):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type

        # 根据敌人类型设置属性
        if enemy_type == "normal":
            self.radius = 18
            self.speed = 2
            self.health = 40
            self.damage = 15
            self.color = (220, 20, 60)  # 红色
            self.score_value = 50
        elif enemy_type == "fast":
            self.radius = 15
            self.speed = 5
            self.health = 50
            self.damage = 10
            self.color = (255, 105, 180)  # 粉红色
            self.score_value = 75
        elif enemy_type == "tank":
            self.radius = 25
            self.speed = 2
            self.health = 150
            self.damage = 20
            self.color = (139, 0, 0)  # 深红色
            self.score_value = 150
        elif enemy_type == "sniper":
            self.radius = 16
            self.speed = 2
            self.health = 80
            self.damage = 40
            self.color = (0, 191, 255)  # 深天蓝
            self.score_value = 100
        elif enemy_type == "boss":
            self.radius = 85

            self.speed = 3
            self.health = 800
            self.damage = 60
            self.color = (128, 0, 128)  # 紫色
            self.score_value = 500

        self.max_health = self.health
        self.attack_cooldown = 0
        self.direction = 0
        self.attack_range = 250 if enemy_type == "sniper" else 150
        # self.boss_head_image = None
        # if enemy_type == "boss":
        #     try:
        #         # 加载BOSS头像
        #         self.boss_head_image = load_image("123456.png", (int(self.radius * 1.8), int(self.radius * 1.8)))
        #     except Exception as e:
        #
        #         print(f"无法加载BOSS头像: {e}")
        #         self.boss_head_image = None
        self.boss_head_image = None
        if enemy_type == "boss":
            try:
                # 加载BOSS头像并创建圆形掩码
                size = (int(self.radius * 2), int(self.radius * 2))

                # 1. 加载原始图像
                original_image = pygame.image.load("123456.png").convert_alpha()
                original_image = pygame.transform.scale(original_image, size)

                # 2. 创建圆形掩码表面
                mask_surface = pygame.Surface(size, pygame.SRCALPHA)
                pygame.draw.circle(
                    mask_surface,
                    (255, 255, 255, 255),  # 白色不透明
                    (size[0] // 2, size[1] // 2),  # 圆心位置
                    size[0] // 2  # 半径
                )

                # 3. 应用圆形掩码
                self.boss_head_image = pygame.Surface(size, pygame.SRCALPHA)
                self.boss_head_image.blit(original_image, (0, 0))
                self.boss_head_image.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            except Exception as e:
                print(f"无法加载BOSS头像: {e}")
                self.boss_head_image = None

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # image1 = pygame.image.load("123456.png")
        # image1 = pygame.transform.scale(image1, (int(self.x), int(self.y)))

        #如果是BOSS且有头像图片，绘制头像
        if self.enemy_type == "boss" and self.boss_head_image:
            # 计算头像位置（居中）
            img_rect = self.boss_head_image.get_rect()
            img_rect.center = (int(self.x), int(self.y))
            screen.blit(self.boss_head_image, img_rect)
        else:

         # 绘制敌人眼睛（方向指示）
         dx = math.cos(math.radians(self.direction))
         dy = -math.sin(math.radians(self.direction))
         eye_x = self.x + dx * self.radius * 0.6
         eye_y = self.y + dy * self.radius * 0.6
         pygame.draw.circle(screen, (30, 30, 30), (int(eye_x), int(eye_y)), self.radius // 3)

        # 绘制生命值条
         pygame.draw.rect(screen, (100, 100, 100), (self.x - self.radius, self.y - self.radius - 10, self.radius * 2, 5))
         pygame.draw.rect(screen, HEALTH_BAR, (self.x - self.radius, self.y - self.radius - 10,
                                              self.radius * 2 * (self.health / self.max_health), 5))

        # 如果是狙击手，绘制瞄准线
         if self.enemy_type == "sniper" and self.attack_cooldown > 30:
             player_pos = (self.target_x, self.target_y)
             pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), player_pos, 2)

    def move_towards_player(self, player_x, player_y, walls):
        dx = player_x - self.x
        dy = player_y - self.y
        distance = max(1, math.sqrt(dx * dx + dy * dy))

        self.direction = math.degrees(math.atan2(-dy, dx))

        # 计算移动向量
        move_x = (dx / distance) * self.speed
        move_y = (dy / distance) * self.speed

        # 分别处理X轴和Y轴的移动
        if move_x != 0:
            self.move_single_axis(move_x, 0, walls)
        if move_y != 0:
            self.move_single_axis(0, move_y, walls)

    def move_single_axis(self, dx, dy, walls):
        # 计算新位置
        new_x = self.x + dx
        new_y = self.y + dy

        # 创建敌人矩形用于碰撞检测
        enemy_rect = pygame.Rect(new_x - self.radius, new_y - self.radius,
                                 self.radius * 2, self.radius * 2)

        # 检查墙壁碰撞
        for wall in walls:
            if enemy_rect.colliderect(wall.rect):
                # 如果碰撞，不移动
                return

        # 边界检查
        if self.radius <= new_x <= WIDTH - self.radius:
            self.x = new_x
        if self.radius <= new_y <= HEIGHT - self.radius:
            self.y = new_y

    def can_attack(self, player_x, player_y):
        if self.enemy_type == "sniper":
            # 狙击手需要瞄准时间
            if self.attack_cooldown == 0:
                self.target_x = player_x
                self.target_y = player_y
                self.attack_cooldown = 90  # 1.5秒瞄准时间
                return False
            elif self.attack_cooldown == 1:
                return True

        if self.attack_cooldown <= 0:
            # 检查玩家是否在攻击范围内
            dx = player_x - self.x
            dy = player_y - self.y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < self.attack_range:
                self.attack_cooldown = 60  # 1秒冷却
                return True
        return False

    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0
