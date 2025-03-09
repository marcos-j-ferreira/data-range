import json 
import os
import time
import subprocess
import sys

par = "False"

if len(sys.argv) > 1:
    par = sys.argv[1].upper()

if par == "CLEAR" or par == "-C":
    os.system("cls")
