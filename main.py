from tkinter import *
from tkinter import messagebox, ttk, filedialog
from PIL import ImageTk, Image
import sqlite3
import shutil
import os
import random

# 1366 x 768

class MovieDatabaseApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Movie Wonders")
        # self.root.state("zoomed")
        self.root.geometry('1366x768')
        self.colorpalette = ['#424242', '#EEFCFC', '#B0A69C', '#877D73', '#6E655C']
        self.fonts = [('Century Gothic', 22, "bold"), ('Century Gothic', 22), ('Century Gothic', 17),
                      ('Century Gothic', 17, 'italic'), ('Century Gothic', 15)]
        self.root['bg'] = self.colorpalette[3]

        self.dbfile = "MovieDatabase.sqlite"

        self.menu = Frame(self.root, height=768, width=265, bg=self.colorpalette[2])
        self.menu.grid(row=0, column=0, rowspan=2)
        self.menu.grid_propagate(0)

        self.logoimage = PhotoImage(file='images/logo.png', master=self.root)
        self.logo = Label(self.menu, image=self.logoimage, borderwidth=0, bg=self.colorpalette[2])
        self.logo.grid(row=0, column=0, padx=87, pady=40, sticky=W)

        self.menubutframe = Frame(self.menu, height=768, width=430, bg=self.colorpalette[2])
        self.menubutframe.grid(row=1, column=0, pady=100)
        self.menubutframe.grid_propagate(0)

        # Button Images
        self.movieimg = PhotoImage(file="images/movie.png", master=self.root)
        self.prodimg = PhotoImage(file="images/production.png", master=self.root)
        self.actorimg = PhotoImage(file="images/actor.png", master=self.root)
        self.dirimg = PhotoImage(file="images/director.png", master=self.root)

        # Movie button
        Label(self.menubutframe, image=self.movieimg, borderwidth=0,
              bg=self.colorpalette[2]).grid(row=0, column=0, padx=20)
        Button(self.menubutframe, text="Movies", font=('Century Gothic', 20, "bold"), bg=self.colorpalette[2],
               fg=self.colorpalette[1], borderwidth=0, command=self.moviemain).grid(row=0, column=1, padx=2, sticky=W)

        # Movie button
        Label(self.menubutframe, image=self.prodimg, borderwidth=0,
              bg=self.colorpalette[2]).grid(row=1, column=0, padx=20)
        Button(self.menubutframe, text="Production", font=('Century Gothic', 20, "bold"), bg=self.colorpalette[2],
               fg=self.colorpalette[1], borderwidth=0, command=self.producers).grid(row=1, column=1, padx=2, sticky=W)

        # Movie button
        Label(self.menubutframe, image=self.actorimg, borderwidth=0,
              bg=self.colorpalette[2]).grid(row=2, column=0, padx=20)
        Button(self.menubutframe, text="Actors", font=('Century Gothic', 20, "bold"), bg=self.colorpalette[2],
               fg=self.colorpalette[1], borderwidth=0, command=self.actorsframe).grid(row=2, column=1, padx=2, sticky=W)

        # Movie button
        Label(self.menubutframe, image=self.dirimg, borderwidth=0,
              bg=self.colorpalette[2]).grid(row=3, column=0, padx=20)
        Button(self.menubutframe, text="Directors", font=('Century Gothic', 20, "bold"), bg=self.colorpalette[2],
               fg=self.colorpalette[1], borderwidth=0, command=self.directorsframe).grid(row=3, column=1, padx=2, sticky=W)

        self.mainFrame = Frame(self.root, height=768, width=1100, bg=self.colorpalette[3])
        self.mainFrame.grid(row=1, column=1, rowspan=2)
        self.mainFrame.grid_propagate(0)

        self.titlebar = Frame(self.root, height=60, width=1100, bg=self.colorpalette[0])
        self.titlebar.grid(row=0, column=1)
        self.titlebar.grid_columnconfigure(1, minsize=1100)
        self.titlebar.grid_propagate(0)

        self.title = Label(self.titlebar, text="", font=self.fonts[0], bg=self.colorpalette[0], fg=self.colorpalette[1])
        self.title.grid(row=0, column=0, padx=20, ipady=10)

        self.addimg = PhotoImage(file="images/add.png", master=self.root)
        self.editimg = PhotoImage(file="images/view.png", master=self.root)
        self.delimg = PhotoImage(file="images/delete.png", master=self.root)
        self.edimg = PhotoImage(file="images/edit.png", master=self.root)

        # For default values adding movies
        self.actor = {}
        self.directors = []
        self.genres = []
        self.production = []
        self.filename = ''

        self.database()
        self.moviemain()

    def database(self):
        conn = sqlite3.connect(self.dbfile)
        c = conn.cursor()
        with open("MovieDatabase.sql") as sql:
            sql_as_string = sql.read()
            c.executescript(sql_as_string)

        conn.commit()
        conn.close()

    def clear_frame(self):
        for widget in self.mainFrame.winfo_children():
            widget.destroy()

    def moviemain(self):
        def getdata():
            conn = sqlite3.connect(self.dbfile)
            c = conn.cursor()
            c.execute("""
            SELECT Movies.*, GROUP_CONCAT(G.Genre, ' | ') AS Gen FROM Movies
            INNER JOIN Genre G on Movies.Movie_id = G.Movie_ID
            GROUP BY G.Movie_ID;""")
            temp = c.fetchall()

            conn.close()
            count = 0
            for sup in temp:
                table.insert(parent='', index='end', iid=count, text='',
                             values=(sup[0], sup[1], sup[6], sup[4]))
                count += 1

        def search():
            if (optcbox.get()) == '':
                messagebox.showerror(title="Error", message="Please select a search option")
                return
            conn = sqlite3.connect(self.dbfile)
            c = conn.cursor()
            table.delete(*table.get_children())
            count = 0

            if optvar.get() == "Title":
                c.execute("SELECT * FROM Movies WHERE Title LIKE '%{title}%'".format(title=searchentry.get()))
                temp = c.fetchall()
                c.execute("""
                                SELECT Genre.Movie_ID, GROUP_CONCAT(Genre, ' | ') FROM Genre
                                GROUP BY Genre.Movie_ID;""")
                genre = c.fetchall()
                for sup in temp:
                    for g in genre:
                        if sup[0] == g[0]:
                            table.insert(parent='', index='end', iid=count, text='',
                                         values=(sup[0], sup[1], g[1], sup[4]))
                            count += 1
            elif optvar.get() == "Genre":
                c.execute("""
                SELECT Movies.* FROM Movies
                INNER JOIN Genre G on Movies.Movie_id = G.Movie_ID
                WHERE Genre LIKE '%{}%' GROUP BY G.Movie_ID;""".format(searchentry.get()))
                temp = c.fetchall()
                c.execute("""
                SELECT Genre.Movie_ID, GROUP_CONCAT(Genre, ' | ') FROM Genre
                GROUP BY Genre.Movie_ID;""")
                genre = c.fetchall()
                for sup in temp:
                    for g in genre:
                        if sup[0] == g[0]:
                            table.insert(parent='', index='end', iid=count, text='',
                                         values=(sup[0], sup[1], g[1], sup[4]))
                            count += 1
            elif optvar.get() == 'Year Released':
                print(count)
                c.execute("SELECT * FROM Movies WHERE Year_Released LIKE '%{year}%'".format(year=searchentry.get()))
                temp = c.fetchall()
                c.execute("""
                            SELECT Genre.Movie_ID, GROUP_CONCAT(Genre, ' | ') FROM Genre
                            GROUP BY Genre.Movie_ID;""")
                genre = c.fetchall()
                for sup in temp:
                    for g in genre:
                        if sup[0] == g[0]:
                            table.insert(parent='', index='end', iid=count, text='',
                                         values=(sup[0], sup[1], g[1], sup[4]))
                            count += 1
            elif searchentry.get() == '':
                c.execute("SELECT * FROM Movies;")
                temp = c.fetchall()
                c.execute("""
                        SELECT Genre.Movie_ID, GROUP_CONCAT(Genre, ' | ') FROM Genre
                        GROUP BY Genre.Movie_ID;""")
                genre = c.fetchall()
                for sup in temp:
                    for g in genre:
                        if sup[0] == g[0]:
                            table.insert(parent='', index='end', iid=count, text='',
                                         values=(sup[0], sup[1], g[1], sup[4]))
                            count += 1

            conn.close()

        def view():
            if table.focus() == '':
                messagebox.showerror('Error', 'Please select a movie from the table.')
                return

            def dur(mins):
                hours = int(mins / 60)
                min = mins % 60
                return str(hours) + "H " + str(min) + "m"

            def synop(line):
                n = 13
                words = line.split()
                grouped_words = [' '.join(words[i: i + n]) for i in range(0, len(words), n)]
                return grouped_words

            def linename(lists):
                temp = []
                for i in lists:
                    temp.append(i[0])
                return " | ".join(temp)

            def castnames(lists):
                strlist = []
                for a in lists:
                    strlist.append(a[0] + " as " + a[1])
                return strlist

            def add(id):
                def openfile():
                    self.filename = filedialog.askopenfilename(
                        title="Open A File",
                        filetype=(("JPEG Image", "*.jpeg"), ("JPG Image", "*.jpg"), ("PNG Image", "*.png"),
                                  ("All Files", "*.*")))
                    if self.filename:
                        try:
                            self.filename = r"{}".format(self.filename)

                            image = Image.open(self.filename)
                            resize_image = image.resize((270, 360))
                            self.img = ImageTk.PhotoImage(resize_image, master=self.root)
                            Label(photoframe, image=self.img).grid(row=0, column=0, sticky=NSEW)

                        except ValueError:
                            messagebox.showerror('Value Error', "File Couldn't Be Opened...try again!")
                        except FileNotFoundError:
                            messagebox.showerror("File Not Found", "File Couldn't Be Found...try again!")

                def actors():
                    def save():
                        res = messagebox.askquestion("Please Confirm", "Are you sure to update actors?")
                        if res == "No":
                            return
                        entries = [e1, e2, e3, e4, e5, e6, e7, e8]
                        for i in range(len(vars)):
                            self.actor[vars[i].get()] = entries[i].get()
                        top.destroy()

                    def close():
                        top.destroy()

                    top = Toplevel(mainframe)
                    top['bg'] = self.colorpalette[0]
                    top.geometry("700x700")

                    conn = sqlite3.connect(self.dbfile)
                    c = conn.cursor()
                    c.execute("SELECT Screen_Name FROM Actors;")
                    temp = []
                    for i in c.fetchall():
                        temp.append(i[0])
                    Label(top, text='Actors', bg=self.colorpalette[0], font=self.fonts[0],
                          fg=self.colorpalette[1]).grid(row=0, column=0, padx=5, pady=2, columnspan=3)
                    c.execute("""
                    SELECT Screen_Name, Character_Name FROM Actors INNER JOIN Acts A on Actors.Actor_ID = A.Actor_ID
                    WHERE Movie_ID=:id""", {'id': id})
                    roles = c.fetchall()
                    try:
                        a1 = StringVar()
                        a1box = ttk.Combobox(top, width=20, font=self.fonts[2], textvariable=a1)
                        a1box["values"] = tuple(temp)
                        a1box.grid(row=1, column=0, padx=10, pady=10)

                        a2 = StringVar()
                        a2box = ttk.Combobox(top, width=20, font=self.fonts[2], textvariable=a2)
                        a2box["values"] = tuple(temp)
                        a2box.grid(row=2, column=0, padx=10, pady=10)

                        a3 = StringVar()
                        a3box = ttk.Combobox(top, width=20, font=self.fonts[2], textvariable=a3)
                        a3box["values"] = tuple(temp)
                        a3box.grid(row=3, column=0, padx=10, pady=10)

                        a4 = StringVar()
                        a4box = ttk.Combobox(top, width=20, font=self.fonts[2], textvariable=a4)
                        a4box["values"] = tuple(temp)
                        a4box.grid(row=4, column=0, padx=10, pady=10)

                        a5 = StringVar()
                        a5box = ttk.Combobox(top, width=20, font=self.fonts[2], textvariable=a5)
                        a5box["values"] = tuple(temp)
                        a5box.grid(row=5, column=0, padx=10, pady=10)

                        a6 = StringVar()
                        a6box = ttk.Combobox(top, width=20, font=self.fonts[2], textvariable=a6)
                        a6box["values"] = tuple(temp)
                        a6box.grid(row=6, column=0, padx=10, pady=10)

                        a7 = StringVar()
                        a7box = ttk.Combobox(top, width=20, font=self.fonts[2], textvariable=a7)
                        a7box["values"] = tuple(temp)
                        a7box.grid(row=7, column=0, padx=10, pady=10)

                        a8 = StringVar()
                        a8box = ttk.Combobox(top, width=20, font=self.fonts[2], textvariable=a8)
                        a8box["values"] = tuple(temp)
                        a8box.grid(row=8, column=0, padx=10, pady=10)
                        vars = [a1, a2, a3, a4, a5, a6, a7, a8]

                        a1box.set(roles[0][0])
                        a2box.set(roles[1][0])
                        a3box.set(roles[2][0])
                        a4box.set(roles[3][0])
                        a5box.set(roles[4][0])
                        a6box.set(roles[5][0])
                        a7box.set(roles[6][0])
                        a8box.set(roles[7][0])

                    except:
                        pass

                    for i in range(8):
                        Label(top, text='as', bg=self.colorpalette[0], font=("century Gothic", 18),
                              fg=self.colorpalette[1]).grid(row=i + 1, column=1, padx=2, pady=10)

                    e1 = Entry(top, font=self.fonts[2])
                    e1.grid(row=1, column=2, padx=2)
                    e2 = Entry(top, font=self.fonts[2])
                    e2.grid(row=2, column=2, padx=2)
                    e3 = Entry(top, font=self.fonts[2])
                    e3.grid(row=3, column=2, padx=2)
                    e4 = Entry(top, font=self.fonts[2])
                    e4.grid(row=4, column=2, padx=2)
                    e5 = Entry(top, font=self.fonts[2])
                    e5.grid(row=5, column=2, padx=2)
                    e6 = Entry(top, font=self.fonts[2])
                    e6.grid(row=6, column=2, padx=2)
                    e7 = Entry(top, font=self.fonts[2])
                    e7.grid(row=7, column=2, padx=2)
                    e8 = Entry(top, font=self.fonts[2])
                    e8.grid(row=8, column=2, padx=2)

                    try:
                        e1.insert(0, roles[0][1])
                        e2.insert(0, roles[1][1])
                        e3.insert(0, roles[2][1])
                        e4.insert(0, roles[3][1])
                        e5.insert(0, roles[4][1])
                        e6.insert(0, roles[5][1])
                        e7.insert(0, roles[6][1])
                        e8.insert(0, roles[7][1])
                    except:
                        pass

                    Button(top, text="Save", bg=self.colorpalette[0], fg=self.colorpalette[1],
                           command=save, font=self.fonts[1]).grid(row=9, column=0, columnspan=2)
                    Button(top, text="Close", bg=self.colorpalette[0], fg=self.colorpalette[1],
                           command=close, font=self.fonts[1]).grid(row=9, column=1, columnspan=4)

                    conn.close()

                def directors():
                    def save():
                        res = messagebox.askquestion("Please Confirm", "Are you sure to update directors?")
                        if res == "No":
                            return
                        self.directors = [a1.get(), a2.get(), a3.get(), a4.get(), a5.get(), a6.get(), a7.get(),
                                          a8.get()]
                        top.destroy()

                    def close():
                        top.destroy()

                    top = Toplevel(mainframe)
                    top['bg'] = self.colorpalette[0]
                    top.geometry("600x700")

                    conn = sqlite3.connect(self.dbfile)
                    c = conn.cursor()
                    c.execute("SELECT Firstname ||' '|| Lastname FROM Directors;")
                    temp = []
                    for i in c.fetchall():
                        temp.append(i[0])
                    Label(top, text='Directors', bg=self.colorpalette[0], font=self.fonts[0],
                          fg=self.colorpalette[1]).grid(row=0, column=0, padx=5, pady=2, columnspan=2)

                    c.execute("""SELECT Firstname ||' '|| Lastname FROM Directors INNER JOIN Directs D 
                    on Directors.Director_ID = D.Director_ID WHERE Movie_ID=:id""", {'id': id})
                    directs = c.fetchall()

                    a1 = StringVar()
                    a1box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a1)
                    a1box["values"] = tuple(temp)
                    a1box.grid(row=1, column=0, padx=20, pady=10)

                    a2 = StringVar()
                    a2box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a2)
                    a2box["values"] = tuple(temp)
                    a2box.grid(row=2, column=0, padx=20, pady=10)

                    a3 = StringVar()
                    a3box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a3)
                    a3box["values"] = tuple(temp)
                    a3box.grid(row=3, column=0, padx=20, pady=10)

                    a4 = StringVar()
                    a4box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a4)
                    a4box["values"] = tuple(temp)
                    a4box.grid(row=4, column=0, padx=20, pady=10)

                    a5 = StringVar()
                    a5box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a5)
                    a5box["values"] = tuple(temp)
                    a5box.grid(row=5, column=0, padx=10, pady=10)

                    a6 = StringVar()
                    a6box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a6)
                    a6box["values"] = tuple(temp)
                    a6box.grid(row=6, column=0, padx=20, pady=10)

                    a7 = StringVar()
                    a7box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a7)
                    a7box["values"] = tuple(temp)
                    a7box.grid(row=7, column=0, padx=20, pady=10)

                    a8 = StringVar()
                    a8box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a8)
                    a8box["values"] = tuple(temp)
                    a8box.grid(row=8, column=0, padx=20, pady=10)

                    try:
                        a1box.set(directs[0][0])
                        a2box.set(directs[1][0])
                        a3box.set(directs[2][0])
                        a4box.set(directs[3][0])
                        a5box.set(directs[4][0])
                        a6box.set(directs[5][0])
                        a7box.set(directs[6][0])
                        a8box.set(directs[7][0])
                    except:
                        pass

                    buttonFrame = Frame(top, bg=self.colorpalette[0])
                    buttonFrame.grid(row=9, column=0)

                    Button(buttonFrame, text="Save", bg=self.colorpalette[0], fg=self.colorpalette[1],
                           command=save, font=self.fonts[1]).grid(row=0, column=0)
                    Button(buttonFrame, text="Close", bg=self.colorpalette[0], fg=self.colorpalette[1],
                           command=close, font=self.fonts[1]).grid(row=0, column=1, padx=10)

                    conn.close()

                def produce():
                    def save():
                        res = messagebox.askquestion("Please Confirm", "Are you sure to update producers?")
                        if res == "No":
                            return
                        self.production = [a1.get(), a2.get(), a3.get(), a4.get(), a5.get(), a6.get(), a7.get(),
                                           a8.get()]
                        top.destroy()

                    def close():
                        top.destroy()

                    top = Toplevel(mainframe)
                    top['bg'] = self.colorpalette[0]
                    top.geometry("600x700")

                    conn = sqlite3.connect(self.dbfile)
                    c = conn.cursor()
                    c.execute("SELECT Production_Name FROM Production;")
                    temp = []
                    for i in c.fetchall():
                        temp.append(i[0])
                    Label(top, text='Producer', bg=self.colorpalette[0], font=self.fonts[0],
                          fg=self.colorpalette[1]).grid(row=0, column=0, padx=5, pady=2, columnspan=2)

                    c.execute("""
                    SELECT Production_Name FROM Production INNER JOIN Owns O on Production.Production_ID = O.Production_ID
                    WHERE Movie_ID=:id""", {'id': id})
                    owns = c.fetchall()

                    a1 = StringVar()
                    a1box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a1)
                    a1box["values"] = tuple(temp)
                    a1box.grid(row=1, column=0, padx=20, pady=10)

                    a2 = StringVar()
                    a2box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a2)
                    a2box["values"] = tuple(temp)
                    a2box.grid(row=2, column=0, padx=20, pady=10)

                    a3 = StringVar()
                    a3box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a3)
                    a3box["values"] = tuple(temp)
                    a3box.grid(row=3, column=0, padx=20, pady=10)

                    a4 = StringVar()
                    a4box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a4)
                    a4box["values"] = tuple(temp)
                    a4box.grid(row=4, column=0, padx=20, pady=10)

                    a5 = StringVar()
                    a5box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a5)
                    a5box["values"] = tuple(temp)
                    a5box.grid(row=5, column=0, padx=10, pady=10)

                    a6 = StringVar()
                    a6box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a6)
                    a6box["values"] = tuple(temp)
                    a6box.grid(row=6, column=0, padx=20, pady=10)

                    a7 = StringVar()
                    a7box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a7)
                    a7box["values"] = tuple(temp)
                    a7box.grid(row=7, column=0, padx=20, pady=10)

                    a8 = StringVar()
                    a8box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a8)
                    a8box["values"] = tuple(temp)
                    a8box.grid(row=8, column=0, padx=20, pady=10)

                    try:
                        a1box.set(owns[0][0])
                        a2box.set(owns[1][0])
                        a3box.set(owns[2][0])
                        a4box.set(owns[3][0])
                        a5box.set(owns[4][0])
                        a6box.set(owns[5][0])
                        a7box.set(owns[6][0])
                        a8box.set(owns[7][0])
                    except:
                        pass

                    buttonFrame = Frame(top, bg=self.colorpalette[0])
                    buttonFrame.grid(row=9, column=0)

                    Button(buttonFrame, text="Save", bg=self.colorpalette[0], fg=self.colorpalette[1],
                           command=save, font=self.fonts[1]).grid(row=0, column=0)
                    Button(buttonFrame, text="Close", bg=self.colorpalette[0], fg=self.colorpalette[1],
                           command=close, font=self.fonts[1]).grid(row=0, column=1, padx=10)

                    conn.close()

                def genres():
                    def save():
                        res = messagebox.askquestion("Please Confirm", "Are you sure to update genre?")
                        if res == "No":
                            return
                        self.genres = [a1.get(), a2.get(), a3.get(), a4.get(), a5.get(), a6.get(), a7.get(), a8.get()]
                        top.destroy()

                    def close():
                        top.destroy()

                    top = Toplevel(mainframe)
                    top['bg'] = self.colorpalette[0]
                    top.geometry("600x700")

                    conn = sqlite3.connect(self.dbfile)
                    c = conn.cursor()
                    c.execute("SELECT DISTINCT (Genre) FROM Genre;")
                    temp = []
                    for i in c.fetchall():
                        temp.append(i[0])
                    Label(top, text='Genre', bg=self.colorpalette[0], font=self.fonts[0],
                          fg=self.colorpalette[1]).grid(row=0, column=0, ipadx=10, pady=2, columnspan=2)

                    c.execute("SELECT Genre FROM Genre WHERE Movie_ID=" + str(id))
                    gens = c.fetchall()

                    a1 = StringVar()
                    a1box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a1)
                    a1box["values"] = tuple(temp)
                    a1box.grid(row=1, column=0, padx=20, pady=10)

                    a2 = StringVar()
                    a2box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a2)
                    a2box["values"] = tuple(temp)
                    a2box.grid(row=2, column=0, padx=20, pady=10)

                    a3 = StringVar()
                    a3box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a3)
                    a3box["values"] = tuple(temp)
                    a3box.grid(row=3, column=0, padx=20, pady=10)

                    a4 = StringVar()
                    a4box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a4)
                    a4box["values"] = tuple(temp)
                    a4box.grid(row=4, column=0, padx=20, pady=10)

                    a5 = StringVar()
                    a5box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a5)
                    a5box["values"] = tuple(temp)
                    a5box.grid(row=5, column=0, padx=10, pady=10)

                    a6 = StringVar()
                    a6box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a6)
                    a6box["values"] = tuple(temp)
                    a6box.grid(row=6, column=0, padx=20, pady=10)

                    a7 = StringVar()
                    a7box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a7)
                    a7box["values"] = tuple(temp)
                    a7box.grid(row=7, column=0, padx=20, pady=10)

                    a8 = StringVar()
                    a8box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a8)
                    a8box["values"] = tuple(temp)
                    a8box.grid(row=8, column=0, padx=20, pady=10)
                    try:
                        a1box.set(gens[0][0])
                        a2box.set(gens[1][0])
                        a3box.set(gens[2][0])
                        a4box.set(gens[3][0])
                        a5box.set(gens[4][0])
                        a6box.set(gens[5][0])
                        a7box.set(gens[6][0])
                        a8box.set(gens[7][0])
                    except:
                        pass

                    buttonFrame = Frame(top, bg=self.colorpalette[0])
                    buttonFrame.grid(row=9, column=0)

                    Button(buttonFrame, text="Save", bg=self.colorpalette[0], fg=self.colorpalette[1],
                           command=save, font=self.fonts[1]).grid(row=0, column=0)
                    Button(buttonFrame, text="Close", bg=self.colorpalette[0], fg=self.colorpalette[1],
                           command=close, font=self.fonts[1]).grid(row=0, column=1, padx=10)

                    conn.close()

                def save():
                    if title.get() == '' or duration.get() == '' or self.genres == []:
                        print(title.get(), synopsis.get("1.0", "end"), duration.get(), year.get(), self.genres)
                        messagebox.showerror('Error', 'Please complete all entries.')
                        return
                    sv = messagebox.askquestion("Please Confirm", "Are you sure to update movie?")
                    if sv == "No":
                        return
                    conn = sqlite3.connect(self.dbfile)
                    c = conn.cursor()

                    path = os.path.basename(self.filename)
                    c.execute("""UPDATE Movies SET Title=?, Synopsis=?, Movie_Duration=?, Year_Released=?, Photo=?
                    WHERE Movie_id=?""",
                              (title.get(), synopsis.get("1.0", "end"), duration.get(), year.get(), "movies/" + path,
                               id))

                    c.execute("PRAGMA foreign_keys=ON")
                    c.execute(
                        "DELETE FROM Actors WHERE Actor_ID IN (SELECT Actor_ID FROM Acts WHERE Movie_ID=:id);",
                        {'id': id})
                    c.execute("PRAGMA foreign_keys=ON")
                    c.execute("DELETE FROM Acts WHERE Movie_ID=" + str(id))
                    for i, j in self.actor.items():
                        if i != "":
                            act_id = random.randint(0, 99999)
                            c.execute("PRAGMA foreign_keys = ON;")
                            c.execute("INSERT INTO Actors(Actor_ID, Screen_Name) VALUES (:id,:name)",
                                      {'name': i, 'id': act_id})
                            c.execute("PRAGMA foreign_keys = ON;")
                            c.execute("INSERT INTO Acts VALUES (:a, :m, :cn)", {'a': act_id, 'm': id, 'cn': j})

                    c.execute("PRAGMA foreign_keys=ON")
                    c.execute(
                        "DELETE FROM Directors WHERE Director_ID IN (SELECT Director_ID FROM Directs WHERE Movie_ID=:id)",
                        {'id': id})
                    c.execute("PRAGMA foreign_keys=ON")
                    c.execute("DELETE FROM Directs WHERE Movie_ID=" + str(id))
                    for i in self.directors:
                        if i != "":
                            dir_id = random.randint(0, 99999)
                            dname = i.split()
                            c.execute("PRAGMA foreign_keys = ON;")
                            c.execute("INSERT INTO Directors VALUES (?, ?, ?)", (dir_id, dname[0], " ".join(dname[1:])))
                            c.execute("PRAGMA foreign_keys = ON;")
                            c.execute("INSERT INTO Directs VALUES (?,?)", (id, dir_id))

                    c.execute("PRAGMA foreign_keys=ON")
                    c.execute("DELETE FROM Genre WHERE Movie_ID=" + str(id))
                    for i in self.genres:
                        if i != "":
                            c.execute("PRAGMA foreign_keys = ON;")
                            c.execute("INSERT INTO Genre VALUES (?, ?)", (id, i))

                    c.execute("PRAGMA foreign_keys=ON")
                    c.execute(
                        "DELETE FROM Production WHERE Production_ID IN (SELECT Production_ID FROM Owns WHERE Movie_ID=:id)",
                        {'id': id})
                    c.execute("PRAGMA foreign_keys=ON")
                    c.execute("DELETE FROM Owns WHERE Movie_ID=" + str(id))
                    for i in self.production:
                        if i != "":
                            prod_id = random.randint(0, 99999)
                            c.execute("PRAGMA foreign_keys = ON;")
                            c.execute("INSERT INTO Production VALUES (?,?)", (prod_id, i))
                            c.execute("PRAGMA foreign_keys = ON;")
                            c.execute("INSERT INTO Owns VALUES (?, ?)", (id, prod_id))

                    try:
                        shutil.copyfile(self.filename, r"movies/" + path)
                    except:
                        pass

                    conn.commit()
                    conn.close()

                conn = sqlite3.connect(self.dbfile)
                c = conn.cursor()
                c.execute("SELECT * FROM Movies WHERE Movie_id=" + str(id))
                moviedetail = c.fetchall()
                self.clear_frame()
                mainframe = Frame(self.mainFrame, height=768, width=1100, bg=self.colorpalette[0])
                mainframe.grid(row=1, column=0, padx=8, pady=8)
                mainframe.grid_propagate(0)

                OF = Frame(mainframe, height=50, width=500, bg=self.colorpalette[0])
                OF.grid(row=0, column=0, sticky=W)
                OF.grid_propagate(0)

                self.backimg = PhotoImage(file="images/back.png", master=self.root)
                Button(OF, image=self.backimg, borderwidth=0, bg=self.colorpalette[0],
                       activebackground=self.colorpalette[0], command=self.moviemain).grid(row=0, column=0)

                # Labels
                LF = Frame(mainframe, height=490, width=1100, bg=self.colorpalette[0])
                LF.grid(row=1, column=0, sticky=W, pady=4)
                LF.grid_propagate(0)

                Label(LF, text='Title:', bg=self.colorpalette[0], font=("Century Gothic", 18),
                      fg=self.colorpalette[1]).grid(row=0, column=0, padx=5, pady=2, sticky=E)
                Label(LF, text='Year Released:', bg=self.colorpalette[0], font=("Century Gothic", 18),
                      fg=self.colorpalette[1]).grid(row=1, column=0, padx=5, pady=2, sticky=E)
                Label(LF, text='Movie Duration:', bg=self.colorpalette[0], font=("Century Gothic", 18),
                      fg=self.colorpalette[1]).grid(row=2, column=0, padx=5, pady=2, sticky=E)
                Label(LF, text='Photo:', bg=self.colorpalette[0], font=("Century Gothic", 18),
                      fg=self.colorpalette[1]).grid(row=3, column=0, padx=5, pady=2, sticky=E)

                title = Entry(LF, font=self.fonts[2], borderwidth=0, width=38, bg=self.colorpalette[2],
                              fg=self.colorpalette[1])
                title.grid(row=0, column=1, pady=2)
                year = Entry(LF, font=self.fonts[2], borderwidth=0, width=38, bg=self.colorpalette[2],
                             fg=self.colorpalette[1])
                year.grid(row=1, column=1, pady=2)
                duration = Entry(LF, font=self.fonts[2], borderwidth=0, width=38, bg=self.colorpalette[2],
                                 fg=self.colorpalette[1])
                duration.grid(row=2, column=1, pady=2)

                Button(LF, text="Add Photo", font=self.fonts[2], bg=self.colorpalette[0],
                       fg=self.colorpalette[1], command=openfile).grid(row=3, column=1)

                photoframe = Frame(LF, height=360, width=270, bg=self.colorpalette[0])
                photoframe.grid(row=0, column=2, sticky=N, rowspan=20, padx=50)
                photoframe.grid_propagate(0)

                self.filename = moviedetail[0][5]
                image = Image.open(self.filename)
                resize_image = image.resize((270, 360))
                self.img = ImageTk.PhotoImage(resize_image, master=self.root)
                Label(photoframe, image=self.img).grid(row=0, column=0, sticky=NSEW)

                Label(LF, text='Synopsis:', bg=self.colorpalette[0], font=self.fonts[1],
                      fg=self.colorpalette[1]).grid(row=4, column=0, padx=5, pady=2, sticky=E)
                synopsis = Text(LF, height=13, width=55, bg=self.colorpalette[2], fg=self.colorpalette[1],
                                borderwidth=0,
                                font=("Century Gothic", 12))
                synopsis.grid(row=4, column=1, rowspan=10, pady=20)

                title.insert(0, moviedetail[0][1])
                year.insert(0, moviedetail[0][4])
                duration.insert(0, moviedetail[0][3])
                synopsis.insert(END, moviedetail[0][2])

                actorFrame = Frame(mainframe, width=1000, height=200, bg=self.colorpalette[0])
                actorFrame.grid(row=2, column=0, columnspan=4, sticky=W, padx=95)
                actorFrame.grid_propagate(0)

                Button(actorFrame, text='Add Actors', bg=self.colorpalette[0], font=self.fonts[0],
                       fg=self.colorpalette[1], command=actors).grid(row=0, column=0, padx=5, pady=5, sticky=W)
                Button(actorFrame, text='Add Directors', bg=self.colorpalette[0], font=self.fonts[0],
                       fg=self.colorpalette[1], command=directors).grid(row=0, column=1, padx=5, pady=5, sticky=W)
                Button(actorFrame, text='Add Production', bg=self.colorpalette[0], font=self.fonts[0],
                       fg=self.colorpalette[1], command=produce).grid(row=0, column=2, ipadx=5, pady=5, sticky=W)
                Button(actorFrame, text='Add Genre', bg=self.colorpalette[0], font=self.fonts[0],
                       fg=self.colorpalette[1], command=genres).grid(row=0, column=3, ipadx=5, pady=5, sticky=W)

                Button(actorFrame, text='Update Movie', bg=self.colorpalette[1], font=self.fonts[0],
                       fg=self.colorpalette[0], command=save).grid(row=1, column=0, columnspan=4, pady=5)

            id = table.item(table.focus(), "values")[0]
            conn = sqlite3.connect(self.dbfile)
            c = conn.cursor()
            c.execute("SELECT * FROM Movies WHERE Movie_id={}".format(id))
            movie = c.fetchone()

            self.clear_frame()
            mainframe = Frame(self.mainFrame, height=768, width=1100, bg=self.colorpalette[0])
            mainframe.grid(row=1, column=0, padx=8, pady=8)
            mainframe.grid_propagate(0)

            OF = Frame(mainframe, bg=self.colorpalette[0])
            OF.grid(row=0, column=0, sticky=W, padx=10, pady=10, columnspan=3)
            OF.grid_columnconfigure(1, minsize=960)
            self.backimg = PhotoImage(file="images/back.png", master=self.root)

            Button(OF, image=self.backimg, borderwidth=0, bg=self.colorpalette[0],
                   activebackground=self.colorpalette[0], command=self.moviemain).grid(row=0, column=0)
            Button(OF, image=self.edimg, borderwidth=0, bg=self.colorpalette[0],
                   activebackground=self.colorpalette[0], command=lambda: add(id)).grid(row=0, column=2)

            photoframe = Frame(mainframe, height=360, width=270, bg=self.colorpalette[1])
            photoframe.grid(row=1, column=0, padx=170, pady=8, sticky=W)
            photoframe.grid_propagate(0)

            detailsframe = Frame(mainframe, bg=self.colorpalette[0], height=320, width=400)
            detailsframe.grid(row=1, column=1, pady=10, columnspan=2, sticky=E)
            detailsframe.grid_propagate(0)

            image = Image.open(movie[5])
            resize_image = image.resize((270, 360))
            self.img = ImageTk.PhotoImage(resize_image, master=self.root)
            Label(photoframe, image=self.img).grid(row=0, column=0)

            c.execute("""
            SELECT Firstname ||' '|| Lastname FROM Directors
            INNER JOIN Directs D on Directors.Director_ID = D.Director_ID
            WHERE D.Movie_ID=:id;
            """, {'id': id})
            dirs = c.fetchall()

            c.execute("SELECT Genre FROM Genre WHERE Movie_ID={}".format(id))
            genres = []
            temp = c.fetchall()
            for i in temp:
                genres.append(i[0])

            Label(detailsframe, text=movie[1], bg=self.colorpalette[0], font=self.fonts[0], fg=self.colorpalette[1]) \
                .grid(row=0, column=0, padx=10, pady=10, sticky=W)
            Label(detailsframe, text=" | ".join(genres), bg=self.colorpalette[0], font=self.fonts[4],
                  fg=self.colorpalette[1]) \
                .grid(row=1, column=0, padx=20, pady=10, sticky=W)
            Label(detailsframe, text=movie[4], bg=self.colorpalette[0], font=self.fonts[3], fg=self.colorpalette[1]) \
                .grid(row=2, column=0, pady=10, padx=20, sticky=W)
            Label(detailsframe, text=dur(movie[3]), bg=self.colorpalette[0], font=self.fonts[3],
                  fg=self.colorpalette[1]) \
                .grid(row=3, column=0, pady=10, padx=20, sticky=W)
            Label(detailsframe, text='Directed by: ' + linename(dirs), bg=self.colorpalette[0], font=self.fonts[4],
                  fg=self.colorpalette[1]).grid(row=4, column=0, pady=20, padx=20, sticky=W)

            capFrame = Frame(mainframe, height=195, width=1100, bg=self.colorpalette[0])
            capFrame.grid(row=2, column=0, columnspan=2, sticky=W)
            capFrame.grid_propagate(0)

            synFrame = Frame(capFrame, height=350, width=700, bg=self.colorpalette[0])
            synFrame.grid(row=0, column=0, columnspan=2, sticky=W, padx=10)
            synFrame.grid_propagate(0)

            Label(synFrame, text='Synopsis:', bg=self.colorpalette[0], font=("Century Gothic", 18, 'bold'),
                  fg=self.colorpalette[1]).grid(row=0, column=0, padx=5, sticky=W)
            synopsis = synop(movie[2])
            for i in range(1, len(synopsis) + 1):
                Label(synFrame, text=synopsis[i - 1], bg=self.colorpalette[0], font=("Century Gothic", 11),
                      fg=self.colorpalette[1]).grid(row=i, column=0, sticky=W, padx=10)

            castFrame = Frame(capFrame, height=350, width=400, bg=self.colorpalette[0])
            castFrame.grid(row=0, column=2)
            castFrame.grid_propagate(0)

            c.execute("""
            SELECT Screen_Name, A.Character_Name FROM Actors
            INNER JOIN Acts A on Actors.Actor_ID = A.Actor_ID
            WHERE Movie_ID=:id;""", {'id': id})
            x = c.fetchall()
            Label(castFrame, text='Casts', bg=self.colorpalette[0], font=("Century Gothic", 18, 'bold'),
                  fg=self.colorpalette[1]).grid(row=0, column=0, padx=5, sticky=W)
            for i in range(1, len(castnames(x))+1):
                Label(castFrame, text=castnames(x)[i - 1], bg=self.colorpalette[0], font=("Century Gothic", 14),
                      fg=self.colorpalette[1]).grid(row=i, column=0, sticky=W, padx=4)

            c.execute("""
            SELECT Production_Name FROM Production
            INNER JOIN Owns O on Production.Production_ID = O.Production_ID
            WHERE Movie_ID=:id;""", {'id': id})

            Label(mainframe, text='Produced by: ' + linename(c.fetchall()), bg=self.colorpalette[0], font=self.fonts[4],
                  fg=self.colorpalette[1]).grid(row=4, column=0, sticky=W, columnspan=2, padx=20)

            conn.close()

        def add():
            def openfile():
                self.filename = filedialog.askopenfilename(
                    title="Open A File",
                    filetype=(("JPEG Image", "*.jpeg"), ("JPG Image", "*.jpg"), ("PNG Image", "*.png"),
                              ("All Files", "*.*")))
                if self.filename:
                    try:
                        self.filename = r"{}".format(self.filename)

                        image = Image.open(self.filename)
                        resize_image = image.resize((270, 360))
                        self.img = ImageTk.PhotoImage(resize_image, master=self.root)
                        Label(photoframe, image=self.img).grid(row=0, column=0, sticky=NSEW)

                    except ValueError:
                        messagebox.showerror('Value Error', "File Couldn't Be Opened...try again!")
                    except FileNotFoundError:
                        messagebox.showerror("File Not Found", "File Couldn't Be Found...try again!")

            def actors():
                def save():
                    res = messagebox.askquestion("Please Confirm", "Are you sure to add actors?")
                    if res == "No":
                        return
                    entries = [e1, e2, e3, e4, e5, e6, e7, e8]
                    for i in range(len(vars)):
                        self.actor[vars[i].get()] = entries[i].get()
                    top.destroy()

                def close():
                    top.destroy()

                top = Toplevel(mainframe)
                top['bg'] = self.colorpalette[0]
                top.geometry("700x700")

                conn = sqlite3.connect(self.dbfile)
                c = conn.cursor()
                c.execute("SELECT Screen_Name FROM Actors;")
                temp = []
                for i in c.fetchall():
                    temp.append(i[0])
                Label(top, text='Actors', bg=self.colorpalette[0], font=self.fonts[0],
                      fg=self.colorpalette[1]).grid(row=0, column=0, padx=5, pady=2, columnspan=3)

                a1 = StringVar()
                a1box = ttk.Combobox(top, width=20, font=self.fonts[2], textvariable=a1)
                a1box["values"] = tuple(temp)
                a1box.grid(row=1, column=0, padx=10, pady=10)

                a2 = StringVar()
                a2box = ttk.Combobox(top, width=20, font=self.fonts[2], textvariable=a2)
                a2box["values"] = tuple(temp)
                a2box.grid(row=2, column=0, padx=10, pady=10)

                a3 = StringVar()
                a3box = ttk.Combobox(top, width=20, font=self.fonts[2], textvariable=a3)
                a3box["values"] = tuple(temp)
                a3box.grid(row=3, column=0, padx=10, pady=10)

                a4 = StringVar()
                a4box = ttk.Combobox(top, width=20, font=self.fonts[2], textvariable=a4)
                a4box["values"] = tuple(temp)
                a4box.grid(row=4, column=0, padx=10, pady=10)

                a5 = StringVar()
                a5box = ttk.Combobox(top, width=20, font=self.fonts[2], textvariable=a5)
                a5box["values"] = tuple(temp)
                a5box.grid(row=5, column=0, padx=10, pady=10)

                a6 = StringVar()
                a6box = ttk.Combobox(top, width=20, font=self.fonts[2], textvariable=a6)
                a6box["values"] = tuple(temp)
                a6box.grid(row=6, column=0, padx=10, pady=10)

                a7 = StringVar()
                a7box = ttk.Combobox(top, width=20, font=self.fonts[2], textvariable=a7)
                a7box["values"] = tuple(temp)
                a7box.grid(row=7, column=0, padx=10, pady=10)

                a8 = StringVar()
                a8box = ttk.Combobox(top, width=20, font=self.fonts[2], textvariable=a8)
                a8box["values"] = tuple(temp)
                a8box.grid(row=8, column=0, padx=10, pady=10)

                vars = [a1, a2, a3, a4, a5, a6, a7, a8]
                for i in range(len(vars)):
                    Label(top, text='as', bg=self.colorpalette[0], font=("century Gothic", 18),
                          fg=self.colorpalette[1]).grid(row=i + 1, column=1, padx=2, pady=10)

                e1 = Entry(top, font=self.fonts[2])
                e1.grid(row=1, column=2, padx=2)
                e2 = Entry(top, font=self.fonts[2])
                e2.grid(row=2, column=2, padx=2)
                e3 = Entry(top, font=self.fonts[2])
                e3.grid(row=3, column=2, padx=2)
                e4 = Entry(top, font=self.fonts[2])
                e4.grid(row=4, column=2, padx=2)
                e5 = Entry(top, font=self.fonts[2])
                e5.grid(row=5, column=2, padx=2)
                e6 = Entry(top, font=self.fonts[2])
                e6.grid(row=6, column=2, padx=2)
                e7 = Entry(top, font=self.fonts[2])
                e7.grid(row=7, column=2, padx=2)
                e8 = Entry(top, font=self.fonts[2])
                e8.grid(row=8, column=2, padx=2)

                Button(top, text="Save", bg=self.colorpalette[0], fg=self.colorpalette[1],
                       command=save, font=self.fonts[1]).grid(row=9, column=0, columnspan=2)
                Button(top, text="Close", bg=self.colorpalette[0], fg=self.colorpalette[1],
                       command=close, font=self.fonts[1]).grid(row=9, column=1, columnspan=4)

                conn.close()

            def directors():
                def save():
                    res = messagebox.askquestion("Please Confirm", "Are you sure to add directors?")
                    if res == "No":
                        return
                    self.directors = [a1.get(), a2.get(), a3.get(), a4.get(), a5.get(), a6.get(), a7.get(), a8.get()]
                    top.destroy()

                def close():
                    top.destroy()

                top = Toplevel(mainframe)
                top['bg'] = self.colorpalette[0]
                top.geometry("600x700")

                conn = sqlite3.connect(self.dbfile)
                c = conn.cursor()
                c.execute("SELECT Firstname ||' '|| Lastname FROM Directors;")
                temp = []
                for i in c.fetchall():
                    temp.append(i[0])
                Label(top, text='Directors', bg=self.colorpalette[0], font=self.fonts[0],
                      fg=self.colorpalette[1]).grid(row=0, column=0, padx=5, pady=2, columnspan=2)

                a1 = StringVar()
                a1box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a1)
                a1box["values"] = tuple(temp)
                a1box.grid(row=1, column=0, padx=20, pady=10)

                a2 = StringVar()
                a2box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a2)
                a2box["values"] = tuple(temp)
                a2box.grid(row=2, column=0, padx=20, pady=10)

                a3 = StringVar()
                a3box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a3)
                a3box["values"] = tuple(temp)
                a3box.grid(row=3, column=0, padx=20, pady=10)

                a4 = StringVar()
                a4box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a4)
                a4box["values"] = tuple(temp)
                a4box.grid(row=4, column=0, padx=20, pady=10)

                a5 = StringVar()
                a5box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a5)
                a5box["values"] = tuple(temp)
                a5box.grid(row=5, column=0, padx=10, pady=10)

                a6 = StringVar()
                a6box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a6)
                a6box["values"] = tuple(temp)
                a6box.grid(row=6, column=0, padx=20, pady=10)

                a7 = StringVar()
                a7box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a7)
                a7box["values"] = tuple(temp)
                a7box.grid(row=7, column=0, padx=20, pady=10)

                a8 = StringVar()
                a8box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a8)
                a8box["values"] = tuple(temp)
                a8box.grid(row=8, column=0, padx=20, pady=10)

                buttonFrame = Frame(top, bg=self.colorpalette[0])
                buttonFrame.grid(row=9, column=0)

                Button(buttonFrame, text="Save", bg=self.colorpalette[0], fg=self.colorpalette[1],
                       command=save, font=self.fonts[1]).grid(row=0, column=0)
                Button(buttonFrame, text="Close", bg=self.colorpalette[0], fg=self.colorpalette[1],
                       command=close, font=self.fonts[1]).grid(row=0, column=1, padx=10)

                conn.close()

            def produce():
                def save():
                    res = messagebox.askquestion("Please Confirm", "Are you sure to add producers?")
                    if res == "No":
                        return
                    self.production = [a1.get(), a2.get(), a3.get(), a4.get(), a5.get(), a6.get(), a7.get(), a8.get()]
                    top.destroy()

                def close():
                    top.destroy()

                top = Toplevel(mainframe)
                top['bg'] = self.colorpalette[0]
                top.geometry("600x700")

                conn = sqlite3.connect(self.dbfile)
                c = conn.cursor()
                c.execute("SELECT Production_Name FROM Production;")
                temp = []
                for i in c.fetchall():
                    temp.append(i[0])
                Label(top, text='Producer', bg=self.colorpalette[0], font=self.fonts[0],
                      fg=self.colorpalette[1]).grid(row=0, column=0, padx=5, pady=2, columnspan=2)

                a1 = StringVar()
                a1box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a1)
                a1box["values"] = tuple(temp)
                a1box.grid(row=1, column=0, padx=20, pady=10)

                a2 = StringVar()
                a2box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a2)
                a2box["values"] = tuple(temp)
                a2box.grid(row=2, column=0, padx=20, pady=10)

                a3 = StringVar()
                a3box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a3)
                a3box["values"] = tuple(temp)
                a3box.grid(row=3, column=0, padx=20, pady=10)

                a4 = StringVar()
                a4box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a4)
                a4box["values"] = tuple(temp)
                a4box.grid(row=4, column=0, padx=20, pady=10)

                a5 = StringVar()
                a5box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a5)
                a5box["values"] = tuple(temp)
                a5box.grid(row=5, column=0, padx=10, pady=10)

                a6 = StringVar()
                a6box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a6)
                a6box["values"] = tuple(temp)
                a6box.grid(row=6, column=0, padx=20, pady=10)

                a7 = StringVar()
                a7box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a7)
                a7box["values"] = tuple(temp)
                a7box.grid(row=7, column=0, padx=20, pady=10)

                a8 = StringVar()
                a8box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a8)
                a8box["values"] = tuple(temp)
                a8box.grid(row=8, column=0, padx=20, pady=10)

                buttonFrame = Frame(top, bg=self.colorpalette[0])
                buttonFrame.grid(row=9, column=0)

                Button(buttonFrame, text="Save", bg=self.colorpalette[0], fg=self.colorpalette[1],
                       command=save, font=self.fonts[1]).grid(row=0, column=0)
                Button(buttonFrame, text="Close", bg=self.colorpalette[0], fg=self.colorpalette[1],
                       command=close, font=self.fonts[1]).grid(row=0, column=1, padx=10)

                conn.close()

            def genres():
                def save():
                    res = messagebox.askquestion("Please Confirm", "Are you sure to add genres?")
                    if res == "No":
                        return
                    self.genres = [a1.get(), a2.get(), a3.get(), a4.get(), a5.get(), a6.get(), a7.get(), a8.get()]
                    top.destroy()

                def close():
                    top.destroy()

                top = Toplevel(mainframe)
                top['bg'] = self.colorpalette[0]
                top.geometry("600x700")

                conn = sqlite3.connect(self.dbfile)
                c = conn.cursor()
                c.execute("SELECT DISTINCT (Genre) FROM Genre;")
                temp = []
                for i in c.fetchall():
                    temp.append(i[0])
                Label(top, text='Genre', bg=self.colorpalette[0], font=self.fonts[0],
                      fg=self.colorpalette[1]).grid(row=0, column=0, ipadx=10, pady=2, columnspan=2)

                a1 = StringVar()
                a1box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a1)
                a1box["values"] = tuple(temp)
                a1box.grid(row=1, column=0, padx=20, pady=10)

                a2 = StringVar()
                a2box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a2)
                a2box["values"] = tuple(temp)
                a2box.grid(row=2, column=0, padx=20, pady=10)

                a3 = StringVar()
                a3box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a3)
                a3box["values"] = tuple(temp)
                a3box.grid(row=3, column=0, padx=20, pady=10)

                a4 = StringVar()
                a4box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a4)
                a4box["values"] = tuple(temp)
                a4box.grid(row=4, column=0, padx=20, pady=10)

                a5 = StringVar()
                a5box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a5)
                a5box["values"] = tuple(temp)
                a5box.grid(row=5, column=0, padx=10, pady=10)

                a6 = StringVar()
                a6box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a6)
                a6box["values"] = tuple(temp)
                a6box.grid(row=6, column=0, padx=20, pady=10)

                a7 = StringVar()
                a7box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a7)
                a7box["values"] = tuple(temp)
                a7box.grid(row=7, column=0, padx=20, pady=10)

                a8 = StringVar()
                a8box = ttk.Combobox(top, width=30, font=self.fonts[2], textvariable=a8)
                a8box["values"] = tuple(temp)
                a8box.grid(row=8, column=0, padx=20, pady=10)

                buttonFrame = Frame(top, bg=self.colorpalette[0])
                buttonFrame.grid(row=9, column=0)

                Button(buttonFrame, text="Save", bg=self.colorpalette[0], fg=self.colorpalette[1],
                       command=save, font=self.fonts[1]).grid(row=0, column=0)
                Button(buttonFrame, text="Close", bg=self.colorpalette[0], fg=self.colorpalette[1],
                       command=close, font=self.fonts[1]).grid(row=0, column=1, padx=10)

                conn.close()

            def save():
                if title.get() == '' or duration.get() == '' or self.genres == []:
                    print(title.get(), synopsis.get("1.0", "end"), duration.get(), year.get(), self.genres)
                    messagebox.showerror('Error', 'Please complete all entries.')
                    return
                sv = messagebox.askquestion("Please Confirm", "Are you sure to add movie?")
                if sv == "No":
                    return
                conn = sqlite3.connect(self.dbfile)
                c = conn.cursor()

                mov_id = random.randint(0, 99999)
                path = os.path.basename(self.filename)
                c.execute("""INSERT INTO Movies
                VALUES (?, ?, ?, ?, ?, ?)""", (
                    mov_id, title.get(), synopsis.get("1.0", "end"), duration.get(), year.get(), "movies/" + path))
                print(mov_id)

                for i, j in self.actor.items():
                    if i != "":
                        act_id = random.randint(0, 99999)
                        c.execute("PRAGMA foreign_keys = ON;")
                        c.execute("INSERT INTO Actors(Actor_ID, Screen_Name) VALUES (:id,:name)",
                                  {'name': i, 'id': act_id})
                        c.execute("PRAGMA foreign_keys = ON;")
                        c.execute("INSERT INTO Acts VALUES (:a, :m, :cn)", {'a': act_id, 'm': mov_id, 'cn': j})

                for i in self.directors:
                    if i != "":
                        dir_id = random.randint(0, 99999)
                        dname = i.split()
                        c.execute("PRAGMA foreign_keys = ON;")
                        c.execute("INSERT INTO Directors VALUES (?, ?, ?)", (dir_id, dname[0], " ".join(dname[1:])))
                        c.execute("PRAGMA foreign_keys = ON;")
                        c.execute("INSERT INTO Directs VALUES (?,?)", (mov_id, dir_id))

                for i in self.genres:
                    if i != "":
                        c.execute("PRAGMA foreign_keys = ON;")
                        c.execute("INSERT INTO Genre VALUES (?, ?)", (mov_id, i))

                for i in self.production:
                    if i != "":
                        prod_id = random.randint(0, 99999)
                        c.execute("PRAGMA foreign_keys = ON;")
                        c.execute("INSERT INTO Production VALUES (?,?)", (prod_id, i))
                        c.execute("PRAGMA foreign_keys = ON;")
                        c.execute("INSERT INTO Owns VALUES (?, ?)", (mov_id, prod_id))

                try:
                    shutil.copyfile(self.filename, r"movies/" + path)
                except:
                    pass

                c.execute("SELECT * FROM Movies WHERE Movie_id=" + str(mov_id))
                print(c.fetchall())

                conn.commit()
                conn.close()

            self.clear_frame()
            mainframe = Frame(self.mainFrame, height=768, width=1100, bg=self.colorpalette[0])
            mainframe.grid(row=1, column=0, padx=8, pady=8)
            mainframe.grid_propagate(0)

            OF = Frame(mainframe, height=50, width=500, bg=self.colorpalette[0])
            OF.grid(row=0, column=0, sticky=W)
            OF.grid_propagate(0)

            self.backimg = PhotoImage(file="images/back.png", master=self.root)
            Button(OF, image=self.backimg, borderwidth=0, bg=self.colorpalette[0],
                   activebackground=self.colorpalette[0], command=self.moviemain).grid(row=0, column=0)

            # Label
            LF = Frame(mainframe, height=490, width=1100, bg=self.colorpalette[0])
            LF.grid(row=1, column=0, sticky=W, pady=4)
            LF.grid_propagate(0)

            Label(LF, text='Title:', bg=self.colorpalette[0], font=('Century Gothic', 18),
                  fg=self.colorpalette[1]).grid(row=0, column=0, padx=5, pady=2, sticky=E)
            Label(LF, text='Year Released:', bg=self.colorpalette[0], font=('Century Gothic',18),
                  fg=self.colorpalette[1]).grid(row=1, column=0, padx=5, pady=2, sticky=E)
            Label(LF, text='Movie Duration:', bg=self.colorpalette[0], font=('Century Gothic', 18),
                  fg=self.colorpalette[1]).grid(row=2, column=0, padx=5, pady=2, sticky=E)
            Label(LF, text='Photo:', bg=self.colorpalette[0], font=('Century Gothic', 18),
                  fg=self.colorpalette[1]).grid(row=3, column=0, padx=5, pady=2, sticky=E)

            title = Entry(LF, font=self.fonts[2], borderwidth=0, width=38, bg=self.colorpalette[2],
                          fg=self.colorpalette[1])
            title.grid(row=0, column=1)
            year = Entry(LF, font=self.fonts[2], borderwidth=0, width=38, bg=self.colorpalette[2],
                         fg=self.colorpalette[1])
            year.grid(row=1, column=1)
            duration = Entry(LF, font=self.fonts[2], borderwidth=0, width=38, bg=self.colorpalette[2],
                             fg=self.colorpalette[1])
            duration.grid(row=2, column=1)

            Button(LF, text="Add Photo", font=self.fonts[2], bg=self.colorpalette[0],
                   fg=self.colorpalette[1], command=openfile).grid(row=3, column=1)

            photoframe = Frame(LF, height=360, width=270, bg=self.colorpalette[0])
            photoframe.grid(row=0, column=2, sticky=N, rowspan=20, padx=50, ipady=20)
            photoframe.grid_propagate(0)

            Label(LF, text='Synopsis:', bg=self.colorpalette[0], font=self.fonts[1],
                  fg=self.colorpalette[1]).grid(row=4, column=0, padx=5, pady=2, sticky=E)
            synopsis = Text(LF, height=14, width=55, bg=self.colorpalette[2], fg=self.colorpalette[1], borderwidth=0,
                            font=("Century Gothic", 12))
            synopsis.grid(row=4, column=1, rowspan=10, pady=20)

            actorFrame = Frame(mainframe, width=1000, height=200, bg=self.colorpalette[0])
            actorFrame.grid(row=2, column=0, columnspan=2, sticky=N, padx=100)
            actorFrame.grid_propagate(0)

            Button(actorFrame, text='Add Actors', bg=self.colorpalette[0], font=self.fonts[0],
                   fg=self.colorpalette[1], command=actors).grid(row=0, column=0, padx=5, pady=5, sticky=W)
            Button(actorFrame, text='Add Directors', bg=self.colorpalette[0], font=self.fonts[0],
                   fg=self.colorpalette[1], command=directors).grid(row=0, column=1, padx=5, pady=5, sticky=W)
            Button(actorFrame, text='Add Production', bg=self.colorpalette[0], font=self.fonts[0],
                   fg=self.colorpalette[1], command=produce).grid(row=0, column=2, ipadx=5, pady=5, sticky=W)
            Button(actorFrame, text='Add Genre', bg=self.colorpalette[0], font=self.fonts[0],
                   fg=self.colorpalette[1], command=genres).grid(row=0, column=3, ipadx=5, pady=5, sticky=W)

            Button(actorFrame, text='Save Movie', bg=self.colorpalette[1], font=self.fonts[0],
                   fg=self.colorpalette[0], command=save).grid(row=1, column=0, columnspan=4, pady=5)

        def delete():
            if table.focus() == '':
                messagebox.showerror('Error', 'Please select a movie from the table.')
                return

            sv = messagebox.askquestion("Please Confirm", "Are you sure to delete movie?")
            if sv == "No":
                return

            id = table.item(table.focus(), "values")[0]
            conn = sqlite3.connect(self.dbfile)
            c = conn.cursor()

            # c.execute("PRAGMA foreign_keys=ON")
            c.execute("DELETE FROM Movies WHERE Movie_id=" + str(id))
            c.execute("PRAGMA foreign_keys=ON")
            c.execute("DELETE FROM Actors WHERE Actor_ID IN (SELECT Actor_ID FROM Acts WHERE Movie_ID=:id);",
                      {'id': id})
            c.execute("PRAGMA foreign_keys=ON")
            c.execute("DELETE FROM Acts WHERE Movie_ID=" + str(id))
            c.execute("PRAGMA foreign_keys=ON")
            c.execute("DELETE FROM Directors WHERE Director_ID IN (SELECT Director_ID FROM Directs WHERE Movie_ID=:id)",
                      {'id': id})
            c.execute("PRAGMA foreign_keys=ON")
            c.execute("DELETE FROM Directs WHERE Movie_ID=" + str(id))
            c.execute("PRAGMA foreign_keys=ON")
            c.execute("DELETE FROM Genre WHERE Movie_ID=" + str(id))
            c.execute("PRAGMA foreign_keys=ON")
            c.execute(
                "DELETE FROM Production WHERE Production_ID IN (SELECT Production_ID FROM Owns WHERE Movie_ID=:id)",
                {'id': id})
            c.execute("PRAGMA foreign_keys=ON")
            c.execute("DELETE FROM Owns WHERE Movie_ID=" + str(id))
            conn.commit()
            conn.close()

            table.delete(table.focus())
            messagebox.showinfo("Success", "The movie has been deleted")

        self.title.config(text="Movies")
        self.clear_frame()

        mainframe = Frame(self.mainFrame, height=768, width=1100, bg=self.colorpalette[0])
        mainframe.grid(row=1, column=0, padx=8, pady=8)
        mainframe.grid_propagate(0)

        # Search Frame
        SF = Frame(mainframe, height=50, width=1100, bg=self.colorpalette[0])
        SF.grid(row=0, column=0)
        SF.grid_propagate(0)
        SF.grid_columnconfigure(0, minsize=120)
        SF.grid_columnconfigure(5, minsize=140)

        delete = Button(SF, image=self.delimg, borderwidth=0, bg=self.colorpalette[0],
                        activebackground=self.colorpalette[0], command=delete)
        delete.grid(row=0, column=8, padx=5)

        add = Button(SF, image=self.addimg, borderwidth=0, bg=self.colorpalette[0],
                     activebackground=self.colorpalette[0], command=add)
        add.grid(row=0, column=7, padx=5)

        view = Button(SF, image=self.editimg, borderwidth=0, bg=self.colorpalette[0],
                      activebackground=self.colorpalette[0], command=view)
        view.grid(row=0, column=6, padx=5)

        # Entries and combobox
        self.root.option_add('*TCombobox*Listbox.font', self.fonts[2])
        Label(SF, text="Search By:", font=self.fonts[2], bg=self.colorpalette[0],
              fg=self.colorpalette[1]).grid(row=0, column=1, padx=2, pady=3)
        searchentry = Entry(SF, font=self.fonts[2])
        searchentry.grid(row=0, column=3, padx=2)
        optvar = StringVar()
        optcbox = ttk.Combobox(SF, width=12, font=self.fonts[2], textvariable=optvar)
        optcbox['values'] = ("Title", "Genre", "Year")
        optcbox.grid(row=0, column=2, padx=2)
        self.searchimg = PhotoImage(file="images/search.png", master=self.root)
        Button(SF, image=self.searchimg, borderwidth=0, bg=self.colorpalette[0],
               activebackground=self.colorpalette[2], comman=search).grid(row=0, column=4)

        # Table frame
        table_frame = Frame(mainframe, width=1100, height=658)
        table_frame.grid(row=1, column=0, sticky=NW, pady=10)

        # Treeview scrollbar
        table_scroll = Scrollbar(table_frame)
        table_scroll.grid(row=0, column=1, sticky=NS)

        # Add Treeview widget to display the students
        table = ttk.Treeview(table_frame, yscrollcommand=table_scroll.set, height=18)
        table.grid(row=0, column=0, sticky=NS, pady=12, padx=10)
        table_scroll.config(command=table.yview)

        # Table style
        style = ttk.Style()
        style.configure("Treeview", highlightthickness=0, bd=0, font=('Century Gothic', 20), rowheight=32,
                        fieldbackground=self.colorpalette[2])
        style.configure("Treeview.Heading", font=('Century Gothic', 20, "bold"))
        style.map('Treeview', background=[('selected', '#BFBFBF')])

        # Format table
        cols = ("ID", "Title", "Genre", "Year")
        table["columns"] = cols
        table.column('#0', width=0, stretch=NO)
        # Create headings
        table.heading("#0", text='', anchor=CENTER)
        for col in cols:
            if col == "ID":
                table.column(col, anchor=CENTER, width=100)
                table.heading(col, text=col, anchor=CENTER)
            elif col == "Title" or col == "Genre":
                table.column(col, anchor=W, width=400)
                table.heading(col, text=col, anchor=CENTER)
            else:
                table.column(col, anchor=W, width=155)
                table.heading(col, text=col, anchor=CENTER)

        getdata()

    def producers(self):
        self.title.config(text="Production")
        self.clear_frame()

        mainframe = Frame(self.mainFrame, height=768, width=1100, bg=self.colorpalette[0])
        mainframe.grid(row=1, column=0, padx=8, pady=8)
        mainframe.grid_propagate(0)

        # Search Frame
        SF = Frame(mainframe, height=50, width=1100, bg=self.colorpalette[0])
        SF.grid(row=0, column=0)
        SF.grid_propagate(0)
        SF.grid_columnconfigure(5, minsize=1020)

        delete = Button(SF, image=self.delimg, borderwidth=0, bg=self.colorpalette[0],
                        activebackground=self.colorpalette[0])
        delete.grid(row=0, column=8, padx=5)

        # add = Button(SF, image=self.addimg, borderwidth=0, bg=self.colorpalette[0],
        #              activebackground=self.colorpalette[0])
        # add.grid(row=0, column=7, padx=5)
        #
        # view = Button(SF, image=self.editimg, borderwidth=0, bg=self.colorpalette[0],
        #               activebackground=self.colorpalette[0])
        # view.grid(row=0, column=6, padx=5)

        # Table frame
        table_frame = Frame(mainframe, width=1100, height=658)
        table_frame.grid(row=1, column=0, sticky=NW, pady=10)

        # Treeview scrollbar
        table_scroll = Scrollbar(table_frame)
        table_scroll.grid(row=0, column=1, sticky=NS)

        # Add Treeview widget to display the students
        table = ttk.Treeview(table_frame, yscrollcommand=table_scroll.set, height=18)
        table.grid(row=0, column=0, sticky=NS, pady=10, padx=10)
        table_scroll.config(command=table.yview)

        # Table style
        style = ttk.Style()
        style.configure("Treeview", highlightthickness=0, bd=0, font=('Century Gothic', 20), rowheight=32,
                        fieldbackground=self.colorpalette[2])
        style.configure("Treeview.Heading", font=('Century Gothic', 22, "bold"))
        style.map('Treeview', background=[('selected', '#BFBFBF')])

        # Format table
        cols = ("Producers")
        table["columns"] = cols
        table.column('#0', width=0, stretch=NO)
        # Create headings
        table.heading("#0", text='', anchor=CENTER)
        table.column("Producers", anchor=CENTER, width=1052)
        table.heading("Producers", text="Producers", anchor=CENTER)

        conn = sqlite3.connect(self.dbfile)
        c = conn.cursor()
        c.execute("SELECT Production_Name FROM Production")

        count = 0
        for i in c.fetchall():
            table.insert(parent='', index='end', iid=count, text='',values=(i))
            count += 1


    def actorsframe(self):
        self.title.config(text="Actors")
        self.clear_frame()

        mainframe = Frame(self.mainFrame, height=768, width=1100, bg=self.colorpalette[0])
        mainframe.grid(row=1, column=0, padx=8, pady=8)
        mainframe.grid_propagate(0)

        # Search Frame
        SF = Frame(mainframe, height=50, width=1100, bg=self.colorpalette[0])
        SF.grid(row=0, column=0)
        SF.grid_propagate(0)
        SF.grid_columnconfigure(5, minsize=1020)

        delete = Button(SF, image=self.delimg, borderwidth=0, bg=self.colorpalette[0],
                        activebackground=self.colorpalette[0])
        delete.grid(row=0, column=8, padx=5)

        # add = Button(SF, image=self.addimg, borderwidth=0, bg=self.colorpalette[0],
        #              activebackground=self.colorpalette[0])
        # add.grid(row=0, column=7, padx=5)
        #
        # view = Button(SF, image=self.editimg, borderwidth=0, bg=self.colorpalette[0],
        #               activebackground=self.colorpalette[0])
        # view.grid(row=0, column=6, padx=5)

        # Table frame
        table_frame = Frame(mainframe, width=1100, height=658)
        table_frame.grid(row=1, column=0, sticky=NW, pady=10)

        # Treeview scrollbar
        table_scroll = Scrollbar(table_frame)
        table_scroll.grid(row=0, column=1, sticky=NS)

        # Add Treeview widget to display the students
        table = ttk.Treeview(table_frame, yscrollcommand=table_scroll.set, height=18)
        table.grid(row=0, column=0, sticky=NS, pady=10, padx=10)
        table_scroll.config(command=table.yview)

        # Table style
        style = ttk.Style()
        style.configure("Treeview", highlightthickness=0, bd=0, font=('Century Gothic', 20), rowheight=32,
                        fieldbackground=self.colorpalette[2])
        style.configure("Treeview.Heading", font=('Century Gothic', 22, "bold"))
        style.map('Treeview', background=[('selected', '#BFBFBF')])

        # Format table
        cols = ("Actors")
        table["columns"] = cols
        table.column('#0', width=0, stretch=NO)
        # Create headings
        table.heading("#0", text='', anchor=CENTER)
        table.column("Actors", anchor=CENTER, width=1054)
        table.heading("Actors", text="Actors", anchor=CENTER)

        conn = sqlite3.connect(self.dbfile)
        c = conn.cursor()
        c.execute("SELECT Screen_Name FROM Actors")

        count = 0
        for i in c.fetchall():
            table.insert(parent='', index='end', iid=count, text='',values=(i))
            count += 1

    def directorsframe(self):
        self.title.config(text="Directors")
        self.clear_frame()

        mainframe = Frame(self.mainFrame, height=768, width=1100, bg=self.colorpalette[0])
        mainframe.grid(row=1, column=0, padx=8, pady=8)
        mainframe.grid_propagate(0)

        # Search Frame
        SF = Frame(mainframe, height=50, width=1100, bg=self.colorpalette[0])
        SF.grid(row=0, column=0)
        SF.grid_propagate(0)
        SF.grid_columnconfigure(5, minsize=1020)

        delete = Button(SF, image=self.delimg, borderwidth=0, bg=self.colorpalette[0],
                        activebackground=self.colorpalette[0])
        delete.grid(row=0, column=8, padx=5)

        # add = Button(SF, image=self.addimg, borderwidth=0, bg=self.colorpalette[0],
        #              activebackground=self.colorpalette[0])
        # add.grid(row=0, column=7, padx=5)
        #
        # view = Button(SF, image=self.editimg, borderwidth=0, bg=self.colorpalette[0],
        #               activebackground=self.colorpalette[0])
        # view.grid(row=0, column=6, padx=5)

        # Table frame
        table_frame = Frame(mainframe, width=1100, height=658)
        table_frame.grid(row=1, column=0, sticky=NW, pady=10)

        # Treeview scrollbar
        table_scroll = Scrollbar(table_frame)
        table_scroll.grid(row=0, column=1, sticky=NS)

        # Add Treeview widget to display the students
        table = ttk.Treeview(table_frame, yscrollcommand=table_scroll.set, height=18)
        table.grid(row=0, column=0, sticky=NS, pady=10, padx=10)
        table_scroll.config(command=table.yview)

        # Table style
        style = ttk.Style()
        style.configure("Treeview", highlightthickness=0, bd=0, font=('Century Gothic', 20), rowheight=32,
                        fieldbackground=self.colorpalette[2])
        style.configure("Treeview.Heading", font=('Century Gothic', 22, "bold"))
        style.map('Treeview', background=[('selected', '#BFBFBF')])

        # Format table
        cols = ("Directors")
        table["columns"] = cols
        table.column('#0', width=0, stretch=NO)
        # Create headings
        table.heading("#0", text='', anchor=CENTER)
        table.column("Directors", anchor=CENTER, width=1052)
        table.heading("Directors", text="Directors", anchor=CENTER)

        conn = sqlite3.connect(self.dbfile)
        c = conn.cursor()
        c.execute("SELECT Firstname||' '||Lastname FROM Directors")

        count = 0
        for i in c.fetchall():
            table.insert(parent='', index='end', iid=count, text='',values=(i))
            count += 1

if __name__ == '__main__':
    root = Tk()
    application = MovieDatabaseApp(root)
    root.mainloop()
