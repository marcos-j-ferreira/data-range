import json
import os
import time
import subprocess
import sys
import re

par = "False"

if len(sys.argv) > 1:
    par = sys.argv[1].upper()

if par == "CLEAR":
    os.system("cls")

def clear():
    os.system("cls")

config = {
    "ip": None,
    "host": None,
    "time":None,
    "run": 3
}

files = {
        "down": ["down-1.txt", "down-2.txt", "down-3.txt"],
        "up": ["up-1.txt", "up-2.txt", "up-3.txt"],
        "netsh": ["netsh-1.txt","netsh-2.txt" ,"netsh-3.txt"]
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
    # config["run"] = int(data.get("run", 3))

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

    print(command)

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        return result.stdout
    
    except Exception as e:
        print(f"Error: {e}")

def save_to_file(filename, content):

    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

data = {
    "up": [],
    "down": [],
    "range": {
        "sinal" : [],
        "TR": [],
        "TT": []
    }
}

filess = {"netsh": ["netsh-1.txt","netsh-1.txt","netsh-2.txt" ,"netsh-3.txt"]}

def read_file(option, filename):
    if not os.path.exists(filename):
        print(f"Arquivo não encontrado: {filename}")
        return None
    
    global data
    
    if option == "netsh":
        patterns = {
            "Taxa de recepção": r"Taxa de recep[\s\S]*?\(Mbps\)\s*:\s*(\d+)",
            "Taxa de transmissão": r"Taxa de transmiss[\s\S]*?\(Mbps\)\s*:\s*(\d+)",
            "Sinal": r"Sinal\s*:\s*(\d+)%"
        }
        try:
            result = {}
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
            
            for key, pattern in patterns.items():
                match = re.search(pattern, content)
                if match:
                    result[key] = int(match.group(1))
            
            if result:
                data['range']['TT'].append(result.get('Taxa de transmissão', 0))
                data['range']['TR'].append(result.get("Taxa de recepção", 0))
                data['range']['sinal'].append(result.get("Sinal", 0))
            
        except Exception as e:
            print(f"Erro ao processar netsh: {e}")
    
    elif option in ["down", "up"]:
        try:
            
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
            
            pattern = r"\[\s*\d+\]\s+0.00-\d+\.\d{2}\s+sec\s+[\d\.]+\s+[GM]Bytes\s+([\d\.]+)\s+Mbits/sec\s+(sender|receiver)"
            matches = re.findall(pattern, content)
            
            if matches:
                for bandwidth, direction in matches:
                    bandwidth_value = float(bandwidth)
                    if option == "down" and direction == "receiver":
                        data["down"].append(bandwidth_value)
                    elif option == "up" and direction == "sender":
                        data["up"].append(bandwidth_value)

            if matches:
                for bandwidth, direction in matches:
                    bandwidth_value = float(bandwidth)
                    if option == "up" and direction == "receiver":
                        data["up"].append(bandwidth_value)
                    # elif option == "down" and direction == "sender":
                    #     data["down"].append(bandwidth_value)
            else:
                print("Nenhum valor final de Bandwidth encontrado.")
        
        except Exception as e:
            print(f"Erro ao processar {option}: {e}")
    
    return data

def set_data():
    data["up"].clear()
    data["down"].clear()
    data["range"]["sinal"].clear()
    data["range"]["TR"].clear()
    data["range"]["TT"].clear()
    
    for category, file_list in files.items():
        for file_name in file_list:
            read_file(category, file_name)

def format_table(data):
    #print(data)
    header = "+---------+---------+---------+--------------------------------+"
    title = "| Rodadas |   Up    |  Down   |       Dados                    |"
    separator = header
    
    num_rodadas = len(data["up"]) if len(data["up"]) > len(data["down"]) else len(data["down"])
    rows = []

    for i in range(3):
        up = data["up"][i] if i < len(data["up"]) else "N/A"
        down = data["down"][i] if i < len(data["down"]) else "N/A"
        sinal = data["range"]["sinal"][i] if i < len(data["range"]["sinal"]) else "N/A"
        tr = data["range"]["TR"][i] if i < len(data["range"]["TR"]) else "N/A"
        tt = data["range"]["TT"][i] if i < len(data["range"]["TT"]) else "N/A"
        
        row = f"|    {i+1}    | {up:<7} | {down:<7} | Rec.: {tr}, Tra.: {tt}, S: {sinal}% |"
        rows.append(row)
    
    table = f"\nTabela de Resultados:\n{separator}\n{title}\n{separator}\n" + "\n".join(rows) + f"\n{separator}"
    
    with open("table.txt", "w", encoding="utf-8") as f:
        f.write(table)
    
    return table

def main():
    run = config["run"]

    c = 1

    for i in range(1, 4):
        print(f"Executando rodada {i}...")

        print("Executando teste de download...")
        down_output = run_script(command["down"] + f" --logfile down-{i}.txt")
        #time.sleep(config["time"] + 2)  

        print("Executando teste de upload...")
        up_output = run_script(command["up"] + f" --logfile up-{i}.txt")
        #time.sleep(config["time"] + 2)  

        print("Executando análise de rede...")
        netsh_output = run_script(command["netsh"])
        save_to_file(filess["netsh"][i], netsh_output)
        #time.sleep(2)  

        c = 0

    set_data()

    tabela = format_table(data)
    print(tabela)
    print("Tabela de resultados salva em 'table.txt'.")

c = {
    "ip":None,
    "host":None,
    "time": 30,
    "run": 3
}

def read(opetion=None, number=3):
    ope = opetion.upper()

    if ope is None:
        print("Escolha uma opção\n Down\n Up\n Netsh")

    if ope == "DOWN":
        clear()
        for i in range(0,3):
            with open(files["down"][i], "r", encoding="utf-8") as f:
                result = f.read()
                print(result)
    
    if ope == "UP":
        clear()

        for i in range(0,3):
            with open(files["up"][i], "r", encoding="utf-8") as f:
                result = f.read()
                print(result)
    
    if ope == "NETSH":
        clear()

        for i in range(0,3):
            with open(files["netsh"][i], "r", encoding="utf-8") as f:
                result = f.read()
                print(result)

def show_help():
    clear()
    help_text = """
Uso: python main.py [OPÇÃO] [ARGUMENTOS]

Opções disponíveis:
  INFO, -I                             Exibe a configuração atual do setup.
  CONFIG, -C <IP> <HOST> <TIME> <RUN>  Define a configuração e salva no JSON.
  RUN, -R                              Executa o script principal.
  LOG, -L   <file>                     Mostra todos os logs dos arquivos
  DELETE, -D                           Deleta todos os arquivos de log.
  TABLE, -T                            Mostra a tabela de resultados.

Exemplos:
  python main.py INFO
  python main.py CONFIG 192.168.1.1 myserver.com 30 3
  python main.py RUN
  python main.py LOG down
  python main.py DELETE
  python main.py TABLE
"""
    print(help_text)

def delete_files():
    for category, file_list in files.items():
        for file in file_list:
            if os.path.exists(file):
                os.remove(file)
    print("Cache limpo")


def parse_args():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)

    par = sys.argv[1].upper()
    comandos = {
        "INFO": handle_info,
        "-I": handle_info,
        "CONFIG": handle_config,
        "-C": handle_config,
        "RUN": handle_run,
        "-R": handle_run,
        "LOG": handle_log,
        "-L": handle_log,
        "-D": delete_files,
        "DELETE": delete_files,
        "-T": show_table,
        "TABLE": show_table
    }

    if par in comandos:
        comandos[par]()
    else:
        print("Erro: Comando desconhecido.")
        show_help()
        sys.exit(1)

def show_table():
    set_data()
    tabela = format_table(data)
    print(tabela)

def handle_info():
    config = path_json()
    print(f"Seu setup está configurado da seguinte forma:\n"
          f"IP: {config['ip']}\n"
          f"HOST: {config['host']}\n"
          f"TIME: {config['time']}\n"
          f"RUN: {config['run']}")

def handle_config():
    if len(sys.argv) != 6:
        print("Erro: Argumentos insuficientes para CONFIG. Use:")
        print("python main.py CONFIG <IP> <HOST> <TIME> <RUN>")
        sys.exit(1)
    
    ip, host, time, run = sys.argv[2:6]
    write_json(ip, host, time, run)

def handle_run():
    delete_files()
    main()

def handle_log():
    if len(sys.argv) < 3:
        print("Necessário passar um nome de arquivo. Opções: [up, down, netsh]")
        return
    
    result = sys.argv[2].upper()
    opcoes_validas = {"DOWN": "down", "UP": "UP", "NETSH": "NETSH"}
    
    if result in opcoes_validas:
        print(result)
        read(opcoes_validas[result])
    else:
        print("Escolha uma opção válida:\nOpções: [down, up, netsh]")

parse_args()