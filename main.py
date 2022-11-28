import threading
import time
import segno
import os,sys
import os.path
from sys import platform
from PIL import Image
from pynput import keyboard
from flask import Flask, render_template, send_file
import socket
currently_pressed = set()
clipboard_glob = None
flag = False


def kill_app():
    time.sleep(20)
    os._exit(0)


def flaskstuff(clipboard):
    base_dir = '.'
    if hasattr(sys, '_MEIPASS'):
        base_dir = os.path.join(sys._MEIPASS)
    app = Flask(__name__,
        template_folder=os.path.join(base_dir, 'templates'))



    @app.route("/")
    def hello_world():
        return render_template('index.html')

    @app.route('/download')
    def download():
        path = clipboard

        thread = threading.Thread(target=kill_app)
        thread.start()
        return send_file(path, as_attachment=True)

    app.run(debug=True,use_reloader=False,host='0.0.0.0')


def checkforfile(clipboard):
    checkmark = os.path.isfile(clipboard)
    return checkmark

def getqrlinux():
    try:
        import tkinter
    except ImportError:
        pass
    root = tkinter.Tk()
    clipboard = root.selection_get(selection="CLIPBOARD")
    global clipboard_glob
    clipboard_glob = clipboard
    if not checkforfile(clipboard):
        qrcode = segno.make(clipboard,micro=False)
        qrcode.save('Clipboard.png',scale = 10)
        qrpic = Image.open("Clipboard.png")
        qrpic.show()
    else:
        global flag
        flag = True
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        IPAddr += ':5000'
        IPAddr = 'http://'+IPAddr
        qrcode = segno.make(IPAddr,micro=False)
        qrcode.save('Clipboard.png', scale=10)
        qrpic = Image.open("Clipboard.png")
        qrpic.show()
        return

def on_press(key):
    combination = {keyboard.Key.ctrl,keyboard.Key.alt,keyboard.KeyCode(char='q')}

    is_pressed = False
    if key in combination:
        currently_pressed.add(key)


    if currently_pressed == combination:
        is_pressed = True
        getqrlinux()
        return False



if __name__ == "__main__":

    if platform == "linux" or platform == "linux2":
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
        listener.join()
        if flag:
            flaskstuff(clipboard_glob)
    elif platform == "darwin":
        print("Nobody loves you")
    elif platform == "win32":
        print("Wrong PLatfrom Bro")
