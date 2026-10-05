import pygame
import os
import math
import random

from game.player import Player
from game.enemy import Enemy
from game.ai import EnemyAI
from game.bullets import Bullet
from game.effects import Effects

from ui.menu import Menu
from ui.hud import HUD


# =========================================================
# INITIALIZATION
# =========================================================

pygame.init()

try:
    pygame.mixer.init()
    SOUND_ENABLED = True
except pygame.error:
    SOUND_ENABLED = False


WIDTH = 1000
HEIGHT = 650

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "AI Shooting Game"
)

clock = pygame.time.Clock()

FPS = 60


# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

IMAGE_DIR = os.path.join(
    BASE_DIR,
    "assets",
    "images"
)

SOUND_DIR = os.path.join(
    BASE_DIR,
    "assets",
    "sounds"
)


# =========================================================
# LOAD IMAGES
# =========================================================

player_image = pygame.image.load(
    os.path.join(
        IMAGE_DIR,
        "player.png"
    )
).convert_alpha()

enemy_image = pygame.image.load(
    os.path.join(
        IMAGE_DIR,
        "enemy.png"
    )
).convert_alpha()


# =========================================================
# LOAD SOUNDS
# =========================================================

player_shoot_sound = None
enemy_shoot_sound = None
hit_sound = None


def load_sound(filename):

    if not SOUND_ENABLED:
        return None

    path = os.path.join(
        SOUND_DIR,
        filename
    )

    try:

        return pygame.mixer.Sound(
            path
        )

    except pygame.error:

        print(
            "Could not load sound:",
            filename
        )

        return None


player_shoot_sound = load_sound(
    "player_shoot.wav"
)

enemy_shoot_sound = load_sound(
    "enemy_shoot.wav"
)

hit_sound = load_sound(
    "hit.wav"
)


def play_sound(sound, name):

    if not SOUND_ENABLED:
        return

    if sound is None:
        return

    try:

        sound.play()

    except pygame.error:

        print(
            "Sound error:",
            name
        )


# =========================================================
# OBJECTS
# =========================================================

menu = Menu()

hud = HUD()

effects = Effects()

player = Player(
    100,
    HEIGHT // 2,
    player_image
)

enemy = Enemy(
    WIDTH - 180,
    HEIGHT // 2,
    enemy_image
)

ai = EnemyAI()


# =========================================================
# BULLETS
# =========================================================

player_bullets = []

enemy_bullets = []


# =========================================================
# GAME VARIABLES
# =========================================================

score = 0

game_state = "MENU"

running = True


# =========================================================
# RESET GAME
# =========================================================

def reset_game():

    global score
    global player_bullets
    global enemy_bullets

    score = 0

    player_bullets = []

    enemy_bullets = []

    player.reset(
        100,
        HEIGHT // 2
    )

    enemy.reset(
        WIDTH - 180,
        HEIGHT // 2
    )

    ai.state = ai.CHASE

    ai.reaction_timer = 0

    ai.update_difficulty(
        score
    )


# =========================================================
# BACKGROUND
# =========================================================

def draw_game_background():

    screen.fill(
        (8, 12, 22)
    )

    grid_size = 50

    for x in range(
        0,
        WIDTH,
        grid_size
    ):

        pygame.draw.line(
            screen,
            (20, 28, 45),
            (x, 0),
            (x, HEIGHT)
        )

    for y in range(
        0,
        HEIGHT,
        grid_size
    ):

        pygame.draw.line(
            screen,
            (20, 28, 45),
            (0, y),
            (WIDTH, y)
        )


# =========================================================
# GUN
# =========================================================

def draw_gun(
    screen,
    center_x,
    center_y,
    target_x,
    target_y,
    gun_color
):

    dx = target_x - center_x

    dy = target_y - center_y

    distance = math.sqrt(
        dx * dx +
        dy * dy
    )

    if distance == 0:
        return

    direction_x = dx / distance

    direction_y = dy / distance

    gun_length = 38

    end_x = (
        center_x
        + direction_x
        * gun_length
    )

    end_y = (
        center_y
        + direction_y
        * gun_length
    )

    pygame.draw.line(
        screen,
        gun_color,
        (
            int(center_x),
            int(center_y)
        ),
        (
            int(end_x),
            int(end_y)
        ),
        9
    )

    pygame.draw.circle(
        screen,
        gun_color,
        (
            int(end_x),
            int(end_y)
        ),
        5
    )


# =========================================================
# MAIN LOOP
# =========================================================

while running:

    clock.tick(FPS)

    # =====================================================
    # EVENTS
    # =====================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # =================================================
        # MENU
        # =================================================

        if game_state == "MENU":

            result = menu.handle_event(
                event
            )

            if result == "START GAME":

                reset_game()

                game_state = "GAME"

            elif result == "HOW TO PLAY":

                game_state = "HOW_TO_PLAY"

            elif result == "QUIT":

                running = False

        # =================================================
        # HOW TO PLAY
        # =================================================

        elif game_state == "HOW_TO_PLAY":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    game_state = "MENU"

        # =================================================
        # GAME
        # =================================================

        elif game_state == "GAME":

            if event.type == pygame.KEYDOWN:

                # Pause
                if event.key == pygame.K_p:

                    game_state = "PAUSED"

                # Menu
                elif event.key == pygame.K_ESCAPE:

                    game_state = "MENU"

                # Player shooting
                elif event.key == pygame.K_SPACE:

                    enemy_center_x, enemy_center_y = (
                        enemy.get_center()
                    )

                    bullet = player.shoot(
                        enemy_center_x,
                        enemy_center_y
                    )

                    if bullet:

                        player_bullets.append(
                            Bullet(
                                bullet["x"],
                                bullet["y"],
                                enemy_center_x,
                                enemy_center_y,
                                speed=14,
                                damage=20
                            )
                        )

                        play_sound(
                            player_shoot_sound,
                            "Player Shoot Sound"
                        )

                        effects.create_muzzle_flash(
                            bullet["x"],
                            bullet["y"]
                        )

        # =================================================
        # PAUSED
        # =================================================

        elif game_state == "PAUSED":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p:

                    game_state = "GAME"

                elif event.key == pygame.K_ESCAPE:

                    game_state = "MENU"

        # =================================================
        # GAME OVER
        # =================================================

        elif game_state == "GAME_OVER":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:

                    reset_game()

                    game_state = "GAME"

                elif event.key == pygame.K_ESCAPE:

                    game_state = "MENU"

    # =====================================================
    # GAME UPDATE
    # =====================================================

    if game_state == "GAME":

        # -------------------------------------------------
        # PLAYER
        # -------------------------------------------------

        player.update(
            WIDTH,
            HEIGHT
        )

        # -------------------------------------------------
        # PLAYER CENTER
        # -------------------------------------------------

        player_center_x, player_center_y = (
            player.get_center()
        )

        # -------------------------------------------------
        # ENEMY CENTER
        # -------------------------------------------------

        enemy_center_x, enemy_center_y = (
            enemy.get_center()
        )

        # -------------------------------------------------
        # DISTANCE
        # -------------------------------------------------

        distance = ai.get_distance(
            enemy_center_x,
            enemy_center_y,
            player_center_x,
            player_center_y
        )

        # -------------------------------------------------
        # AI STATE
        # -------------------------------------------------

        ai.decide_state(
            enemy_center_x,
            enemy_center_y,
            player_center_x,
            player_center_y
        )

        ai.update_reaction()

        # -------------------------------------------------
        # ENEMY MOVEMENT
        # -------------------------------------------------

        enemy.update_movement(
            player_center_x,
            player_center_y,
            WIDTH,
            HEIGHT,
            ai
        )

        enemy.update_cooldowns()

        # -------------------------------------------------
        # NEW ENEMY POSITION
        # -------------------------------------------------

        enemy_center_x, enemy_center_y = (
            enemy.get_center()
        )

        distance = ai.get_distance(
            enemy_center_x,
            enemy_center_y,
            player_center_x,
            player_center_y
        )

        # -------------------------------------------------
        # ENEMY SHOOTING
        # -------------------------------------------------

        if ai.should_shoot(
            distance
        ):

            predicted_x, predicted_y = (
                ai.predict_position(
                    player_center_x,
                    player_center_y,
                    player.velocity_x,
                    player.velocity_y
                )
            )

            # Keep prediction inside screen

            predicted_x = max(
                0,
                min(
                    predicted_x,
                    WIDTH
                )
            )

            predicted_y = max(
                0,
                min(
                    predicted_y,
                    HEIGHT
                )
            )

            # ---------------------------------------------
            # Add small adaptive aim error at lower levels
            # ---------------------------------------------

            accuracy = ai.aim_accuracy

            if random.random() > accuracy:

                aim_error = (
                    30
                    + (4 - ai.difficulty) * 10
                )

                predicted_x += random.uniform(
                    -aim_error,
                    aim_error
                )

                predicted_y += random.uniform(
                    -aim_error,
                    aim_error
                )

            predicted_x = max(
                0,
                min(
                    predicted_x,
                    WIDTH
                )
            )

            predicted_y = max(
                0,
                min(
                    predicted_y,
                    HEIGHT
                )
            )

            enemy_bullet = enemy.shoot(
                predicted_x,
                predicted_y
            )

            if enemy_bullet:

                bullet_speed = (
                    10
                    + ai.difficulty * 1.5
                )

                bullet_damage = (
                    8
                    + ai.difficulty * 4
                )

                enemy_bullets.append(
                    Bullet(
                        enemy_bullet["x"],
                        enemy_bullet["y"],
                        predicted_x,
                        predicted_y,
                        speed=bullet_speed,
                        damage=bullet_damage
                    )
                )

                play_sound(
                    enemy_shoot_sound,
                    "Enemy Shoot Sound"
                )

                effects.create_muzzle_flash(
                    enemy_bullet["x"],
                    enemy_bullet["y"]
                )

        # -------------------------------------------------
        # PLAYER BULLETS
        # -------------------------------------------------

        for bullet in player_bullets:

            bullet.update(
                WIDTH,
                HEIGHT
            )

            if bullet.check_collision(
                enemy.x,
                enemy.y,
                enemy.width,
                enemy.height
            ):

                enemy.take_damage(
                    bullet.damage
                )

                bullet.active = False

                score += 20

                play_sound(
                    hit_sound,
                    "Hit Sound"
                )

                effects.create_hit_effect(
                    bullet.x,
                    bullet.y
                )

                ai.player_shot_reaction()

        player_bullets = [
            bullet
            for bullet in player_bullets
            if bullet.active
        ]

        # -------------------------------------------------
        # ENEMY BULLETS
        # -------------------------------------------------

        for bullet in enemy_bullets:

            bullet.update(
                WIDTH,
                HEIGHT
            )

            if bullet.check_collision(
                player.x,
                player.y,
                player.width,
                player.height
            ):

                player.take_damage(
                    bullet.damage
                )

                bullet.active = False

                play_sound(
                    hit_sound,
                    "Hit Sound"
                )

                effects.create_hit_effect(
                    bullet.x,
                    bullet.y
                )

        enemy_bullets = [
            bullet
            for bullet in enemy_bullets
            if bullet.active
        ]

        # -------------------------------------------------
        # ENEMY DEFEATED
        # -------------------------------------------------

        if enemy.health <= 0:

            score += 100

            enemy.reset(
                WIDTH - 180,
                HEIGHT // 2
            )

            ai.update_difficulty(
                score
            )

        # -------------------------------------------------
        # PLAYER DEFEATED
        # -------------------------------------------------

        if player.health <= 0:

            game_state = "GAME_OVER"

        # -------------------------------------------------
        # EFFECTS
        # -------------------------------------------------

        effects.update()

    # =====================================================
    # DRAW
    # =====================================================

    if game_state == "MENU":

        menu.draw(
            screen
        )

    elif game_state == "HOW_TO_PLAY":

        menu.draw_how_to_play(
            screen
        )

    elif game_state in [
        "GAME",
        "PAUSED",
        "GAME_OVER"
    ]:

        draw_game_background()

        # -------------------------------------------------
        # PLAYER
        # -------------------------------------------------

        player.draw(
            screen
        )

        player_center_x, player_center_y = (
            player.get_center()
        )

        enemy_center_x, enemy_center_y = (
            enemy.get_center()
        )

        # Player automatically aims at enemy

        draw_gun(
            screen,
            player_center_x,
            player_center_y,
            enemy_center_x,
            enemy_center_y,
            (80, 90, 110)
        )

        # -------------------------------------------------
        # ENEMY
        # -------------------------------------------------

        enemy.draw(
            screen
        )

        # Predictive enemy aim

        predicted_draw_x, predicted_draw_y = (
            ai.predict_position(
                player_center_x,
                player_center_y,
                player.velocity_x,
                player.velocity_y
            )
        )

        predicted_draw_x = max(
            0,
            min(
                predicted_draw_x,
                WIDTH
            )
        )

        predicted_draw_y = max(
            0,
            min(
                predicted_draw_y,
                HEIGHT
            )
        )

        draw_gun(
            screen,
            enemy_center_x,
            enemy_center_y,
            predicted_draw_x,
            predicted_draw_y,
            (110, 70, 70)
        )

        # -------------------------------------------------
        # BULLETS
        # -------------------------------------------------

        for bullet in player_bullets:

            bullet.draw(
                screen,
                (255, 220, 80)
            )

        for bullet in enemy_bullets:

            bullet.draw(
                screen,
                (255, 80, 80)
            )

        # -------------------------------------------------
        # EFFECTS
        # -------------------------------------------------

        effects.draw(
            screen
        )

        # -------------------------------------------------
        # HUD
        # -------------------------------------------------

        hud.draw(
            screen,
            player.health,
            score,
            ai.difficulty
        )

        # -------------------------------------------------
        # PAUSE
        # -------------------------------------------------

        if game_state == "PAUSED":

            hud.draw_pause(
                screen
            )

        # -------------------------------------------------
        # GAME OVER
        # -------------------------------------------------

        if game_state == "GAME_OVER":

            hud.draw_game_over(
                screen,
                score
            )

    pygame.display.flip()


# =========================================================
# CLEANUP
# =========================================================

pygame.quit()