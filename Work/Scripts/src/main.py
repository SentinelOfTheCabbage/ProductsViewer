from Work.Scripts.src.view.ui.main_window.main_window import MainWindow
from tkinter import Tk
from Work.Scripts import conf

f = open(conf.ROOT_DIR + r'\Data\Temp\filename.txt', 'w')
f.write(conf.ROOT_DIR + r'\Data\db.pickle')
f.close()
MainWindow(Tk(), "База данных продуктов")

