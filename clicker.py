import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import sys

delay = 0.2
button = Button.left
start_stop_key = KeyCode(char='=')
exit_key = KeyCode(char='-')
action_key = KeyCode(char='1')

name ='./actions/action.txt'
if len(sys.argv) > 1:
    name = './actions/' + sys.argv[1]

reading = open(name, "r")
actions = reading.read().split('\n')
a_len = len(actions)
i = 0

class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.a_running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False
    
    def start_action(self):
        self.a_running = True

    def stop_action(self):
        self.a_running = False

    def exit(self):
        self.stop_clicking()
        self.stop_action()
        self.program_running = False

    def run(self):
        global actions, a_len, i
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                time.sleep(self.delay)
            time.sleep(0.1)

            start = mouse.position
            i = 0
            while self.a_running:
                if i < a_len:
                    mouse.click(self.button)
                    time.sleep(0.1)
                    mouse.move(float(actions[i]), 0)
                    time.sleep(float(actions[i + 1]))
                    i += 2
                else:
                    mouse.position = start
                    i = 0

mouse = Controller()
click_thread = ClickMouse(delay, button)
click_thread.start()

def on_press(key):
    if key == start_stop_key:
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
    elif key == action_key:
        if click_thread.a_running:
            click_thread.stop_action()
        else:
            click_thread.start_action()
    elif key == exit_key:
        click_thread.exit()
        listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()