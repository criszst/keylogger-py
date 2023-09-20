import socket
import platform

import requests
import win32api
import os
def infoPc():
    listI = f"""
        Sistema: {platform.system()}
        Processador: {platform.processor()}
        Arquitetura: {platform.architecture()}
        Host Name: {socket.gethostname()}
        User: {os.getlogin()}
        Ip Privado: {socket.gethostbyname(socket.gethostname())}
        Ip Publico: {requests.get('https://api.ipify.org').text}
        Volume: {win32api.GetVolumeInformation("C://")}
    """

    return listI