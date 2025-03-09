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

config = {
    "ip": None,
    "host": None,
    "time":None,
    "run": None
}

def path_json():

    way = "./config.json"

    if not os.path.exists(way):
        raise FileNotFoundError (f" config not found {way}")
    with open(way, "r", encoding="utf-8") as file:
        data = json.load(file)

    config["ip"] = data.get("ip", "10.0.0.2")
    config["host"] = data.get("host", "50.0.0.10")
    config["time"] = int(data.get("time", 30))
    config["run"] = int(data.get("run", 3))
    
    return config

def write_json(ip, host, time, vezes):

    data = {
    "ip": ip,
    "host": host,
    "time":time,
    "run": vezes
    }

    path_json = './config.json'

    with open(path_json, "w") as file:
        json.dump(data, file, indent=4)

path_json()

