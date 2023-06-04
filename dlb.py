# Comando que busca por citações de leis brasileiras em arquivos CSV, e retorna
# o número de cada linha com uma ou mais ocorrência e a ocorrência, a uma saída
# específica. Caso nenhuma saída seja especificada, a saída padrão será usada
# (STDOUT).

import sys, re, csv


# Função de busca de ocorrências de citações de leis.
def scan(csv_data):
    output_ocurrences = []

    for row in csv_data:
        string = ' '.join(row[1:])
    
    return output_ocurrences


# Procedimento de verificação de argumentos passados ao programa.
def check_args():
    num_args = 0

    if len(sys.argv) == 2:
        num_args = 2
    elif len(sys.argv) == 3:
        num_args = 3
    else:
        raise Exception("Você deve passar os dados de entrada como argumento.")

    return  num_args


def main():
    try:
        num_args = check_args()
        if num_args == 2:
            #with open(sys.argv[1], 'r') as input_data:
            #    csv_data = csv.reader(input_data, delimiter=' ', quotechar='|')
            #    scan(csv_data)
            print('2')
        else:
            #with open(sys.argv[1], 'r') as input_data:
            #    csv_data = csv.reader(input_data, delimiter=' ', quotechar='|')
            #    scan(csv_data)
            print('3')
    except Exception as err:
        print(err)


if __name__ == "__main__":
    main()
else:
    raise Exception("'dlb.py' não deve ser usado como módulo.")
