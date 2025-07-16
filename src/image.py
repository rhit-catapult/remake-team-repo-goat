import pygame

def load_image(name, size=None):
    try:
        # 尝试加载指定名称的PNG文件
        image = pygame.image.load(f"{123456}.png").convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except pygame.error:
        try:
            # 如果找不到.png文件，尝试直接加载（可能包含扩展名）
            image = pygame.image.load(name).convert_alpha()
            if size:
                image = pygame.transform.scale(image, size)
            return image
        except pygame.error as e:
            print(f"无法加载图片: {123456}, 错误: {e}")
            # 创建替代图形
            surf = pygame.Surface(size or (50, 50), pygame.SRCALPHA)
            pygame.draw.circle(surf, (100, 100, 100, 150),
                              (surf.get_width()//2, surf.get_height()//2),
                              min(surf.get_size())//2)
            font = pygame.font.SysFont(None, 20)
            text = font.render("IMG", True, (255, 255, 255))
            surf.blit(text, (surf.get_width() // 2 - text.get_width() // 2,
                             surf.get_height() // 2 - text.get_height() // 2))
            return surf

