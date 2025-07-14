import math

from image import *


# 子弹类
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
        self.lifetime = 120  # 子弹存在时间（帧）
        self.walls = walls

        # 根据武器类型设置子弹颜色
        if weapon_type == "Pistol":
            self.color = (255, 215, 0)  # 金色
        elif weapon_type == "Shotgun":
            self.color = (255, 140, 0)  # 深橙色
        elif weapon_type == "Rifle":
            self.color = (50, 205, 50)  # 酸橙色
        elif weapon_type == "Rocket Launcher":
            self.color = (255, 0, 0)  # 红色

    def move(self):
        rad = math.radians(self.direction)
        dx = self.speed * math.cos(rad)
        dy = -self.speed * math.sin(rad)

        # 检查墙壁碰撞
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
            self.lifetime = 0  # 子弹碰到墙壁消失

        self.lifetime -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        if self.is_explosive:
            pygame.draw.circle(screen, (255, 100, 0), (int(self.x), int(self.y)), self.radius + 2, 1)

    def is_out_of_bounds(self):
        return (self.x < 0 or self.x > WIDTH or
                self.y < 0 or self.y > HEIGHT or
                self.lifetime <= 0)
