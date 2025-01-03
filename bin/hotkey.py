import time
import json
from pynput.keyboard import Key, Listener, Controller

keyboard = Controller()

# GET ROOM FROM FILE
with open('vanilla.json', 'r') as file:
    data = json.load(file)

rooms = [item for item in data if item['num_players'] > 10]

# HOTKEY
room_index = 0

def on_press(key):
    global room_index

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
        if room_index > len(rooms):
            room_index = 0

        room_name = rooms[room_index]['name']
        keyboard.press(Key.enter)
        keyboard.type(f"/sala {room_name}")
        keyboard.press(Key.enter)
        room_index += 1

with Listener(on_press=on_press) as listener:
    listener.join()  
