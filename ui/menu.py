import pygame


class Menu:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 72)
        self.button_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)

        self.selected = 0

        self.buttons = [
            "START GAME",
            "HOW TO PLAY",
            "QUIT"
        ]

    def draw_background(self, screen):
        width, height = screen.get_size()

        # Dark futuristic background
        screen.fill((8, 12, 22))

        # Grid
        grid_size = 50

        for x in range(0, width, grid_size):
            pygame.draw.line(
                screen,
                (20, 28, 45),
                (x, 0),
                (x, height)
            )

        for y in range(0, height, grid_size):
            pygame.draw.line(
                screen,
                (20, 28, 45),
                (0, y),
                (width, y)
            )

    def draw(self, screen):
        self.draw_background(screen)

        width, height = screen.get_size()

        # Title
        title = self.title_font.render(
            "AI SHOOTING GAME",
            True,
            (235, 240, 255)
        )

        screen.blit(
            title,
            (
                width // 2 - title.get_width() // 2,
                100
            )
        )

        subtitle = self.small_font.render(
            "SMART AI COMBAT SYSTEM",
            True,
            (130, 170, 220)
        )

        screen.blit(
            subtitle,
            (
                width // 2 - subtitle.get_width() // 2,
                165
            )
        )

        # Buttons
        for i, button in enumerate(self.buttons):

            button_width = 260
            button_height = 52

            x = width // 2 - button_width // 2
            y = 245 + i * 70

            if i == self.selected:
                color = (55, 100, 170)
                border_color = (130, 180, 255)
            else:
                color = (25, 32, 48)
                border_color = (70, 80, 100)

            pygame.draw.rect(
                screen,
                color,
                (x, y, button_width, button_height),
                border_radius=10
            )

            pygame.draw.rect(
                screen,
                border_color,
                (x, y, button_width, button_height),
                2,
                border_radius=10
            )

            text = self.button_font.render(
                button,
                True,
                (240, 245, 255)
            )

            screen.blit(
                text,
                (
                    width // 2 - text.get_width() // 2,
                    y + 13
                )
            )

        # Controls
        controls = self.small_font.render(
            "UP / DOWN = Select     ENTER = Confirm",
            True,
            (120, 130, 150)
        )

        screen.blit(
            controls,
            (
                width // 2 - controls.get_width() // 2,
                height - 55
            )
        )

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_UP:
            self.selected -= 1

            if self.selected < 0:
                self.selected = len(self.buttons) - 1

        elif event.key == pygame.K_DOWN:
            self.selected += 1

            if self.selected >= len(self.buttons):
                self.selected = 0

        elif event.key == pygame.K_RETURN:
            return self.buttons[self.selected]

        return None

    def draw_how_to_play(self, screen):
        self.draw_background(screen)

        width, height = screen.get_size()

        title = self.title_font.render(
            "HOW TO PLAY",
            True,
            (235, 240, 255)
        )

        screen.blit(
            title,
            (
                width // 2 - title.get_width() // 2,
                70
            )
        )

        instructions = [
            "ARROW KEYS  -  Move Player",
            "SPACE       -  Shoot",
            "P             -  Pause",
            "",
            "The AI predicts your movement.",
            "The enemy changes between CHASE,",
            "ATTACK and RETREAT states.",
            "",
            "Defeat the AI to increase your score.",
            "",
            "Press ESC to return"
        ]

        y = 175

        for line in instructions:

            text = self.small_font.render(
                line,
                True,
                (210, 220, 235)
            )

            screen.blit(
                text,
                (
                    width // 2 - text.get_width() // 2,
                    y
                )
            )

            y += 32