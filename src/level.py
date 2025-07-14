import constant
import wall
import loot
import enemy


class Level:
    def __init__(self, level_num):
        self.level_num = level_num
        self.walls = []
        self.enemies = []
        self.initial_player_pos = (constant.WIDTH // 2, constant.HEIGHT // 2)
        self.weapon_drops = []

        # 根据关卡号生成不同的关卡
        if level_num == 1:
            self._create_level_1()
        elif level_num == 2:
            self._create_level_2()
        else:  # 最终关卡
            self._create_level_3()

    def _create_level_1(self):
        # 简单迷宫布局
        self.walls = [
            wall.Wall(200, 150, 100, 30, "normal"),
            wall.Wall(400, 300, 30, 200, "normal"),
            wall.Wall(600, 100, 200, 30, "normal"),
            wall.Wall(700, 400, 100, 30, "normal"),
            wall.Wall(150, 500, 300, 30, "normal"),
            wall.Wall(800, 200, 30, 150, "normal"),
        ]

        # 初始敌人
        self.enemies = [
            enemy.Enemy(300, 300, "normal"),
            enemy.Enemy(700, 300, "normal"),
            enemy.Enemy(500, 500, "normal")
        ]

        # 初始武器掉落
        self.weapon_drops = [
            loot.WeaponDrop(200, 200, "Shotgun")
        ]

    def _create_level_2(self):
        # 更复杂的迷宫
        self.walls = [
            wall.Wall(100, 100, 50, 300, "normal"),
            wall.Wall(100, 100, 300, 50, "normal"),
            wall.Wall(350, 100, 50, 200, "normal"),
            wall.Wall(200, 250, 200, 50, "normal"),

            wall.Wall(650, 150, 200, 50, "normal"),
            wall.Wall(650, 300, 200, 50, "normal"),
            wall.Wall(800, 150, 50, 200, "normal"),
            wall.Wall(200, 450, 400, 50, "normal"),
            wall.Wall(700, 450, 200, 50, "normal"),
        ]

        # 敌人
        self.enemies = [
            enemy.Enemy(300, 200, "normal"),
            enemy.Enemy(400, 400, "fast"),
            enemy.Enemy(600, 200, "normal"),
            enemy.Enemy(750, 400, "normal"),
            enemy.Enemy(500, 350, "sniper")
        ]

        # 武器掉落
        self.weapon_drops = [
            loot.WeaponDrop(600, 400, "Rifle"),
            loot.WeaponDrop(400, 200, "Knife")
        ]

    def _create_level_3(self):
        # 最终关卡
        self.walls = [
            # 外部围墙
            wall.Wall(50, 50, 900, 30, "metal"),
            wall.Wall(50, 50, 30, 600, "metal"),
            wall.Wall(50, 620, 900, 30, "metal"),
            wall.Wall(920, 50, 30, 600, "metal"),

            # 内部障碍
            wall.Wall(150, 150, 200, 30, "normal"),
            wall.Wall(150, 150, 30, 200, "normal"),
            wall.Wall(650, 150, 200, 30, "normal"),
            wall.Wall(820, 150, 30, 200, "normal"),
            wall.Wall(150, 500, 200, 30, "normal"),
            wall.Wall(150, 330, 30, 200, "normal"),
            wall.Wall(650, 500, 200, 30, "normal"),
            wall.Wall(820, 330, 30, 200, "normal"),

            # Wall(400, 250, 200, 30, "breakable"),
            # Wall(400, 450, 200, 30, "breakable"),
            # Wall(350, 300, 30, 150, "breakable"),
            # Wall(620, 300, 30, 150, "breakable"),

            # 中心区域
            # Wall(450, 350, 100, 100, "metal")
        ]

        # 敌人
        self.enemies = [
            enemy.Enemy(250, 250, "tank"),
            enemy.Enemy(600, 200, "tank"),
            enemy.Enemy(250, 450, "tank"),
            enemy.Enemy(700, 450, "tank"),
            enemy.Enemy(350, 350, "sniper"),
            enemy.Enemy(750, 350, "sniper"),
            enemy.Enemy(350, 450, "sniper"),
            enemy.Enemy(750, 450, "sniper"),
            enemy.Enemy(550, 400, "boss")
        ]

        # 武器掉落
        self.weapon_drops = [
            loot.WeaponDrop(200, 400, "Rocket Launcher"),
            loot.WeaponDrop(800, 400, "Rocket Launcher"),
            loot.WeaponDrop(500, 200, "Rifle")
        ]
