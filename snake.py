from config import config
from time import sleep
import psycopg2
import random
import pygame as pg

conn, cur = None, None
pg.init()
size_block = 20
color_block1 = (255, 165, 0)
color_block2 = (245, 222, 179)
WHITE = (255, 255, 255)
COLOR2 = (255, 255, 0)
BLACK = (0, 0, 0)
snake_color = (23, 114, 69)
count_block = 20
margin = 1
margin2 = 70
speed = 3
level = 1

size = [size_block * count_block + 2 * size_block + margin * count_block,
        size_block * count_block + 2 * size_block + margin * count_block + margin2]
screen = pg.display.set_mode(size)

pg.display.set_caption("SNAKE")
timer = pg.time.Clock()
text = pg.font.SysFont('ariel', 36)
timer_interval = 10000
timer_event = pg.USEREVENT + 1
pg.time.set_timer(timer_event, timer_interval)


class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def border(self):
        return 0 <= self.x < size_block and 0 <= self.y < size_block

    def __eq__(self, other):
        return isinstance(other, Snake) and self.x == other.x and self.y == other.y


def get_random():
    x = random.randint(0, count_block - 1)
    y = random.randint(0, count_block - 1)
    apple_block = Snake(x, y)
    while apple_block in snake_blocks or apple_block in walls:
        apple_block.x = random.randint(0, count_block - 1)
        apple_block.y = random.randint(0, count_block - 1)
    return apple_block


def draw_blocks(color, row, column):
    pg.draw.rect(screen, color, [size_block + column * size_block + margin * (column + 1),
                                 margin2 + size_block + row * size_block + margin * (row + 1),
                                 size_block, size_block])


walls = []
snake_blocks = [Snake(9, 9), Snake(9, 10)]
apple = get_random()
apple_weight = random.randint(1, 3)
d_row = 0
d_col = 1
score = 0
pause = False

try:
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    create_script = ''' CREATE TABLE IF NOT EXISTS snake (
        username varchar(20) NOT NULL,
        level int,
        score int) '''

    cur.execute(create_script)
    username = input('Enter your username: ')
    sleep(2)

    user_insert = ''' INSERT INTO snake (username, level, score)
                    VALUES (%s, %s, %s) '''
    existing = ''' SELECT * FROM snake WHERE username = %s '''

    cur.execute(existing, [username])
    result = cur.fetchone()

    if result:
        level = int(result[1])
        score = int(result[2])

    else:
        cur.execute(user_insert, (username, 1, 0))

    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    pause = not pause
                    if pause:
                        user = ''' UPDATE snake SET level = %s WHERE username = %s '''
                        cur.execute(user, (level, username))
                        user = ''' UPDATE snake SET score = %s WHERE username = %s '''
                        cur.execute(user, (score, username))

            elif event.type == pg.KEYUP:
                if event.key == pg.K_UP and d_col != 0:
                    d_row = -1
                    d_col = 0

                elif event.key == pg.K_DOWN and d_col != 0:
                    d_row = 1
                    d_col = 0

                elif event.key == pg.K_RIGHT and d_row != 0:
                    d_row = 0
                    d_col = 1

                elif event.key == pg.K_LEFT and d_row != 0:
                    d_row = 0
                    d_col = -1

            elif event.type == timer_event:
                apple = get_random()
                apple_weight = random.randint(1, 3)

        if pause:
            continue

        screen.fill(WHITE)

        pg.draw.rect(screen, COLOR2, [0, 0, size[0], margin2])
        text_score = text.render(f"SCORE: {score}", 0, snake_color)
        text_speed = text.render(f"LEVEL: {level}", 0, snake_color)
        screen.blit(text_score, (count_block, count_block))
        screen.blit(text_speed, (count_block + 250, count_block))

        for row in range(count_block):
            for column in range(count_block):
                if (row + column) % 2 == 0:
                    color = color_block2
                else:
                    color = color_block1
                draw_blocks(color, row, column)

        head = snake_blocks[-1]

        if not head.border():
            exit()

        if level == 1:
            walls = [Snake(2, 1), Snake(2, 2), Snake(2, 3), Snake(2, 4), Snake(2, 5)]

        elif level == 2:
            walls = [Snake(2, 1), Snake(2, 2), Snake(2, 3), Snake(2, 4), Snake(2, 5), Snake(7, 10), Snake(7, 11),
                     Snake(7, 12),
                     Snake(7, 13), Snake(7, 14)]

        else:
            walls = [Snake(2, 1), Snake(2, 2), Snake(2, 3), Snake(2, 4), Snake(2, 5), Snake(7, 10), Snake(7, 11),
                     Snake(7, 12),
                     Snake(7, 13), Snake(7, 14), Snake(12, 5), Snake(13, 4), Snake(12, 6), Snake(18, 9), Snake(5, 19),
                     Snake(6, 12)]

        for wall in walls:
            draw_blocks(BLACK, wall.x, wall.y)

        draw_blocks('red', apple.x, apple.y)

        for block in snake_blocks:
            draw_blocks(snake_color, block.x, block.y)

        if head == apple:
            score += apple_weight
            if score >= level * 5:
                speed += 3
                level += 1
            snake_blocks.append(apple)
            apple = get_random()
            apple_weight = random.randint(1, 3)
            timer_event = pg.USEREVENT + 1
            pg.time.set_timer(timer_event, timer_interval)

        if head in walls:
            exit()

        head = snake_blocks[-1]
        new_head = Snake(head.x + d_row, head.y + d_col)

        if new_head in snake_blocks:
            exit()
        snake_blocks.append(new_head)
        snake_blocks.pop(0)
        pg.display.flip()
        timer.tick(speed)
        conn.commit()

except(Exception, psycopg2.DatabaseError) as error:
    print(error)

finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()