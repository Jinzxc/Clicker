import time
from pynput import keyboard
from pynput.mouse import Listener, Controller
import sys

start_stop_key = keyboard.KeyCode(char='=')
exit_key = keyboard.KeyCode(char='-')

name ='./actions/action.txt'
moving = False

if len(sys.argv) > 2:
    if sys.argv[1] == 'move':
        name = './move/' + sys.argv[2]
        moving = True
elif len(sys.argv) > 1:
    name = './actions/' + sys.argv[1]

f = open(name, "a")
reading = False
pos, t = 0, 0

mouse = Controller()
    
def on_press(key):
    global reading, pos
    if key == start_stop_key:
        reading = not reading
        pos = 0
    elif key == exit_key:
        k_listener.stop()
        m_listener.stop()
        del reading, pos
        f.close()

def on_click(x, y, button, pressed):
    global pos, t
    if pressed and reading:
        if moving:
                f.write(str(x) + ' ' + str(y) + '\n')
        else:
            if pos == 0:
                pos = x
                t = time.time()
            elif pressed and reading:
                dx = x - pos
                f.write(str(dx) + '\n')
                pos = x

                dt = time.time() - t
                f.write(str(dt) + '\n')
                t = time.time()

k_listener = keyboard.Listener(on_press=on_press)
k_listener.start()

with Listener(on_click=on_click) as m_listener:
    m_listener.join()
