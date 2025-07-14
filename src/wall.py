import pygame

from constant import *


# 墙壁/障碍物类
class Wall:
    def __init__(self, x, y, width, height, wall_type="normal"):
        self.rect = pygame.Rect(x, y, width, height)
        self.wall_type = wall_type
        self.color = WALL_COLOR

        # 根据墙壁类型设置不同颜色
        if wall_type == "breakable":
            self.color = (139, 69, 19)  # 棕色
        elif wall_type == "metal":
            self.color = (169, 169, 169)  # 灰色

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (70, 70, 70), self.rect, 2)
