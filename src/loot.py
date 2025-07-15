from image import *
import math


# 武器掉落类
class WeaponDrop:
    def __init__(self, x, y, weapon_type):
        self.x = x
        self.y = y
        self.weapon_type = weapon_type
        self.radius = 15
        self.color = (50, 205, 50) if weapon_type != "Knife" else (30, 144, 255)
        self.icon = None

        # 加载图标
        if weapon_type == "Shotgun":
            self.icon = load_image("shotgun_icon", (20, 20))
        elif weapon_type == "Rifle":
            self.icon = load_image("rifle_icon", (25, 15))
        # elif weapon_type == "Rocket Launcher":
        #     self.icon = load_image("rocket_icon", (20, 20))
        elif weapon_type == "Knife":
            self.icon = load_image("knife_icon", (20, 20))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

        # 绘制武器图标
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
