import pygame
import os
pygame.font.init()
pygame.mixer.init()

# window dimension and values
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("space shooter")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLET = 3
YELLOW_HIT = pygame.USEREVENT+1
RED_HIT = pygame.USEREVENT+2

# sound and font
BORDER = pygame.Rect((WIDTH//2)-5, 0, 10, HEIGHT)
SCORE_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

# image spaceship and background
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
YELLOW_SPACESHIP_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png')),
                                                (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP_IMAGE, 90)
RED_SPACESHIP_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'spaceship_red.png')),
                                             (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP_IMAGE, 270)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(yellow, red, yellow_bullet, red_bullet, red_health, yellow_health, winner_text):
    # space background
    WIN.blit(SPACE, (0, 0))

    # draw border
    pygame.draw.rect(WIN, BLACK, BORDER)

    # draw score text
    red_health_text = SCORE_FONT.render('Health: '+str(red_health), True, WHITE)
    yellow_health_text = SCORE_FONT.render('Health: ' + str(yellow_health), True, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # draw spaceship
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    # draw bullets
    for bullet in yellow_bullet:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in red_bullet:
        pygame.draw.rect(WIN, RED, bullet)

    # winner text
    winner_message = WINNER_FONT.render(winner_text, True, WHITE)
    WIN.blit(winner_message, (WIDTH//2 - winner_message.get_width()//2, HEIGHT//2 - winner_message.get_height()//2))

    # must use it update the display
    pygame.display.update()


def yellow_control(control_keys, yellow):
    if control_keys[pygame.K_a] and yellow.x-VEL >= 0:  # left
        yellow.x -= VEL
    if control_keys[pygame.K_d] and yellow.x+VEL+SPACESHIP_WIDTH < BORDER.x:  # right
        yellow.x += VEL
    if control_keys[pygame.K_w] and yellow.y-VEL >= 0:  # up
        yellow.y -= VEL
    if control_keys[pygame.K_s] and yellow.y+VEL+SPACESHIP_HEIGHT+17 <= HEIGHT:  # down
        yellow.y += VEL


def red_control(control_keys, red):
    if control_keys[pygame.K_LEFT] and red.x-VEL > BORDER.x + BORDER.width:  # left
        red.x -= VEL
    if control_keys[pygame.K_RIGHT] and red.x+VEL+SPACESHIP_WIDTH < WIDTH:  # right
        red.x += VEL
    if control_keys[pygame.K_UP] and red.y-VEL >= 0:  # up
        red.y -= VEL
    if control_keys[pygame.K_DOWN] and red.y+VEL+SPACESHIP_HEIGHT+17 <= HEIGHT:  # down
        red.y += VEL


def bullet_handle_control(yellow_bullet, red_bullet, yellow, red):
    for bullet in yellow_bullet:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):  # if bullet collide with red spaceship
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullet.remove(bullet)
        if bullet.x+bullet.width > WIDTH:
            yellow_bullet.remove(bullet)

    for bullet in red_bullet:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):  # if bullet collide with yellow spaceship
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullet.remove(bullet)
        if bullet.x < 0:
            red_bullet.remove(bullet)


def main():
    yellow = pygame.Rect(100, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    clock = pygame.time.Clock()
    yellow_bullet = []
    red_bullet = []
    yellow_health = 10
    red_health = 10
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullet) < MAX_BULLET:
                    bullet = pygame.Rect(yellow.x+yellow.width-15, yellow.y+yellow.height//2+4, 10, 5)
                    yellow_bullet.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullet) < MAX_BULLET:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2+4, 10, 5)
                    red_bullet.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if winner_text != "":
            draw_window(yellow, red, yellow_bullet, red_bullet, red_health, yellow_health, winner_text)
            pygame.time.delay(5000)
            break

        control_keys = pygame.key.get_pressed()
        yellow_control(control_keys, yellow)
        red_control(control_keys, red)
        bullet_handle_control(yellow_bullet, red_bullet, yellow, red)
        draw_window(yellow, red, yellow_bullet, red_bullet, red_health, yellow_health, winner_text)

    main()


if __name__ == "__main__":
    main()
