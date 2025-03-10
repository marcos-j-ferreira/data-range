# README

## Descrição
Este script em Python automatiza testes de desempenho de rede utilizando a ferramenta `iperf3` e coleta informações da interface de rede usando `netsh`. Ele executa testes de upload e download, armazena os resultados em arquivos e gera uma tabela com os dados coletados.

## Funcionalidades
- Leitura e gravação de configurações em um arquivo JSON (`config.json`).
- Execução de testes de upload e download usando `iperf3`.
- Coleta de dados da interface de rede via `netsh`.
- Análise dos resultados armazenados em arquivos.
- Gera uma tabela com os resultados dos testes.
- Interface de linha de comando para configuração e execução do script.

## Requisitos
- Python 3.x
- `iperf3` instalado e acessível no caminho do sistema.
- Sistema operacional Windows (para comandos `netsh`).

## Instalação
1. Clone este repositório:
   ```sh
   git clone https://github.com/marcos-j-ferreira/data-range.git
   cd DATA-RANGE
   ```
2. Certifique-se de ter o `iperf3` instalado.
3. Execute o script com os comandos abaixo.

## Uso
O script pode ser executado com diferentes comandos:

### Exibir a configuração atual
```sh
python main.py INFO
```

### Configurar um novo setup
```sh
python main.py CONFIG <IP> <HOST> <TIME> <RUN>
```
Exemplo:
```sh
python main.py CONFIG 192.168.1.1 myserver.com 30 3
```

### Executar os testes
```sh
python main.py RUN
```

### Exibir logs dos testes
```sh
python main.py LOG <opcao>
```
Opções disponíveis:
- `down` (resultados de download)
- `up` (resultados de upload)
- `netsh` (dados da interface de rede)

Exemplo:
```sh
python main.py LOG down
```

## Estrutura dos Arquivos
- `main.py`: Script principal.
- `config.json`: Arquivo de configuração.
- `down-*.txt`, `up-*.txt`, `netsh-*.txt`: Arquivos contendo os resultados dos testes.
- `table.txt`: Arquivo gerado com os resultados formatados em tabela.

## Autor
Marcos Júnior,
marcos.j.lemes.ferreira.2004@gmail.com

