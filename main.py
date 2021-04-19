import pygame

pygame.font.init()  # font
pygame.mixer.init()  # sound

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Aircraft Fight')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
BULLET_HIT_SOUND = pygame.mixer.Sound('assets/Grenade.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('assets/GunSilencer.mp3')
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLET = 10
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# load the gaming planes
YELLOW_SPACESHIP_IMAGE = pygame.image.load('assets/spaceship_yellow.png')
# rotate & scale the IMAGE
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    90)
RED_SPACESHIP_IMAGE = pygame.image.load('assets/spaceship_red.png')
# scale the IMAGE
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    270)

# load the gaming background
SPACE = pygame.transform.scale(pygame.image.load('assets/space.png'), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)  # set up a border in the playing window

    red_health_txt = HEALTH_FONT.render('Health: ' + str(red_health), True, WHITE)
    yellow_health_txt = HEALTH_FONT.render('Health: ' + str(yellow_health), True, WHITE)
    WIN.blit(red_health_txt, (WIDTH - red_health_txt.get_width() - 10, 10))
    WIN.blit(yellow_health_txt, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))  # position of the IMAGE
    WIN.blit(RED_SPACESHIP, (red.x, red.y))  # position of the IMAGE

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(key_pressed, yellow):
    if key_pressed[pygame.K_a] and yellow.x - VEL > 0:  # left
        yellow.x -= VEL

    if key_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # right
        yellow.x += VEL

    if key_pressed[pygame.K_w] and yellow.y - VEL > 0:  # up
        yellow.y -= VEL

    if key_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # down
        yellow.y += VEL


def red_handle_movement(key_pressed, red):
    if key_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # left
        red.x -= VEL

    if key_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # right
        red.x += VEL

    if key_pressed[pygame.K_UP] and red.y - VEL > 0:  # up
        red.y -= VEL

    if key_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # down
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL

        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL

        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(txt):
    draw_txt = WINNER_FONT.render(txt, True, WHITE)
    WIN.blit(draw_txt, (WIDTH // 2 - draw_txt.get_width() // 2, HEIGHT // 2 - draw_txt.get_height() // 2))

    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10,
                                         5)  # set up bullets
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)  # set up bullets
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_txt = ''
        if red_health <= 0:
            winner_txt = 'YELLOW WINS!'

        if yellow_health <= 0:
            winner_txt = 'RED WINS!'

        if winner_txt != '':
            draw_winner(winner_txt)
            break

        key_pressed = pygame.key.get_pressed()
        yellow_handle_movement(key_pressed, yellow)
        red_handle_movement(key_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()


if __name__ == '__main__':
    main()
