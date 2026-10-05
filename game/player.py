import pygame
import math


class Player:

    def __init__(self, x, y, image):

        self.x = x
        self.y = y

        self.width = 80
        self.height = 80

        self.speed = 5

        self.health = 100

        self.image = pygame.transform.scale(
            image,
            (self.width, self.height)
        )

        self.velocity_x = 0
        self.velocity_y = 0

        # Slightly slower firing speed
        self.shoot_cooldown = 0

    def update(self, screen_width, screen_height):

        keys = pygame.key.get_pressed()

        self.velocity_x = 0
        self.velocity_y = 0

        if keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed

        if keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed

        if keys[pygame.K_UP]:
            self.velocity_y = -self.speed

        if keys[pygame.K_DOWN]:
            self.velocity_y = self.speed

        self.x += self.velocity_x
        self.y += self.velocity_y

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

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def get_center(self):

        return (
            self.x + self.width // 2,
            self.y + self.height // 2
        )

    def get_muzzle_position(
        self,
        target_x,
        target_y
    ):

        center_x, center_y = self.get_center()

        dx = target_x - center_x
        dy = target_y - center_y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        if distance == 0:
            return center_x, center_y

        direction_x = dx / distance
        direction_y = dy / distance

        muzzle_distance = 38

        muzzle_x = (
            center_x
            + direction_x * muzzle_distance
        )

        muzzle_y = (
            center_y
            + direction_y * muzzle_distance
        )

        return muzzle_x, muzzle_y

    def can_shoot(self):

        return self.shoot_cooldown <= 0

    def shoot(
        self,
        target_x,
        target_y
    ):

        if not self.can_shoot():
            return None

        muzzle_x, muzzle_y = (
            self.get_muzzle_position(
                target_x,
                target_y
            )
        )

        dx = target_x - muzzle_x
        dy = target_y - muzzle_y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        if distance == 0:
            return None

        bullet_speed = 14

        velocity_x = (
            dx / distance
        ) * bullet_speed

        velocity_y = (
            dy / distance
        ) * bullet_speed

        # Increased from 12 to 16
        # = slightly slower firing
        self.shoot_cooldown = 24

        return {
            "x": muzzle_x,
            "y": muzzle_y,
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

        self.health = 100

        self.velocity_x = 0
        self.velocity_y = 0

        self.shoot_cooldown = 0

    def draw(self, screen):

        screen.blit(
            self.image,
            (
                int(self.x),
                int(self.y)
            )
        )