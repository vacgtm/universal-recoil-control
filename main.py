from modules.move_mouse import main
import os, time, threading 
from pynput import keyboard
from pynput import mouse
from pynput.mouse import Controller, Button
from modules.readjson import read_json
c = mouse.Controller()

class universal_recoil:
    def __init__(self, xval, yval, speed, toggled, key, left_is_pressed, right_is_pressed, hipfire_mode, hipfire_xval, hipfire_yval, hipfire_speed):
        self.xval = xval
        self.yval = yval 
        self.speed = speed
        self.toggled = toggled
        self.key = key
        self.left_is_pressed = left_is_pressed
        self.right_is_pressed = right_is_pressed
        self.hipfire_mode = hipfire_mode
        self.hipfire_xval = hipfire_xval
        self.hipfire_yval = hipfire_yval 
        self.hipfire_speed = hipfire_speed



    def recoil_comp(self):
        while True:
            if self.hipfire_mode == "True":
                if self.toggled and self.left_is_pressed:
                    main(self.hipfire_xval, self.hipfire_yval)
                    time.sleep(self.hipfire_speed)
                else:
                    time.sleep(0.01)
            elif self.hipfire_mode == "False":
                if self.toggled and self.left_is_pressed and self.right_is_pressed:
                    main(self.xval, self.yval)
                    time.sleep(self.speed)
                else:
                    time.sleep(0.01)


    
    def on_press(self, key):
        if key == keyboard.KeyCode.from_char(self.key):
            print('pressed')
            self.toggled = not self.toggled
    
    def on_click(self, x, y, button, pressed):
        if button == Button.left:
            if self.toggled:
                self.left_is_pressed = pressed
        
        if button == Button.right:
            if self.toggled:
                self.right_is_pressed = pressed






main_instance =  universal_recoil( 
    xval=read_json("configuration/config.json", "xval"),
    yval=read_json("configuration/config.json", "yval"),
    speed=read_json("configuration/config.json", "speed"),
    toggled=False,
    key=read_json("configuration/config.json", "key"),
    left_is_pressed=False,
    right_is_pressed=False,
    hipfire_mode=read_json("configuration/hipfire.json", "hipfire_mode"),
    hipfire_xval=read_json("configuration/hipfire.json", "hipfire_xval"),
    hipfire_yval=read_json("configuration/hipfire.json", "hipfire_yval"),
    hipfire_speed=read_json("configuration/hipfire.json", "hipfire_speed")
)


threading.Thread(target=main_instance.recoil_comp, daemon=True).start()
kb_thread = keyboard.Listener(on_press=main_instance.on_press)
mouse_thread = mouse.Listener(on_click=main_instance.on_click)
kb_thread.start()
mouse_thread.start()
while True:
    time.sleep(0.1)
