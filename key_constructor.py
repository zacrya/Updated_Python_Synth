from PySide6.QtCore import QRect
from PySide6.QtWidgets import QPushButton, QWidget
from oscillator import Oscillator

def get_wkey(key):
    var = key
    text = str(u"#c4{\n"
    "background-color: rgb(255, 255, 255);\n"
    "background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:0.861709, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255))\n"
    "}\n"
    "\n"
    "#c4:pressed{\n"
    "background-color: rgb(250, 250, 250);\n"
    "}\n"
    "")
    text = text.replace('c4', var)

    return text

def get_bkey(key):
    var = key
    text = str(u"#c4{\n"
    "background-color: rgb(0, 0, 0);\n"
    "background-color: qlineargradient(spread:pad, x1:0.738916, y1:0.0681818, x2:0.985222, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255))\n"
    "}\n"
    "\n"
    "#c4:pressed{\n"
    "background-color: rgb(0, 0, 0);\n"
    "}\n"
    "")
    text = text.replace('c4', key)

    return text

class octave(QWidget):
    def __init__(self, window):
        super().__init__()
        self.setParent(window)

        
        for i in keys:
            wkey = get_wkey(i)
            self.i = key(window, name=str(i))
            if len(self.i.name) == 3:
                self.i.raise_()

keys = {
    'c4':{'style':str(get_wkey('c4')), 'coord': QRect(30, 160, 50, 190), 'pitch':0},
    'd4':{'style':get_wkey('d4'), 'coord': QRect(80, 160, 50, 190), 'pitch':2},
    'e4':{'style':get_wkey('e4'), 'coord': QRect(130, 160, 50, 190), 'pitch':4},
    'f4':{'style':get_wkey('f4'), 'coord': QRect(180, 160, 50, 190), 'pitch':5},
    'g4':{'style':get_wkey('g4'), 'coord': QRect(230, 160, 50, 190), 'pitch':7},
    'a4':{'style':get_wkey('a4'), 'coord': QRect(280, 160, 50, 190), 'pitch':9},
    'b4':{'style':get_wkey('b4'), 'coord': QRect(330, 160, 50, 190), 'pitch':11},
    'c40':{'style':get_bkey('c40'), 'coord': QRect(60, 160, 40, 100), 'pitch':1},
    'd40':{'style':get_bkey('d40'), 'coord': QRect(110, 160, 40, 100), 'pitch':3},
    'f40':{'style':get_bkey('f40'), 'coord': QRect(210, 160, 40, 100), 'pitch':6},
    'g40':{'style':get_bkey('g40'), 'coord': QRect(260, 160, 40, 100), 'pitch':8},
    'a40':{'style':get_bkey('a40'), 'coord': QRect(310, 160, 40, 100), 'pitch':10},
}

class key(QPushButton):
    def __init__(self, window, name):
        super().__init__()
        self.name = name
        self.setParent(window)
        self.setObjectName(name)
        self.setGeometry(keys[name]['coord'])
        self.setStyleSheet(keys[name]['style'])
        #self.clicked.connect(lambda: button_clicked(keys[name]['pitch']))
        self.pressed.connect(lambda: button_clicked(keys[name]['pitch']))
        self.released.connect(lambda: button_released())

osc = Oscillator()

def button_clicked(key):
    osc.set_pitch(key)
    osc.play()

def button_released():
    osc.stop()
