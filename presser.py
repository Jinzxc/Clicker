'''''''''''''''''''''''''''''''''''''''''''''''''''
Jin's Activity Automation

Important Update Notes:
V1.0 - created from action_reader.py (basic presses)
v2.0 - combined mouse and keyboard movements
V3.0 - switched from pynput to pyautogui for pressing

Features:
* Press keys with time intervals
* Paired with the the reader script
* Automated questing

Not completely generalized and will 
not work with everything
'''''''''''''''''''''''''''''''''''''''''''''''''''

import sys, time, threading, pyautogui, math
from pynput.keyboard import Key, Listener, KeyCode
from pynput import mouse as clicker
from pynput.mouse import Button

# constants
delay = 2
button = Button.left
start_stop_key = KeyCode(char='=')
exit_key = KeyCode(char='-')

# variables
go = False
moving = False
active = True

name, other = './kactions/kaction.txt', ''
questing, m_len, a_len = 0, 0, 0

# read in command_line argument (will throw errors if file does not exist)
if len(sys.argv) > 3:
    questing = 1
if len(sys.argv) > 2:
    other = './move/' + sys.argv[2]
    moving = True
if len(sys.argv) > 1:
    name = './kactions/' + sys.argv[1]

reading = open(name, "r")
actions = reading.read().split('\n')

# moving between maps
if moving:
    m_reading = open(other, "r")
    m_actions = m_reading.read().split('\n')
    if questing == 1:
        for i in range(len(m_actions)):
            m_actions[i] = m_actions[i].split(' ')
    else:
        m_actions[0] = m_actions[0].split(' ')
        m_actions[1] = m_actions[1].split(' ')
    m_len = len(m_actions)

a_len = len(actions) - 1
i = 0

# custom sleep function, sleeps in div sections
def sleep(seconds, div):
    parts = float(seconds) / float(div)
    i = 0
    while i < div and go:
        time.sleep(parts)
        i += 1

# custom move then click function
def move_click(location, index, button):
    mouse.position = (
        float(location[index][0]), # x
        float(location[index][1])) # y
    
    time.sleep(0.2)
    mouse.click(button)

# clicking thread (not generalized)
class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        global m_actions, m_len, active, questing
        # count = 0
        while self.program_running:
            while self.running:
                if questing == 1:
                    for j in range(m_len):
                        if self.running:
                            if len(m_actions[j]) > 1:
                                move_click(m_actions, j, self.button)
                                time.sleep(0.5)
                            elif m_actions[j][0] == 's':
                                active = False
                            elif m_actions[j][0] == 'c':
                                active = True
                            else:
                                sleep(float(m_actions[j][0]), math.ceil(float(m_actions[j][0]) / 5))
                        else:
                            break
                    j = 0
                else:
                    sleep(60, 6)
                    active = False
                    # out of room
                    if self.running:
                        move_click(m_actions, 0, self.button)
                    if self.running:
                        sleep(60, 12)
                    if self.running:
                        # into room
                        move_click(m_actions, 1, self.button)
                    active = True
            time.sleep(1)

# pressing thread (generalized)
class PressKey(threading.Thread):
    def __init__(self, delay):
        super(PressKey, self).__init__()
        self.delay = delay
        self.running = False
        self.program_running = True
    
    def start_action(self):
        self.running = True

    def stop_action(self):
        self.running = False

    def exit(self):
        self.stop_action()
        self.program_running = False

    def run(self):
        global actions, a_len, i, active
        while self.program_running:
            i = 0
            while self.running:
                if active:
                    if i < a_len:
                        # pressing comes here
                        pyautogui.press(actions[i])
                        time.sleep(float(actions[i + 1]))
                        i += 2
                    else:
                        i = 0
                else:
                    time.sleep(1)
                    
                    i = 0
            time.sleep(1)
            active = True

press_thread = PressKey(delay)
press_thread.start()

if moving:
    mouse = clicker.Controller()
    click_thread = ClickMouse(delay, button)
    click_thread.start()

# press detection
def on_press(key):
    global go
    if key == start_stop_key:
        if press_thread.running:
            press_thread.stop_action()
            if moving: 
                click_thread.stop_clicking()
            go = False
        else:
            press_thread.start_action()
            if moving:
                click_thread.start_clicking()
            go = True
    elif key == exit_key:
        press_thread.exit()
        if moving:
            click_thread.exit()
        listener.stop()

with Listener(on_press=on_press) as listener:
    listener.join()