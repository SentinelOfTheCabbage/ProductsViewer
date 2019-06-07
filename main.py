from tkinter import Tk
from Work.Scripts import conf
from Work.Scripts.main_window import MainWindow

f = open(conf.ROOT_DIR + r'\Data\filename.txt', 'w')
f.write(conf.ROOT_DIR + r'\Data\db.pickle')
f.close()
MainWindow(Tk(), "База данных продуктов")