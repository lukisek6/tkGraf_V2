from audioop import reverse
from sys import stdout, stderr
from pocitani_prospech import Bankomat
from os.path import basename, splitext
import tkinter as tk


class Application(tk.Tk):
    #name = basename(splitext(basename(__file__.capitalize()))[0])
    name = "PRASE"

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)
        self.bind("<Escape>", self.quit)
        self.lbl = tk.Label(self, text="PRASE")
        self.lbl.pack()
        self.btn = tk.Button(self, text="Quit", command=self.quit)
        self.btn.pack()


        self.var_R = tk.IntVar()
        self.entry_R = tk.Entry(width=5, textvariable=self.var_R)
        self.entry_R.pack(fill="x")

        self.entry_R.bind("<Return>",self.click_handler)

        self.zprava = tk.Message(self, text="")
        self.zprava.pack()


    def napis(self,textus):
        self.zprava.config(text=textus)

    def click_handler(self,event):
        self.number_change()


    def number_change(self,var = None, index = None, mode =None):
        print(var,index, mode)
        global r  
        r = self.var_R.get()
        try:
            line = r
            number = int(line)
            slovnik = bankomat.read()
            novy_slovnik = bankomat.make(number,slovnik)
            if novy_slovnik == "Chyba, nejsou peníze":
                s= novy_slovnik
                self.napis(s)
                return False
            print(novy_slovnik)
        except EOFError:
            exit(0)
        except KeyboardInterrupt:
            stderr.write("Program byl přerušen z klávecnice.")
            exit(1)
        except ValueError:
            stdout.write("ERROR\n")
        textas = []
        for klic, value in slovnik.items():
            if int(slovnik[klic]) - int(novy_slovnik[klic]) > 0:
                textus = str(klic)+" x "+str(int(slovnik[klic]) - int(novy_slovnik[klic]))
                print(textus)                
                textas.append(textus)
        s= ""
        print(textas[0])
        for k in textas:
            s = s + str(k)+"\n"
        #textas =[]
        self.napis(s)
        bankomat.write(novy_slovnik)



    def quit(self, event=None):
        super().quit()

if __name__ == "__main__":
    bankomat = Bankomat('trezor.txt')

    app = Application()
    app.mainloop()