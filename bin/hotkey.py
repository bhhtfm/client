import time
import threading
from pynput.keyboard import Key, Listener, Controller

keyboard = Controller()
is_spamming = False

def start_key():
    global is_spamming
    start_time = time.time()
    duration = 10

    while time.time() - start_time < duration and is_spamming:
        keyboard.press(Key.f6)
        keyboard.release(Key.f6)
        time.sleep(0.01)

    is_spamming = False

def on_press(key):
    global is_spamming
    if key == Key.f1:
        keyboard.press(Key.enter)
        keyboard.type("/mort")
        keyboard.press(Key.enter)
    if key == Key.f5:
        keyboard.press(Key.enter)
        keyboard.type("/ping")
        keyboard.press(Key.enter)
    if key == Key.delete:
        keyboard.press(Key.enter)
        keyboard.type("/sala *801")
        keyboard.press(Key.enter)
    elif key == Key.up and not is_spamming:
        is_spamming = True
        spam_thread = threading.Thread(target=start_key)
        spam_thread.start()

with Listener(on_press=on_press) as listener:
    listener.join()
