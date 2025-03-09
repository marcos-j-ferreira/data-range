import json 
import os
import time
import subprocess
import sys
import re

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

command = {
    "down": (f"iperf3 -c {config['host']} -B {config['ip']} -t{config['time']}"),
    "up": (f"iperf3 -c {config['host']} -B {config['ip']} -t{config['time']} -R"),
    "netsh": ("netsh wlan show interface")
}

def run_script(command):

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        return result.stdout
    
    except Exception as e:
        print(f"Error: {e}")

def save_to_file(filename, content):

    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

"""
Meu programa até está, colocando as configurações, como lendo o json e reformatando as configurações. Está executando o comando e escrevendo em um arquivo
"""

data = {
    "up": [],
    "down": [],
    "range": {
        "sinal" : [],
        "TR": [],
        "TT": []
    }
}

def read_file(opetion, filename):

    if not os.path.exists(filename):
        print(f"not found: {filename}")
        return None

    
    if opetion == "netsh":
        
        padroes = {
            "Taxa de recepção": r"Taxa de recep[\s\S]*?\(Mbps\)\s*:\s*(\d+)",
            "Taxa de transmissão": r"Taxa de transmiss[\s\S]*?\(Mbps\)\s*:\s*(\d+)",
            "Sinal": r"Sinal\s*:\s*(\d+)%"
        }
        try:

            result = {}
            with open(filename, "r", encoding="utf-8") as f:
                conteudo = f.read()

                for c, p in padroes.items():
                    match = re.search(p, conteudo)
                    if match:
                        result[c] = match.group(1)
            
            data['range']['TT'].append(result['Taxa de transmissão'])
            data['range']['TR'].append(result["Taxa de recepção"])
            data['range']['sinal'].append(result["Sinal"])
        
        except Exception as e:
            print(f"Erro {e}")

    elif opetion == "down":

        try:

            padroes = {
                "sender" :  r"\[  5\]\s+0.00-30.01\s+sec\s+([\d\.]+)\s+MBytes\s+([\d\.]+)\s+Mbits/sec\s+sender",
                "receiver":  r"\[  5\]\s+0.00-30.01\s+sec\s+([\d\.]+)\s+MBytes\s+([\d\.]+)\s+Mbits/sec\s+sender"
            }


            ope = ["receiver", "sender"]

            with open (filename,"r") as f:
                result = f.read()
            match = re.search(padroes['sender'], result)
            
            if match:
                bandwidth = match.group(2)
                data["down"].append(bandwidth)

        except Exception as e:
            print(f"Erro: {e}")
    
    elif opetion == "up":

        try:

            padroes = {
                "sender" :  r"\[  5\]\s+0.00-30.01\s+sec\s+([\d\.]+)\s+MBytes\s+([\d\.]+)\s+Mbits/sec\s+sender",
                "receiver":  r"\[  5\]\s+0.00-30.01\s+sec\s+([\d\.]+)\s+MBytes\s+([\d\.]+)\s+Mbits/sec\s+sender"
            }


            ope = ["receiver", "sender"]

            with open (filename,"r") as f:
                result = f.read()
            match = re.search(padroes['sender'], result)
            
            if match:
                bandwidth = match.group(2)
                data["up"].append(bandwidth)

        except Exception as e:
            print(f"Erro: {e}")
        
    return data

"""
Até aqui ele está, lendo os arquivos que conterá os dados e armazenando em um dic
"""

def set_data():
    files = {
        "down": ["down-01.txt", "down-02.txt", "down-03.txt"],
        "up": ["up-01.txt", "up-02.txt", "up-03.txt"],
        "netsh": ["netsh-01.txt","netsh-02.txt","netsh-03.txt" ]
    }

    for category, file_list in files.items():
        for file_name in file_list:
            read_file(category, file_name)

def format_table(data):
    set_data()

    header = "+---------+----+------+----------------------------------------------------+"
    title = "| Rodadas | Up | Down |                        Data                        |"
    
    num_rodadas = len(data["up"])
    
    rows = []
    for i in range(num_rodadas):
        up = data["up"][i]
        down = data["down"][i]
        sinal = data["range"]["sinal"][i]
        tr = data["range"]["TR"][i]
        tt = data["range"]["TT"][i]
        
        row = f"|    {i+1}    | {up}  |  {down}   | 'T. Rec.': '{tr}', 'T. Tra.': '{tt}', 'Sinal': '{sinal}' |"
        rows.append(row)
    
    table = f"\nTabela de Resultados:\n{header}\n{title}\n{header}\n" + "\n".join(rows) + f"\n{header}"
    
    return table

print(format_table(data))
