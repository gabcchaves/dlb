# Comando que busca por citações de leis brasileiras em arquivos CSV, e retorna
# o número de cada linha com uma ou mais ocorrência e a ocorrência, a uma saída
# específica. Caso nenhuma saída seja especificada, a saída padrão será usada
# (STDOUT).

import sys, re, csv


# Função de busca de ocorrências de citações de leis.
def scan(csv_data):
    legal_devices = [
        'CC', 'CPC', 'CP', 'CPP', 'CTN', 'CLT', 'CDC', 'CTB',
        'CE', 'CF', 'CA', 'CM', 'CPM', 'CPPM', 'CBA', 'CBT',
        'Código Civil', 'Código de Processo Civil', 'Código de Processo',
        'Código de Processo Penal', 'Código Tributário Nacional',
        'Consolidação das Leis do Trabalho', 'Código de Defesa do Consumidor',
        'Código de Trânsito Brasileiro', 'Código Eleitoral', 'Código Florestal',
        'Código de Águas', 'Código de Minas', 'Código Penal Militar',
        'Código de Processo Penal Militar', 'Código Brasileiro de Aeronáutica',
        'Código Brasileiro de Telecomunicações', 'Código Comercial'
    ]
    p = {
        'law': r'((nº)|(n.))?\s+\d+(\.+\d)?\/\d\d(\d\d)?',
        'article': r'((artigos?)|(arts?\.))\s+',
        'paragraph': r'§\s+((((\w)+|\d+º|\d+),\s+)+((\w)+|\d+º|\d+)\s+e\s+((\w)+|\d+º|\d+)|((\w)+|\d+º|\d+))',
        'item': r'((incisos?)|(inc\.))\s+( (\w+)|(\w+\,\s+)+(\w+)\s+e\s+(\w+))'
    }
    ws = r'\s+'
    c_ws = '\s+,\s+'
    grammar = [
        '(Lei|lei)\s+' + p['law'],
        p['article'] + c_ws + p['item'] + c_ws + p['paragraph'] + r'\s+(da|do)\s+',
        p['article'] + c_ws + 'caput\s+(da|do)',
        p['paragraph'] + c_ws + p['article'] + c_ws + '(da|do)\s+',
    ]

    #output_ocurrences = []
    count = 0

    for row in csv_data:
        string = ' '.join(row[1:])
        for rule in grammar:
            if re.search(rule, string):
                print('\n\n' + rule)
                m = re.findall(re.compile(rule, re.IGNORECASE), string)

    print(count)
    
    #return output_ocurrences


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


# Procedimento que escreve a saída em um arquivo específico.
def pipe_to(dest, orig):
    with open(dest, 'w') as dest_file:
        csv_writer = csv.writer(dest_file)
        for row in orig:
            csv_writer.writerow([row])


def main():
    try:
        num_args = check_args()
        if num_args == 2:
            with open(sys.argv[1], 'r') as input_data:
                csv_data = csv.reader(input_data, delimiter=' ', quotechar='|')
                scan(csv_data)
            #print('2')
        else:
            with open(sys.argv[1], 'r') as input_data:
                csv_data = csv.reader(input_data, delimiter=' ', quotechar='|')
                scan(csv_data)
            #print('3')
            #scan('hi')
    except Exception as err:
        print(err)


if __name__ == "__main__":
    main()
else:
    raise Exception("'dlb.py' não deve ser usado como módulo.")
