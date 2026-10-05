import pygame
import math


class Bullet:

    def __init__(
        self,
        x,
        y,
        target_x,
        target_y,
        speed=12,
        damage=20
    ):

        self.x = x
        self.y = y

        self.speed = speed
        self.damage = damage

        # Slightly larger bullet
        self.radius = 6

        self.active = True

        dx = target_x - x
        dy = target_y - y

        distance = math.sqrt(
            dx * dx + dy * dy
        )

        if distance == 0:

            self.velocity_x = 0
            self.velocity_y = 0

        else:

            self.velocity_x = (
                dx / distance
            ) * speed

            self.velocity_y = (
                dy / distance
            ) * speed

    def update(
        self,
        screen_width,
        screen_height
    ):

        self.x += self.velocity_x
        self.y += self.velocity_y

        if (
            self.x < -20
            or self.x > screen_width + 20
            or self.y < -20
            or self.y > screen_height + 20
        ):

            self.active = False

    def check_collision(
        self,
        target_x,
        target_y,
        target_width,
        target_height
    ):

        # Expanded collision area
        collision_padding = 10

        return (
            self.x
            > target_x - collision_padding
            and
            self.x
            <
            target_x
            + target_width
            + collision_padding

            and

            self.y
            >
            target_y
            - collision_padding

            and

            self.y
            <
            target_y
            + target_height
            + collision_padding
        )

    def draw(
        self,
        screen,
        color=(255, 220, 80)
    ):

        pygame.draw.circle(
            screen,
            color,
            (
                int(self.x),
                int(self.y)
            ),
            self.radius
        )

        trail_x = int(
            self.x
            - self.velocity_x * 1.5
        )

        trail_y = int(
            self.y
            - self.velocity_y * 1.5
        )

        pygame.draw.line(
            screen,
            color,
            (
                trail_x,
                trail_y
            ),
            (
                int(self.x),
                int(self.y)
            ),
            3
        )