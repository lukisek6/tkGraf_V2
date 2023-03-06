from audioop import reverse
from sys import stdout, stderr
import copy
from tkinter import filedialog
import pylab as pl
from pylab import pi



class Bankomat:
    trezor = {}

    def __init__(self,znamky_ben) -> None:
        self.ben = 1
        self.ZNAMKY = znamky_ben

    def read(self,jmeno_body):
        soubor = open(jmeno_body, "r")
        trida = {}
        for line in soubor:
            jmeno, body = line.split()
            trida[jmeno] = body
        print(trida)
        soubor.close()
        return trida

    def read2(self,jmeno_bodovani):

        #trida = self.read()
        soubor = open(jmeno_bodovani, "r")
        znamky = {}
        for line in soubor:
            znamka, body = line.split()
            znamky[znamka] = body
        print(znamky)
        soubor.close()
        return znamky


    def make(self,body,bodovani):
        for klic, value in body.items():
            print(value)
            if int(value) >= int(bodovani["1"]):
                body[klic] = 1
            elif int(value) >= int(bodovani["2"]):
                body[klic] = 2
            elif int(value) >= int(bodovani["3"]):
                body[klic] = 3
            elif int(value) >= int(bodovani["4"]):
                body[klic] = 4
            elif int(value) >= int(bodovani["5"]):
                body[klic] = 5
        print(body)
        return body
    
    def write(self,zapis):
        if zapis == False:
            return False
        else:
            with open(self.ZNAMKY, mode='w') as soubor:
                soubor.write("")
            with open(self.ZNAMKY, mode='a') as soubor:
                for klic, value in zapis.items():
                    soubor.writelines(str(klic)+" "+str(zapis[klic]))
                    soubor.writelines("\n")
        soubor.close()

        return True or False
    
    def prumer(self,znamky):
        prumer_tridy = 0
        pocet_zaku = 0
        for klyc,value in znamky.items():
            prumer_tridy +=value
            pocet_zaku +=1
        print(prumer_tridy)
        prumer_tridy = prumer_tridy / pocet_zaku
        print(prumer_tridy)
        return prumer_tridy

if __name__ == "__main__":
    bankomat = Bankomat("znamky_ben.txt")

    while True:
        try:
            jmeno_body = filedialog.askopenfilename(title='Vyber list bodů')
            jmeno_bodovani = filedialog.askopenfilename(title='Vyber známkování')
            body = bankomat.read(jmeno_body)
            bodovani = bankomat.read2(jmeno_bodovani)
            #znamky = bankomat.make(body,bodovani)
            #print(znamky)
            print("BEN")
            znamky = bankomat.make(body,bodovani)
            bankomat.write(znamky)
            prumer_tridy = bankomat.prumer(znamky)
        except EOFError:
            exit(0)
        except KeyboardInterrupt:
            stderr.write("Program byl přerušen z klávecnice.")
            exit(1)
        except ValueError:
            stdout.write("ERROR\n")
        
        break