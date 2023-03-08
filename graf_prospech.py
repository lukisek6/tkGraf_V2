from audioop import reverse
from sys import stdout, stderr
from pocitani_prospech import Bankomat
from os.path import basename, splitext
import tkinter as tk
import matplotlib.pyplot as plt

from tkinter import filedialog



class MyEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        if not "textvariable" in kw:
            self.variable = tk.StringVar()
            self.config(textvariable=self.variable)
        else:
            self.variable = kw["textvariable"]

    @property
    def value(self):
        return self.variable.get()

    @value.setter
    def value(self, new: str):
        self.variable.set(new)


class About(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent, class_=parent.name)
        self.config()

        btn = tk.Button(self, text="Konec", command=self.close)
        btn.pack()

    def close(self):
        self.destroy()


class Application(tk.Tk):
    name = basename(splitext(basename(__file__.capitalize()))[0])
    name = "Show graph"

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)
        self.bind("<Escape>", self.quit)
        self.jmeno_body = filedialog.askopenfilename(title='Vyber list bodů')
        self.jmeno_bodovani = filedialog.askopenfilename(title='Vyber známkování')
        self.body = bankomat.read(self.jmeno_body)
        self.bodovani = bankomat.read2(self.jmeno_bodovani)
        self.znamky = bankomat.make(self.body,self.bodovani)
        bankomat.write(self.znamky)
        self.prumer_tridy = bankomat.prumer(self.znamky)
        self.jednickari = 0
        self.dvojkari = 0
        self.trojkari = 0
        self.ctverkari = 0
        self.petkari = 0

        #self.entry = tk.Entry()
        #self.entry.pack()
        #self.btn1 = tk.Button(text="...", command=self.find)
        #self.btn1.pack()
        self.btn2 = tk.Button(text="Vykreslit", command=self.show)
        self.btn2.pack()
        self.btn3 = tk.Button(text="Quit", command=quit)
        self.btn3.pack()

    
    def find(self):
        file = filedialog.askopenfile()   
        self.entry.insert(0, file.name)

    def show(self):
        for keys,value in self.znamky.items():
            if value == 1:
                self.jednickari +=1
            elif value ==2:
                self.dvojkari +=1
            elif value ==3:
                self.trojkari +=1
            elif value ==4:
                self.ctverkari +=1
            elif value ==5:
                self.petkari +=1

        prumer = "Průměr třídy je "+str(self.prumer_tridy)

        fig, ax = plt.subplots()

        grades = ['1', '2', '3', '4','5']
        counts = [self.jednickari, self.dvojkari, self.trojkari, self.ctverkari,self.petkari]
        #bar_labels = ['1', '2', '3', '4','5']
        bar_colors = ['tab:green', 'tab:blue', 'tab:orange', 'tab:red','tab:red']
        
        ax.bar(grades, counts, color=bar_colors)
        
        ax.set_ylabel('Počet žáků')
        ax.set_xlabel("Známka")
        ax.set_title('Prospěch třídy')
        ax.legend(title=prumer)
        
        plt.show()

    def about(self):
        window = About(self)
        window.grab_set()

    def quit(self, event=None):
        super().quit()

if __name__ == "__main__":
    bankomat = Bankomat('znamky_ben.txt')

    app = Application()
    app.mainloop()