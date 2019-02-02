from tkinter import *
import tkinter.font as tkfont

clicks_last_ch = 0
clicks_filtr = 0
clicks_table = 0
win_w_now = 650
win_h_now = 450
bd_array = [
    ["Макс", "Озирный"],
    ["Виталий", "Перятин"],
    ["Андрей", "Федоров"],
    ["Наиль", "Сулейманов"]
    ]
col = len(bd_array[0])
row = len(bd_array)


def resize(event):
    global win_w_now
    global win_h_now
    global clicks_last_ch
    global clicks_filtr
    global clicks_table
    if win_w_now != root.winfo_width() or win_h_now != root.winfo_height():
        win_w_now = root.winfo_width()
        win_h_now = root.winfo_height()
        if clicks_filtr == 1 or clicks_table == 1:
            main_lab.place(width=win_w_now - 27-100)
        else:
            main_lab.place(width=win_w_now - 27)
        if clicks_last_ch == 1:
            btn_last_ch.config(text="Последние изменения ↓")
            last_ch.place(y=win_h_now - win_h_now * 0.4-26)
            main_lab.place(height=0.6*win_h_now-28)
            if clicks_filtr == 1:
                filtr_lab.place(x=win_w_now - 125, height=0.6*win_h_now-27)
            else:
                filtr_lab.place(x=win_w_now)
            if clicks_table == 1:
                table_lab.place(x=win_w_now - 125, height=0.6*win_h_now-27)
            else:
                table_lab.place(x=win_w_now)
        else:
            btn_last_ch.config(text="Последние изменения ↑")
            last_ch.place(y=win_h_now)
            main_lab.place(height=win_h_now - 28)
            if clicks_filtr == 1:
                filtr_lab.place(x=win_w_now - 125, height=win_h_now-27)
            else:
                filtr_lab.place(x=win_w_now)
            if clicks_table == 1:
                table_lab.place(x=win_w_now - 125, height=win_h_now-27)
            else:
                table_lab.place(x=win_w_now)


def new_win():
    filtr = Tk()
    filtr.title("name")
    filtr.iconbitmap("img.ico")
    new_win_w = 300
    new_win_h = 200
    filtr.geometry("{winw}x{winh}+{centerw}+{centerh}".format(
        winw=new_win_w,
        winh=new_win_h,
        centerw=(filtr.winfo_screenwidth() - new_win_w) // 2,
        centerh=(filtr.winfo_screenheight() - new_win_h - 30) // 2))
    filtr.resizable(False, False)


def click_filtr(event):
    global clicks_table
    clicks_table = 0
    table_lab.place(x=win_w_now)
    global clicks_filtr
    clicks_filtr += 1
    if clicks_filtr == 1:
        main_lab.place(width=win_w_now - 27 - 100)
        if clicks_last_ch == 1:
            filtr_lab.place(x=win_w_now - 125, height=0.6 * win_h_now - 27)
        else:
            filtr_lab.place(x=win_w_now - 125, height=win_h_now - 27)
    else:
        main_lab.place(width=win_w_now - 27)
        filtr_lab.place(x=win_w_now)
        clicks_filtr = 0


def click_table(event):
    global clicks_filtr
    clicks_filtr = 0
    filtr_lab.place(x=win_w_now)
    global clicks_last_ch
    global clicks_table
    clicks_table += 1
    if clicks_table == 1:
        main_lab.place(width=win_w_now - 27 - 100)
        if clicks_last_ch == 1:
            table_lab.place(x=win_w_now - 125, height=0.6 * win_h_now - 27)
        else:
            table_lab.place(x=win_w_now - 125, height=win_h_now - 27)
    else:
        main_lab.place(width=win_w_now - 27)
        table_lab.place(x=win_w_now)
        clicks_table = 0


def click_last_ch(event):
    global clicks_table
    global clicks_filtr
    global clicks_last_ch
    clicks_last_ch += 1
    if clicks_last_ch == 1:
        btn_last_ch.config(text="Последние изменения ↓")
        last_ch.place(y=win_h_now-win_h_now*0.4-26)
        main_lab.place(height=0.6*win_h_now-28)
        if clicks_filtr == 1:
            filtr_lab.place(x=win_w_now - 125, height=0.6 * win_h_now - 27)
        else:
            filtr_lab.place(x=win_w_now)
        if clicks_table == 1:
            table_lab.place(x=win_w_now - 125, height=0.6 * win_h_now - 27)
        else:
            table_lab.place(x=win_w_now)
    else:
        btn_last_ch.config(text="Последние изменения ↑")
        last_ch.place(y=win_h_now)
        main_lab.place(height=win_h_now-28)
        if clicks_filtr == 1:
            filtr_lab.place(x=win_w_now - 125, height=win_h_now - 27)
        else:
            filtr_lab.place(x=win_w_now)
        if clicks_table == 1:
            table_lab.place(x=win_w_now - 125, height=win_h_now - 27)
        else:
            table_lab.place(x=win_w_now)
        clicks_last_ch = 0


root = Tk()
root.title("База данных продуктов")
root.iconbitmap("img.ico")
win_w_start = 650
win_h_start = 450
root.geometry("{winw}x{winh}+{centerw}+{centerh}".format(
    winw=win_w_start,
    winh=win_h_start,
    centerw=(root.winfo_screenwidth()-win_w_start)//2,
    centerh=(root.winfo_screenheight()-win_h_start-30)//2))
root.resizable(True, True)
root.minsize(win_w_start, win_h_start-20)

main_lab = Label(root, bg="#fff", bd=3)
main_lab.place(width=win_w_now-27, height=win_h_now-48)

main_lab2 = Label(main_lab, bg="#000", bd=3)
main_lab2.place(relx=0.5, rely=0.5, anchor="c")
for r in range(row):
    for c in range(col):
        btn = Label(main_lab2, bg="#000")
        btn.grid(row=r, column=c, ipadx=10, ipady=6, padx=10, pady=10)
        btn2 = Label(btn, width=10, bg="#fff", bd=2, fg="#000",
                     text="{}".format(bd_array[r][c]))
        btn2.pack(expand=True, fill=BOTH)

last_ch = Label(root, bg='#fff', bd=0)
last_ch.place(x=0, y=win_h_now-200, relwidth=1.0, relheight=0.4)

btn_last_ch = Button(root, text="Последние изменения ↑", bg="red", anchor="w")
btn_last_ch.bind("<Button-1>", click_last_ch)
btn_last_ch.pack(side=BOTTOM, fill=X)

label_last_ch = Label(last_ch, justify=LEFT, text="тут последние изменения",
                      bg="blue", fg="white")
label_last_ch.place(x=0, y=0, relwidth=1.0, relheight=1.0)

main_menu = Menu()

menu_menu = Menu(tearoff=0, bg="#fff")
menu_menu.add_command(label="Найти")
menu_menu.add_command(label="Выбрать")
menu_menu.add_command(label="Выбрать всё")
menu_menu.add_command(label="Назад")
menu_menu.add_command(label="Вперёд")
menu_menu.add_command(label="Помощь")
menu_menu.add_command(label="Об авторах")
menu_menu.add_separator()
menu_menu.add_command(label="Выход")

changeBD_menu = Menu(tearoff=0, bg="#fff")
changeBD_menu.add_command(label="Новая БД")
changeBD_menu.add_command(label="Редактировать БД")
changeBD_menu.add_command(label="Открыть БД")
changeBD_menu.add_command(label="Сохранить")
changeBD_menu.add_command(label="Сохранить как...")

otchet_menu = Menu(tearoff=0, bg="#fff")
otchet_menu.add_command(label="Простой отчёт")
otchet_menu.add_command(label="Статистика")
otchet_menu.add_command(label="Сводная таблица")
otchet_menu.add_command(label="Столбчатая диаграмма")
otchet_menu.add_command(label="Гистограмма")
otchet_menu.add_command(label="Диаграмма Босо-Вискеря")
otchet_menu.add_command(label="Диаграмма рассеивания")

right_menu = Label(root, bg='#fff', bd=1, width="3")
right_menu.pack(side=RIGHT, fill=Y)

filtr_lab = Label(root, bg="red", bd=0)
filtr_lab.place(x=win_w_now, y=0, width=100, height=0.6*win_h_now-27)

font = tkfont.nametofont("TkMenuFont")

filtr_btn = Canvas(right_menu, height=50, width=20, bd=1, bg="red")
filtr_btn.bind("<Button-1>", click_filtr)
filtr_btn.create_text((20, 50), angle="-90", anchor="ne", text="фильтр")
filtr_btn.place(x=0, y=0)

table_lab = Label(root, bg="blue", bd=0)
table_lab.place(x=win_w_now, y=0, width=100, height=win_h_now-27)

table_btn = Canvas(right_menu, height=55, width=20, bd=1, bg="blue")
table_btn.bind("<Button-1>", click_table)
table_btn.create_text((20, 55), angle="-90", anchor="ne", text="таблицы",
                      font=font, fill="SystemButtonText")
table_btn.place(x=0, y=54)

main_menu.add_cascade(label="Меню", menu=menu_menu)
main_menu.add_cascade(label="Изменение БД", menu=changeBD_menu)
main_menu.add_cascade(label="Отчёты", menu=otchet_menu)

root.config(menu=main_menu, bg="#000", bd=0)
root.bind("<Configure>", resize)
root.mainloop()
