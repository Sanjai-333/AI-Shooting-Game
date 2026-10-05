import pygame


class HUD:
    def __init__(self):
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)
        self.title_font = pygame.font.Font(None, 34)

    def draw_panel(self, screen):
        panel = pygame.Surface((230, 115), pygame.SRCALPHA)

        panel.fill((15, 20, 30, 210))

        screen.blit(panel, (15, 15))

        pygame.draw.rect(
            screen,
            (80, 90, 110),
            (15, 15, 230, 115),
            2,
            border_radius=10
        )

    def draw_health_bar(
        self,
        screen,
        x,
        y,
        health,
        max_health,
        width=180,
        height=16
    ):
        # Background
        pygame.draw.rect(
            screen,
            (45, 45, 55),
            (x, y, width, height),
            border_radius=6
        )

        # Health
        health_width = int(
            width * (health / max_health)
        )

        health_width = max(0, health_width)

        pygame.draw.rect(
            screen,
            (60, 210, 110),
            (x, y, health_width, height),
            border_radius=6
        )

    def draw(
        self,
        screen,
        player_health,
        score,
        difficulty
    ):
        self.draw_panel(screen)

        # Player label
        player_text = self.title_font.render(
            "PLAYER",
            True,
            (235, 240, 250)
        )

        screen.blit(
            player_text,
            (28, 23)
        )

        # Health bar
        self.draw_health_bar(
            screen,
            28,
            58,
            player_health,
            100
        )

        # Health number
        health_text = self.small_font.render(
            f"{player_health} HP",
            True,
            (235, 240, 250)
        )

        screen.blit(
            health_text,
            (28, 80)
        )

        # Score
        score_text = self.small_font.render(
            f"SCORE: {score}",
            True,
            (255, 215, 90)
        )

        screen.blit(
            score_text,
            (28, 103)
        )

        # AI difficulty
        ai_text = self.small_font.render(
            f"AI LEVEL: {difficulty}",
            True,
            (170, 200, 255)
        )

        screen.blit(
            ai_text,
            (120, 103)
        )

    def draw_pause(self, screen):
        overlay = pygame.Surface(
            screen.get_size(),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 150))

        screen.blit(
            overlay,
            (0, 0)
        )

        pause_text = self.title_font.render(
            "GAME PAUSED",
            True,
            (255, 255, 255)
        )

        text_rect = pause_text.get_rect(
            center=screen.get_rect().center
        )

        screen.blit(
            pause_text,
            text_rect
        )

    def draw_game_over(self, screen, score):
        overlay = pygame.Surface(
            screen.get_size(),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 180))

        screen.blit(
            overlay,
            (0, 0)
        )

        game_over_text = pygame.font.Font(
            None,
            55
        ).render(
            "GAME OVER",
            True,
            (255, 80, 80)
        )

        score_text = self.font.render(
            f"Final Score: {score}",
            True,
            (255, 255, 255)
        )

        restart_text = self.small_font.render(
            "Press R to Restart",
            True,
            (200, 210, 220)
        )

        center_x = screen.get_width() // 2

        screen.blit(
            game_over_text,
            (
                center_x - game_over_text.get_width() // 2,
                220
            )
        )

        screen.blit(
            score_text,
            (
                center_x - score_text.get_width() // 2,
                285
            )
        )

        screen.blit(
            restart_text,
            (
                center_x - restart_text.get_width() // 2,
                325
            )
        )