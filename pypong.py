# Written by Curtis Newton, October 2022

try:
    import pygame
    from pygame.locals import *
    from pygame.mixer import *
    import random
    import sys
except ImportError: raise SystemExit("Sorry, can´t find required libraries.")

pygame.init()
pygame.mixer.init()

class Game:

    def __init__(self) -> None:
        self.SCREENRECT = pygame.Rect(0, 0, 600, 600)
        self.screen = pygame.display.set_mode(self.SCREENRECT.size)
        pygame.display.set_caption("PyPong v1.0")

        self.COLORS = {
            "red": [255, 0, 0],
            "blue": [0, 0, 255],
            "white": [255, 255, 255],
            "black": [0, 0, 0]
        }
        self.GAME_STATE = False

        self.ball_speed = [4, 4]
        self.ball = pygame.Rect(self.SCREENRECT.width * 0.5 - 20 * 0.5, random.randint(175, 300), 20, 20)

        self.player = pygame.Rect(self.SCREENRECT.width - 20, self.SCREENRECT.height * 0.5 - 20, 5, 75)
        self.player_speed = 8

        self.enemy = pygame.Rect(20, self.SCREENRECT.height * 0.5 - 20, 5, 75)
        self.enemy_speed = 7

        self.scores = [0, 0]

    def __stop(self) -> None:
        pygame.quit()
        sys.exit()

    def draw_scores_texts(self) -> None:
        font = pygame.font.Font(None, 30)
        color = pygame.Color("white")
        pscore = font.render(f"Score : {self.scores[0]}", 0, color)
        escore = font.render(f"Score : {self.scores[1]}", 0, color)
        self.screen.blit(pscore, (self.SCREENRECT.width - pscore.get_width() - 40, 20))
        self.screen.blit(escore, (40, 20))

    def draw_credits_text(self) -> None:
        font = pygame.font.Font(None, 20)
        text = font.render("Written by Curtis Newton, 2022, v2.0", 0, self.COLORS["red"])
        self.screen.blit(text, (self.SCREENRECT.width * 0.5 - text.get_width() * 0.5, self.SCREENRECT.height - 20))

    def handle_keyboard_inputs(self) -> None:
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.player.y >= 0: self.player.y -= self.player_speed
        if key[pygame.K_DOWN] and self.player.y <= self.SCREENRECT.height - self.player.height: self.player.y += self.player_speed

    def play_sound(self) -> None:
        sound = pygame.mixer.Sound("sound.wav")
        sound.play()

    def draw_menu(self) -> None:
        self.screen.fill(self.COLORS["white"])
        font = pygame.font.SysFont("dialog_font", 30)
        text = font.render("PyPong v2.0 written by Curtis Newton", 0, self.COLORS["red"])
        text2 = font.render("Press space key to start", 0, self.COLORS["blue"])
        cs = pygame.image.load("cnlogo.png")
        self.screen.blit(text, (self.SCREENRECT.width / 2 - text.get_width() / 2, 15))
        self.screen.blit(text2, (self.SCREENRECT.width / 2 - text2.get_width() / 2, text.get_height() + 15))
        self.screen.blit(cs, (self.SCREENRECT.width / 2 - cs.get_width() / 2, self.SCREENRECT.height / 2 - cs.get_height() / 2))
        pygame.display.flip()

    def run(self) -> None:
        running = True
        clock = pygame.time.Clock()
        fps = 60
        fps_index = 0

        while running:

            if not self.GAME_STATE:
                self.draw_menu()

                for evt in pygame.event.get():
                    if evt.type == pygame.QUIT or evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
                        pygame.quit()
                        break
                        quit()
                    elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_SPACE:
                        self.GAME_STATE = True
                        self.play_sound()

            else:
                self.handle_keyboard_inputs()

                self.screen.fill([0, 0, 0])
                self.draw_scores_texts()
                self.draw_credits_text()

                pygame.draw.line(self.screen, self.COLORS["white"], [self.SCREENRECT.width * 0.5, 0], [self.SCREENRECT.width * 0.5, self.SCREENRECT.height])

                pygame.draw.ellipse(self.screen, self.COLORS["white"], self.ball)
                self.ball.x += self.ball_speed[0]
                self.ball.y += self.ball_speed[1]

                if self.ball.x > self.SCREENRECT.width - 20 or self.ball.x < 0:
                    self.ball_speed[0] = -self.ball_speed[0]
                    if self.ball.x > self.SCREENRECT.width * 0.5:
                        self.scores[1] += 1
                        self.play_sound()
                    else: self.scores[0] += 1
                elif self.ball.y > self.SCREENRECT.height - 20 or self.ball.y < 0:
                    self.ball_speed[1] = -self.ball_speed[1]
                    self.play_sound()

                self.enemy.y = self.ball.y - self.enemy_speed

                if self.ball.colliderect(self.player):
                    self.ball_speed[0] = -self.ball_speed[0]
                    self.ball_speed[0] += 1
                    self.play_sound()
                elif self.ball.colliderect(self.enemy):
                    self.ball_speed[0] = -self.ball_speed[0]
                    self.play_sound()


                pygame.draw.rect(self.screen, self.COLORS["red"], self.player)
                pygame.draw.rect(self.screen, self.COLORS["blue"], self.enemy)

                pygame.display.flip()

                for evt in pygame.event.get():
                    if evt.type == QUIT or evt.type == KEYDOWN and evt.key == K_ESCAPE: self.GAME_STATE = False

                fps_index += 1
                if fps_index % 200 == 0: fps += 3
                clock.tick(fps)

        self.__stop()



if __name__ == "__main__":
    app = Game()
    app.run()
