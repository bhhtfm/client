import time
import json
import random
from pynput.keyboard import Key, Listener, Controller

keyboard = Controller()

with open('vanilla.json', 'r') as file:
    data = json.load(file)

rooms = [item for item in data if item['num_players'] > 10]

def on_press(key):
    if key == Key.f1:
        keyboard.press(Key.enter)
        keyboard.type("/mort")
        keyboard.press(Key.enter)

    if key == Key.f5:
        keyboard.press(Key.enter)
        keyboard.type("/ping")
        keyboard.press(Key.enter)

    if key == Key.end:
        keyboard.press(Key.enter)
        keyboard.type("/sala *801")
        keyboard.press(Key.enter)

    if key == Key.delete:
        room_name = random.choice(rooms)['name']
        keyboard.press(Key.enter)
        keyboard.type(f"/sala {room_name}")
        keyboard.press(Key.enter)

with Listener(on_press=on_press) as listener:
    listener.join()
