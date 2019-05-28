import sys

from tkinter import Tk
from Work.Scripts import conf
from Work.Scripts.main_window import MainWindow

f = open(conf.ROOT_DIR + r'\Data\filename.txt', 'w')
f.write(conf.ROOT_DIR + r'\Data\db.pickle')
f.close()
sys.path.insert(0, "D:\\Python projects\\ProductsViewer\\Work\\Scripts")
MainWindow(Tk(), "База данных продуктов")

