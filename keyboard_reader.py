import time
from pynput import keyboard
from pynput.keyboard import Listener, KeyCode
import sys

start_stop_key = KeyCode(char='=')
exit_key = KeyCode(char='-')
viable_keys = [KeyCode(char='1'), 
               KeyCode(char='2'), 
               KeyCode(char='3'), 
               KeyCode(char='4'), 
               KeyCode(char='5')]
t = 0
start = True

name ='./kactions/kaction.txt'
if len(sys.argv) > 1:
    name = './kactions/' + sys.argv[1]

f = open(name, "a")
reading = False
    
def on_press(key):
    global reading, start, t
    if key == start_stop_key:
        reading = not reading
    elif key in viable_keys and reading:
        if start:
            t = time.time()
            start = False
        else:
            dt = time.time() - t
            f.write(str(dt) + '\n')
            t = time.time()

        f.write(str(key).replace("'", '') + '\n')
    elif key == exit_key:
        listener.stop()
        del reading
        f.close()

with Listener(on_press=on_press) as listener:
    listener.join()