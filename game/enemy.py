import pygame
import math


class Enemy:

    def __init__(self, x, y, image):

        self.x = x
        self.y = y

        self.width = 80
        self.height = 80

        self.base_speed = 3.0
        self.speed = self.base_speed

        self.health = 100
        self.max_health = 100

        self.image = pygame.transform.scale(
            image,
            (self.width, self.height)
        )

        self.velocity_x = 0
        self.velocity_y = 0

        self.shoot_cooldown = 0
        self.shoot_cooldown_limit = 34

        self.reaction_timer = 0

        # Adaptive movement
        self.strafe_direction = 1
        self.strafe_timer = 0

        self.change_direction_timer = 0

    def get_center(self):

        return (
            self.x + self.width // 2,
            self.y + self.height // 2
        )

    def update_movement(
        self,
        player_x,
        player_y,
        screen_width,
        screen_height,
        ai
    ):

        enemy_center_x, enemy_center_y = (
            self.get_center()
        )

        dx = player_x - enemy_center_x
        dy = player_y - enemy_center_y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        if distance == 0:
            return

        direction_x = dx / distance
        direction_y = dy / distance

        # -----------------------------------------
        # Change strafe direction periodically
        # -----------------------------------------

        if self.strafe_timer > 0:
            self.strafe_timer -= 1

        else:

            self.strafe_direction *= -1

            self.strafe_timer = (
                ai.get_strafe_time()
            )

        # -----------------------------------------
        # Change movement direction unpredictably
        # -----------------------------------------

        if self.change_direction_timer > 0:
            self.change_direction_timer -= 1

        else:

            self.change_direction_timer = (
                ai.get_direction_change_time()
            )

            self.strafe_direction *= -1

        # Perpendicular direction
        strafe_x = -direction_y
        strafe_y = direction_x

        movement_x = 0
        movement_y = 0

        # -----------------------------------------
        # FAR RANGE
        # Aggressively chase
        # -----------------------------------------

        if distance > 360:

            movement_x = (
                direction_x
                * self.speed
                * 1.15
            )

            movement_y = (
                direction_y
                * self.speed
                * 1.15
            )

        # -----------------------------------------
        # MEDIUM RANGE
        # Chase + strafe
        # -----------------------------------------

        elif distance > 200:

            movement_x = (
                direction_x
                * self.speed
                * 0.55
            )

            movement_y = (
                direction_y
                * self.speed
                * 0.55
            )

            movement_x += (
                strafe_x
                * self.speed
                * 0.95
                * self.strafe_direction
            )

            movement_y += (
                strafe_y
                * self.speed
                * 0.95
                * self.strafe_direction
            )

        # -----------------------------------------
        # CLOSE RANGE
        # Circle around player
        # -----------------------------------------

        else:

            movement_x = (
                strafe_x
                * self.speed
                * 1.35
                * self.strafe_direction
            )

            movement_y = (
                strafe_y
                * self.speed
                * 1.35
                * self.strafe_direction
            )

            # Push away if too close
            if distance < 145:

                movement_x += (
                    -direction_x
                    * self.speed
                    * 1.25
                )

                movement_y += (
                    -direction_y
                    * self.speed
                    * 1.25
                )

        # -----------------------------------------
        # Apply movement
        # -----------------------------------------

        self.velocity_x = movement_x
        self.velocity_y = movement_y

        self.x += self.velocity_x
        self.y += self.velocity_y

        # -----------------------------------------
        # Screen boundaries
        # -----------------------------------------

        self.x = max(
            0,
            min(
                self.x,
                screen_width - self.width
            )
        )

        self.y = max(
            0,
            min(
                self.y,
                screen_height - self.height
            )
        )

    def update_cooldowns(self):

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.reaction_timer > 0:
            self.reaction_timer -= 1

    def shoot(
        self,
        target_x,
        target_y
    ):

        if self.shoot_cooldown > 0:
            return None

        center_x, center_y = (
            self.get_center()
        )

        dx = target_x - center_x
        dy = target_y - center_y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        if distance == 0:
            return None

        bullet_speed = 10

        velocity_x = (
            dx / distance
        ) * bullet_speed

        velocity_y = (
            dy / distance
        ) * bullet_speed

        self.shoot_cooldown = (
            self.shoot_cooldown_limit
        )

        return {
            "x": center_x,
            "y": center_y,
            "vx": velocity_x,
            "vy": velocity_y
        }

    def take_damage(self, damage):

        self.health -= damage

        if self.health < 0:
            self.health = 0

    def reset(self, x, y):

        self.x = x
        self.y = y

        self.health = self.max_health

        self.velocity_x = 0
        self.velocity_y = 0

        self.shoot_cooldown = 0
        self.reaction_timer = 0

        self.strafe_direction = 1
        self.strafe_timer = 0
        self.change_direction_timer = 0

    def draw(self, screen):

        screen.blit(
            self.image,
            (
                int(self.x),
                int(self.y)
            )
        )

        # Enemy health bar

        bar_width = 80
        bar_height = 8

        bar_x = (
            self.x
            + self.width // 2
            - bar_width // 2
        )

        bar_y = self.y - 18

        pygame.draw.rect(
            screen,
            (45, 45, 50),
            (
                bar_x,
                bar_y,
                bar_width,
                bar_height
            )
        )

        health_width = int(
            bar_width
            * (
                self.health
                / self.max_health
            )
        )

        health_width = max(
            0,
            health_width
        )

        pygame.draw.rect(
            screen,
            (220, 50, 50),
            (
                bar_x,
                bar_y,
                health_width,
                bar_height
            )
        )