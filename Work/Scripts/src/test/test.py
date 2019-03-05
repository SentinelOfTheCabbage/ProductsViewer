from tkinter import Tk, Button

root = Tk()
for i in range(3_000):
    btn = Button(root, text=str(i))
    btn.place(x=0, y=0)
    print(i)
root.mainloop()
