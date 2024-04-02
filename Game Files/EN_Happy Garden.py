import pgzrun
from random import *
import time

WIDTH = 1500
HEIGHT = 900
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

game_over = False
finalized = False
raining = False
garden_happy = True
fangflower_collision = False

time_elapsed = 0
start_time = time.time()

cow = Actor("pig")
cow.pos = (100, 400)

game_over_actor = Actor("gameover")
game_over_actor.pos = CENTER_X, CENTER_Y

flower_list = []
wilted_list = []
fangflower_list = []
Trex_list = []

fangflower_vy_list = []
fangflower_vx_list = []
Trex_vy_list = []
Trex_vx_list = []


def draw():
    global game_over, time_elapsed, finalized, raining
    if not game_over:
        if not raining:
            screen.blit("garden1500x900", (0, 0))
        else:
            screen.blit("garden-raining1500x900", (0, 0))
        cow.draw()
        for flower in flower_list:
            flower.draw()
        for fangflower in fangflower_list:
            fangflower.draw()
            raining = True
        for Trex in Trex_list:
            Trex.draw()
        time_elapsed = int(time.time() - start_time)
        screen.draw.text("Garden is happy in: " + str(time_elapsed) + " seconds",
                         topleft=(10, 10), color="black")
    else:
        if not finalized:
            cow.draw()
            screen.draw.text("Oops! You lose ",
                             topleft=(10, 30), color="black")
            finalized = True
            clock.schedule(show_game_over, 3.0)  # Schedule show_game_over() after 3 second


def show_game_over():
    screen.clear()
    game_over_actor.draw()
    clock.schedule(restart_game, 5.0)  # Schedule restart_game() after 5 seconds


def restart_game():
    global game_over, finalized, raining, garden_happy, fangflower_collision, time_elapsed
    global flower_list, wilted_list, fangflower_list, Trex_list
    global fangflower_vy_list, fangflower_vx_list, Trex_vy_list, Trex_vx_list
    global start_time

    game_over = False
    finalized = False
    raining = False
    garden_happy = True
    fangflower_collision = False

    time_elapsed = 0
    start_time = time.time()

    cow.pos = (100, 400)
    cow.image = "pig"

    flower_list = []
    wilted_list = []
    fangflower_list = []
    Trex_list = []

    fangflower_vy_list = []
    fangflower_vx_list = []
    Trex_vy_list = []
    Trex_vx_list = []

    add_flowers()
    wilt_flower()


def new_flower():
    global flower_list, wilted_list
    flower_new = Actor("flower")
    flower_new.pos = randint(50, WIDTH - 50), randint(150, HEIGHT - 100)
    flower_list.append(flower_new)
    wilted_list.append("happy")
    return


def add_flowers():
    global game_over
    if not game_over:
        new_flower()
        clock.schedule(add_flowers, 2)
    return


def check_wilt_times():
    global wilted_list, game_over, garden_happy
    if(len(wilted_list)>0):
       for wilted_since in wilted_list:
           if (not wilted_since == "happy"):
               time_wilted = int(time.time() - wilted_since)
               if (time_wilted > 10.0):
                   garden_happy = False
                   game_over = True
                   break
    return


def wilt_flower():
    global flower_list, wilted_list, game_over, raining
    if not game_over:
        if wilted_list:
            rand_flower = randint(0, len(flower_list) - 1)
            if flower_list[rand_flower].image == "flower":
                flower_list[rand_flower].image = "flower-wilt"
                wilted_list[rand_flower] = time.time()
            if not raining:
                clock.schedule(wilt_flower, 3)
            else:
                clock.schedule(wilt_flower, 99)
    return


def check_flower_collision():
    global cow, flower_list, wilted_list, game_over
    index = 0
    for flower in flower_list:
        if flower.colliderect(cow) and flower.image == "flower-wilt":
            flower.image = "flower"
            wilted_list[index] = "happy"
            raining = True
            break
        index += 1
    return


def check_fangflower_collision():
    global cow, fangflower_list, fangflower_collision, game_over
    for fangflower in fangflower_list:
        if fangflower.colliderect(cow):
            cow.image = "zap"
            game_over = True
            break
    return


def check_Trex_collision():
    global cow, Trex_list, Trex_collision, game_over
    for Trex in Trex_list:
        if Trex.colliderect(cow):
            cow.image = "rip"
            game_over = True
            break
    return


def velocity():
    random_dir = randint(0, 1)
    random_velocity = randint(4, 6)
    if random_dir == 0:
        return -random_velocity
    else:
        return random_velocity


def mutate():
    global flower_list, fangflower_list, fangflower_vx_list, fangflower_vy_list, game_over
    if not game_over and flower_list and len(fangflower_list) < 5:
        rand_flower = randint(0, len(flower_list) - 1)
        if rand_flower < len(flower_list):
            fangflower_pos_x = flower_list[rand_flower].x
            fangflower_pos_y = flower_list[rand_flower].y
            del flower_list[rand_flower]
            fangflower = Actor("fangflower")
            fangflower.pos = fangflower_pos_x, fangflower_pos_y
            fangflower_vx = velocity()
            fangflower_vy = velocity()
            fangflower_list.append(fangflower)
            fangflower_vx_list.append(fangflower_vx)
            fangflower_vy_list.append(fangflower_vy)
            clock.schedule(mutate, 15)
    return


def mutate_Trex():
    global flower_list, Trex_list, Trex_vx_list, Trex_vy_list, game_over
    if not game_over and flower_list and len(Trex_list) < 3:
        rand_flower = randint(0, len(flower_list) - 1)
        if rand_flower < len(flower_list):
            Trex_pos_x = flower_list[rand_flower].x
            Trex_pos_y = flower_list[rand_flower].y
            del flower_list[rand_flower]
            Trex = Actor("t_rex")
            Trex.pos = Trex_pos_x, Trex_pos_y
            Trex_vx = velocity()
            Trex_vy = velocity()
            Trex_list.append(Trex)
            Trex_vx_list.append(Trex_vx)
            Trex_vy_list.append(Trex_vy)
            clock.schedule(mutate_Trex, 10)
    return


def update_fangflowers():
    global fangflower_list, game_over, raining
    if not game_over:
        index = 0
        for fangflower in fangflower_list:
            fangflower_vx = fangflower_vx_list[index]
            fangflower_vy = fangflower_vy_list[index]
            fangflower.x += fangflower_vx
            fangflower.y += fangflower_vy
            if fangflower.left < 0:
                fangflower_vx_list[index] = -fangflower_vx
            if fangflower.right > WIDTH:
                fangflower_vx_list[index] = -fangflower_vx
            if fangflower.top < 150:
                fangflower_vy_list[index] = -fangflower_vy
            if fangflower.bottom > HEIGHT:
                fangflower_vy_list[index] = -fangflower_vy
            index += 1
    return


def update_Trexs():
    global Trex_list, game_over, raining
    if not game_over:
        index = 0
        for Trex in Trex_list:
            Trex_vx = Trex_vx_list[index]
            Trex_vy = Trex_vy_list[index]
            Trex.x += Trex_vx
            Trex.y += Trex_vy
            if Trex.left < 0:
                Trex_vx_list[index] = -Trex_vx
            if Trex.right > WIDTH:
                Trex_vx_list[index] = -Trex_vx
            if Trex.top < 150:
                Trex_vy_list[index] = -Trex_vy
            if Trex.bottom > HEIGHT:
                Trex_vy_list[index] = -Trex_vy
            index += 1
    return


def reset_cow():
    global game_over
    if not game_over:
        cow.image = "pig"
    return


add_flowers()
wilt_flower()


def update():
    global score, game_over, fangflower_collision, flower_list, fangflower_list, time_elapsed
    global Trex_collision, Trex_list
    check_wilt_times()
    fangflower_collision = check_fangflower_collision()
    Trex_collision = check_Trex_collision()
    if not game_over:
        if keyboard.space:
            cow.image = "pig-water"
            clock.schedule(reset_cow, 0.5)
            check_flower_collision()
        if keyboard.left and cow.x > 0:
            cow.x -= 5
        if keyboard.right and cow.x < WIDTH:
            cow.x += 5
        if keyboard.up and cow.y > 150:
            cow.y -= 5
        if keyboard.down and cow.y < HEIGHT:
            cow.y += 5
        if keyboard.r:
            raining = True
        if time_elapsed > 15 and not fangflower_list:
            mutate()
        if time_elapsed > 10 and not Trex_list:
            mutate_Trex()

        update_fangflowers()
        update_Trexs()


add_flowers()
wilt_flower()
pgzrun.go()