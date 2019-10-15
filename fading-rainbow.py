from sense_hat import SenseHat
from random import randint
from time import sleep
import math

sense = SenseHat()

sense.clear()

sleep(1)

frequency = 0.2

while True:
        for x in range(255):
                red = int(math.sin(frequency*x + 0) * 127 + 128)
                green = int(math.sin(frequency*x + 2) * 127 + 128)
                blue = int(math.sin(frequency*x + 4) * 127 + 128)

                sense.clear(red,green,blue)
                sleep(0.05)
