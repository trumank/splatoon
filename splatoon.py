#!/usr/bin/env python3

from pynput import mouse, keyboard
import time
import pyautogui
import random
import time

ax = None
ay = None
bx = None
by = None

interval = 1/40 #set no higher than framerate or inputs will be missed and spiders will die

spiders = { # keys are row number and value is a list of indexes are slots with remotes
    6: list(range(10)),
    7: list(range(10)),
}
indexed = []
n = 0
for r,row in spiders.items():
    indexed.append((n, r, row))
    n += len(row)
total = sum([len(v) for v in spiders.values()]) - 1
print(indexed, total)

def randomly(seq):
    shuffled = list(seq)
    random.shuffle(shuffled)
    return iter(shuffled)

def command(ax, ay, bx, by):
    print(ax, ay, bx, by)

    dx = (bx - ax)
    dy = (by - ay)

    pyautogui.PAUSE = interval

    for n,r,indexes in randomly(indexed):
        print('swappted to', str(r))
        pyautogui.hotkey('shift', str(r), interval=interval)
        for s in randomly(indexes):
            px = ax + dx * (n + s) / total
            py = ay + dy * (n + s) / total

            pyautogui.press(str(s+1) if s+1<10 else '0')
            pyautogui.moveTo(px, py)
            pyautogui.mouseDown()
            pyautogui.mouseUp()

    pyautogui.press('q')

def listen():
    global ax, ay, bx, by
    ax = None
    ay = None
    bx = None
    by = None
    with mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll) as listener:
        listener.join()

    time.sleep(0.2)

    command(ax, ay, bx, by)


def on_move(x, y):
    pass

def on_click(x, y, button, pressed):
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    if pressed:
        global ax, ay, bx, by
        if not ax and not ay:
            ax = x
            ay = y
            return True
        if not bx and not by:
            bx = x
            by = y
        if ax and ay and bx and by:
            return False

def on_scroll(x, y, dx, dy):
    pass

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_activate():
    print('Global hotkey activated!')
    listen()

def for_canonical(f):
    return lambda k: f(l.canonical(k))

hotkey = keyboard.HotKey(
    keyboard.HotKey.parse('<ctrl>+r'),
    on_activate)
with keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release)) as l:
    l.join()
