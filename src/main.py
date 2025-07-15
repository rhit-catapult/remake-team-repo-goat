import math
import random
import sys

import pygame

import constant
import level
import loot
import player

pygame.init()

screen = pygame.display.set_mode((constant.WIDTH, constant.HEIGHT))
pygame.display.set_caption("2D shoting game")


def main():
    clock = pygame.time.Clock()

    player_instance = player.Player(constant.WIDTH // 2, constant.HEIGHT // 2)

    current_level = 1
    level_instance = level.Level(current_level)
    walls = level_instance.walls
    enemies = level_instance.enemies
    weapon_drops = level_instance.weapon_drops
    player_instance.x, player_instance.y = level_instance.initial_player_pos

    bullets = []

    game_over = False
    level_complete = False
    score = 0

    # 游戏主循环
    while True:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 键盘按下事件 - 移动控制
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player_instance.moving["up"] = True
                if event.key == pygame.K_s:
                    player_instance.moving["down"] = True
                if event.key == pygame.K_a:
                    player_instance.moving["left"] = True
                if event.key == pygame.K_d:
                    player_instance.moving["right"] = True

                if event.key == pygame.K_r and not game_over:  # 换弹
                    player_instance.reload()
                if event.key == pygame.K_j and not game_over:  # 射击
                    player_instance.shoot(bullets, enemies, walls)
                if event.key == pygame.K_1:  # 切换武器（0）
                    player_instance.switch_weapon(0)
                if event.key == pygame.K_2:  # 切换武器（1）
                    player_instance.switch_weapon(1)
                if event.key == pygame.K_3:
                    player_instance.switch_weapon(2)
                if event.key == pygame.K_4:
                    player_instance.switch_weapon(3)
                if event.key == pygame.K_5:
                    player_instance.switch_weapon(4)

                if event.key == pygame.K_SPACE and (game_over or level_complete):  # 重新开始游戏或进入下一关
                    if game_over:
                        return main()
                    elif level_complete:
                        level_complete = False
                        current_level += 1
                        if current_level > 3:  # 总共3关
                            current_level = 1
                        level_instance = level.Level(current_level)
                        walls = level_instance.walls
                        enemies = level_instance.enemies
                        weapon_drops = level_instance.weapon_drops
                        player_instance.x, player_instance.y = level_instance.initial_player_pos
                        player_instance.health = min(player_instance.max_health, player_instance.health + 30)  # 恢复部分生命值
                        bullets = []

            # 键盘释放事件 - 移动控制
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player_instance.moving["up"] = False
                if event.key == pygame.K_s:
                    player_instance.moving["down"] = False
                if event.key == pygame.K_a:
                    player_instance.moving["left"] = False
                if event.key == pygame.K_d:
                    player_instance.moving["right"] = False

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if event.button == 1:  # 左键射击
                    player_instance.shoot(bullets, enemies, walls)

        if game_over:
            # 绘制游戏结束屏幕
            screen.fill(constant.BACKGROUND)

            # 绘制标题
            font_large = pygame.font.SysFont(None, 72)
            font_medium = pygame.font.SysFont(None, 48)
            font_small = pygame.font.SysFont(None, 36)

            game_over_text = font_large.render("GAME OVER", True, (220, 20, 60))
            score_text = font_medium.render(f"Final Score: {score}", True, constant.TEXT_COLOR)
            level_text = font_medium.render(f"Reached Level: {current_level}", True, constant.TEXT_COLOR)
            restart_text = font_small.render("Press SPACE to Restart", True, constant.TEXT_COLOR)

            screen.blit(game_over_text,
                        (constant.WIDTH // 2 - game_over_text.get_width() // 2, constant.HEIGHT // 2 - 150))
            screen.blit(score_text, (constant.WIDTH // 2 - score_text.get_width() // 2, constant.HEIGHT // 2 - 50))
            screen.blit(level_text, (constant.WIDTH // 2 - level_text.get_width() // 2, constant.HEIGHT // 2))
            screen.blit(restart_text, (constant.WIDTH // 2 - restart_text.get_width() // 2, constant.HEIGHT // 2 + 100))

            pygame.display.flip()
            clock.tick(60)
            continue

        if level_complete:
            # 绘制关卡完成屏幕
            screen.fill(constant.BACKGROUND)

            font_large = pygame.font.SysFont(None, 72)
            font_medium = pygame.font.SysFont(None, 48)
            font_small = pygame.font.SysFont(None, 36)

            level_text = font_large.render(f"LEVEL {current_level} COMPLETE!", True, (50, 205, 50))
            score_text = font_medium.render(f"Score: {score}", True, constant.TEXT_COLOR)
            next_text = font_small.render("Press SPACE to Continue to Next Level", True, constant.TEXT_COLOR)

            screen.blit(level_text, (constant.WIDTH // 2 - level_text.get_width() // 2, constant.HEIGHT // 2 - 100))
            screen.blit(score_text, (constant.WIDTH // 2 - score_text.get_width() // 2, constant.HEIGHT // 2))
            screen.blit(next_text, (constant.WIDTH // 2 - next_text.get_width() // 2, constant.HEIGHT // 2 + 100))

            pygame.display.flip()
            clock.tick(60)
            continue

        # 获取鼠标位置并更新玩家方向
        mouse_pos = pygame.mouse.get_pos()
        player_instance.rotate(mouse_pos)

        # 更新玩家移动
        player_instance.update_movement(walls)

        # 更新玩家状态
        player_instance.update()

        # 更新敌人
        for enemy in enemies[:]:
            enemy.move_towards_player(player_instance.x, player_instance.y, walls)
            enemy.update()

            # 检查敌人是否攻击玩家
            dx = enemy.x - player_instance.x
            dy = enemy.y - player_instance.y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < enemy.radius + player_instance.radius:
                if enemy.can_attack(player_instance.x, player_instance.y):
                    player_instance.health -= enemy.damage
                    if player_instance.health <= 0:
                        game_over = True
            elif enemy.enemy_type == "sniper" and enemy.attack_cooldown > 0:
                # 狙击手瞄准线
                enemy.target_x = player_instance.x
                enemy.target_y = player_instance.y

        # 更新子弹
        for bullet in bullets[:]:
            bullet.move()

            # 检查子弹是否击中敌人
            for enemy in enemies[:]:
                dx = bullet.x - enemy.x
                dy = bullet.y - enemy.y
                distance = math.sqrt(dx * dx + dy * dy)

                if distance < bullet.radius + enemy.radius:
                    if bullet.is_explosive:
                        # 爆炸伤害范围内所有敌人
                        for e in enemies[:]:
                            edx = bullet.x - e.x
                            edy = bullet.y - e.y
                            edist = math.sqrt(edx * edx + edy * edy)
                            if edist < bullet.explosion_radius:
                                if e.take_damage(bullet.damage):
                                    player_instance.kills += 1
                                    score += e.score_value
                                    # 掉落武器的概率
                                    if random.random() < 0.3 and len(player_instance.weapons) < 5:
                                        weapon_types = ["Shotgun", "Rifle", "Rocket Launcher", "Knife"]
                                        for wt in weapon_types:
                                            if wt not in player_instance.weapons:
                                                weapon_drops.append(loot.WeaponDrop(e.x, e.y, wt))
                                                break
                                    enemies.remove(e)
                        bullets.remove(bullet)
                        break
                    else:
                        if enemy.take_damage(bullet.damage):
                            player_instance.kills += 1
                            score += enemy.score_value
                            # 掉落武器的概率
                            if random.random() < 0.3 and len(player_instance.weapons) < 5:
                                weapon_types = ["Shotgun", "Rifle", "Rocket Launcher", "Knife"]
                                for wt in weapon_types:
                                    if wt not in player_instance.weapons:
                                        weapon_drops.append(loot.WeaponDrop(enemy.x, enemy.y, wt))
                                        break
                            enemies.remove(enemy)
                        bullets.remove(bullet)
                        break

            # 移除出界的子弹
            # if bullet.is_out_of_bounds():
            #     bullets.remove(bullet)

        # 检查武器掉落
        for drop in weapon_drops[:]:
            if drop.check_collision(player_instance):
                player_instance.add_weapon(drop.weapon_type)
                weapon_drops.remove(drop)

        # 检查关卡是否完成
        if len(enemies) == 0 and not level_complete:
            level_complete = True

        # 绘制游戏
        screen.fill(constant.BACKGROUND)

        # 绘制墙壁
        for wall in walls:
            wall.draw(screen)

        # 绘制武器掉落
        for drop in weapon_drops:
            drop.draw(screen)

        # 绘制子弹
        for bullet in bullets:
            bullet.draw(screen)

        # 绘制敌人
        for enemy in enemies:
            enemy.draw(screen)

        # 绘制玩家
        player_instance.draw(screen)

        # 绘制HUD
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, constant.TEXT_COLOR)
        level_text = font.render(f"Level: {current_level}", True, constant.TEXT_COLOR)
        health_text = font.render(f"Health: {player_instance.health}", True, constant.TEXT_COLOR)
        kills_text = font.render(f"Kills: {player_instance.kills}", True, constant.TEXT_COLOR)

        screen.blit(score_text, (20, 20))
        screen.blit(level_text, (20, 60))
        screen.blit(health_text, (20, 100))
        screen.blit(kills_text, (20, 140))

        # 绘制控制说明
        controls_font = pygame.font.SysFont(None, 24)
        controls = [
            "Controls: WASD - Move, Mouse - Aim, LMB/J - Shoot",
            "R - Reload, Q/E - Switch Weapon, SPACE - Next Level"
        ]

        for i, text in enumerate(controls):
            ctrl_text = controls_font.render(text, True, constant.TEXT_COLOR)
            screen.blit(ctrl_text, (constant.WIDTH - ctrl_text.get_width() - 20, 20 + i * 30))

        # 绘制武器栏
        weapon_y = constant.HEIGHT - 50
        for i, weapon in enumerate(player_instance.weapons):
            color = constant.WEAPON_HIGHLIGHT if i == player_instance.current_weapon else (100, 100, 100)
            pygame.draw.rect(screen, color, (20 + i * 150, weapon_y, 140, 40))
            pygame.draw.rect(screen, (50, 50, 50), (20 + i * 150, weapon_y, 140, 40), 2)

            weapon_text = controls_font.render(weapon, True, (255, 255, 255))

            # 绘制武器图标
            if weapon in player_instance.weapon_icons:
                icon = player_instance.weapon_icons[weapon]
                screen.blit(icon, (20 + i * 150 + 70 - icon.get_width() // 2,
                                   weapon_y + 20 - icon.get_height() // 2))
            else:
                screen.blit(weapon_text, (20 + i * 150 + 70 - weapon_text.get_width() // 2, weapon_y + 15))

            # 如果是远程武器，显示弹药
            if weapon != "Knife":
                ammo_text = controls_font.render(f"{player_instance.ammo[weapon]}/{player_instance.max_ammo[weapon]}",
                                                 True,
                                                 (255, 255, 255))
                screen.blit(ammo_text, (20 + i * 150 + 70 - ammo_text.get_width() // 2, weapon_y + 25))

        # 游戏结束检查
        if player_instance.health <= 0:
            game_over = True

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
