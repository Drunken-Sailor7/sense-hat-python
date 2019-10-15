from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from time import sleep
from time import time
import math
from random import randint
import sys
import os

sense = SenseHat()

#x and y position of the movable pixel
x = int(0)
y = int(0)

#declares colours of pixel to be used
r = int(0)
g = int(0)
b = int(255)

xycoordsgood = int(1)

#checks if destination xy coords are on the 8x8 grid
def check(destinationx,destinationy):

    global xycoordsgood

    if destinationx > 7 or destinationx < 0:
        xycoordsgood = 0
        red_flash()
        return

    if destinationy > 7 or destinationy < 0:
        xycoordsgood = 0
        red_flash()
        return

def red_flash():

    global x,y,r,g,b
    sense.clear(255,0,0)
    sleep(0.3)
    sense.clear()
    draw_targets()
    sense.set_pixel(x,y,r,g,b)

def up():

    global x,y,r,g,b

    check(x,y-1)

    if xycoordsgood == 0:
        print("You cannot move off the 8x8 grid")
        return

    elif xycoordsgood == 1:
        sense.set_pixel(x,y,0,0,0)
        y -= 1
        sense.set_pixel(x,y,r,g,b)

def down():

    global x,y,r,g,b

    check(x,y+1)

    if xycoordsgood == 0:
        print("You cannot move off the 8x8 grid")
        return

    elif xycoordsgood == 1:
        sense.set_pixel(x,y,0,0,0)
        y += 1
        sense.set_pixel(x,y,r,g,b)

def left():

    global x,y,r,g,b

    check(x-1,y)

    if xycoordsgood == 0:
        print("You cannot move off the 8x8 grid")
        return

    elif xycoordsgood == 1:
        sense.set_pixel(x,y,0,0,0)
        x -= 1
        sense.set_pixel(x,y,r,g,b)

def right():

    global x,y,r,g,b

    check(x+1,y)

    if xycoordsgood == 0:
        print("You cannot move off the 8x8 grid")
        return

    elif xycoordsgood == 1:
        sense.set_pixel(x,y,0,0,0)
        x += 1
        sense.set_pixel(x,y,r,g,b)

#checks if snake has moved onto same square as a target and removes target if it has
def eat_target():
    global chosen_coords,x,y

    for count in range(len(chosen_coords)): #checks each set of 3 coords against current coords
        if count % 2 == 0:
            check_x = chosen_coords[count]

        elif count % 2 != 0:
            check_y = chosen_coords[count]

            #if a target's xy coords match the current xy coords, delete the coordinates from the list so it will not be generated again
            if check_x == x and check_y == y:
                del chosen_coords[count]
                del chosen_coords[count-1]
                break

def direction(direction):

    if direction == "up":
        up()
        return

    if direction == "down":
        down()
        return

    if direction == "left":
        left()
        return

    if direction == "right":
        right()
        return

    if direction == "middle":
        restart_game()

def restart_game():
    os.execl(sys.executable, sys.executable, * sys.argv)

def create_targets():
    generate_targets()
    draw_targets()

def generate_targets():
    global chosen_coords

    chosen_coords = []

    while len(chosen_coords) < 6: #generates 2 for each: one for x and one for y
        random_coord = randint(0,7)

        if random_coord not in chosen_coords: #makes sure that only  unique numbers are appended to the list
            chosen_coords.append(random_coord)

def draw_targets():

    targetr = 0
    targetg = 255
    targetb = 0

    for count in range(len(chosen_coords)):
        if count % 2 == 0:
            x_pos = chosen_coords[count]

        elif count % 2 != 0:
            y_pos = chosen_coords[count]

            sense.set_pixel(x_pos,y_pos,targetr,targetg,targetb)

def win_game():
    global chosen_coords

    if len(chosen_coords) == 0: #if list is empty, then all coords must have been removed so all targets have been eaten
        sleep(0.5)
        sense.clear()
        sense.show_message("You win!",scroll_speed=0.05)
        sys.exit()

sense.clear()

create_targets()

sense.set_pixel(x,y,r,g,b)

while True:
    for event in sense.stick.get_events(): #wait for joystick input
        if event.action == ACTION_PRESSED:
            direction(event.direction)
            eat_target()
            win_game()
            xycoordsgood = 1
