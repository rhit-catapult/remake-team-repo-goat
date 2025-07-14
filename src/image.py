import pygame


# 加载图像（如果没有图像文件，使用替代图形）
def load_image(name, size=None):
    try:
        image = pygame.image.load(f"{name}.png")
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except:
        # 创建替代图形
        surf = pygame.Surface((size or (50, 50)))
        surf.fill((100, 100, 100))
        pygame.draw.rect(surf, (150, 150, 150), surf.get_rect(), 2)
        font = pygame.font.SysFont(None, 20)
        text = font.render(name, True, (255, 255, 255))
        surf.blit(text, (surf.get_width() // 2 - text.get_width() // 2,
                         surf.get_height() // 2 - text.get_height() // 2))
        return surf
