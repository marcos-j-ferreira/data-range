import re 
import sys
import os 

def read(opetion=None, number=3):

    files = {
        "down": ["down-0.txt","down-1.txt","down-2.txt"],
        "up": ["up-0.txt","up-1.txt","up-2.txt"],
        "netsh": ["netsh-0.txt","netsh-0.txt","netsh-0.txt"]
    }

    ope = opetion.upper()

    if ope is None:
        print("Escolha uma opção\n Down\n Up\n Netsh")

    if ope == "DOWN":

        for i in range(0,3):

            with open(files["down"][i], "r", encoding="utf-8") as f:
                result = f.read()
                print(result)
    
    if ope == "UP":

        for i in range(0,3):

            with open(files["up"][i], "r", encoding="utf-8") as f:
                result = f.read()
                print(result)
    
    if ope == "NETSH":

        for i in range(0,3):

            with open(files["netsh"][i], "r", encoding="utf-8") as f:
                result = f.read()
                print(result)



read("netsh")

