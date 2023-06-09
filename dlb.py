# Comando que busca por citações de leis brasileiras em arquivos CSV, e retorna
# o número de cada linha com uma ou mais ocorrência e a ocorrência, a uma saída
# específica. Caso nenhuma saída seja especificada, a saída padrão será usada
# (STDOUT).

import sys, re, csv


# Função de busca de ocorrências de citações de leis.
def scan(csv_data):
    #legal_devices = [
    #    'CC', 'CPC', 'CP', 'CPP', 'CTN', 'CLT', 'CDC', 'CTB',
    #    'CE', 'CF', 'CA', 'CM', 'CPM', 'CPPM', 'CBA', 'CBT',
    #    'Código Civil', 'Código de Processo Civil', 'Código de Processo',
    #    'Código de Processo Penal', 'Código Tributário Nacional',
    #    'Consolidação das Leis do Trabalho', 'Código de Defesa do Consumidor',
    #    'Código de Trânsito Brasileiro', 'Código Eleitoral', 'Código Florestal',
    #    'Código de Águas', 'Código de Minas', 'Código Penal Militar',
    #    'Código de Processo Penal Militar', 'Código Brasileiro de Aeronáutica',
    #    'Código Brasileiro de Telecomunicações', 'Código Comercial'
    #]
    p = {
        'art': r'((arts\.|artigos)?\s+(\dº|\d\d+)((,\s+(\dº|\d\d+))*\s+e\s+(\dº|\d\d+))?|(art\.|artigo)?\s+(\dº|\d\d+))',
        'par': r'(§§\s+(\dº|\d\d+)((,\s+(\dº|\d\d+))*\s+e\s+(\dº|\d\d+))?|§\s+(\dº|\d\d+))',
        'inc': r'((incs\.|incisos)?\s*(((?<!\w)(I|II|III)(?!\w)|(?<!\w)(IV|V|VI|VII|VIII|IX|X)(?!\w))|\d\d+)(,\s+(((?<!\w)(I|II|III)(?!\w)|(?<!\w)(IV|V|VI|VII|VIII|IX|X)(?!\w))|\d\d+))*\s+e\s+(((?<!\w)(I|II|III)(?!\w)|(?<!\w)(IV|V|VI|VII|VIII|IX|X)(?!\w))|\d\d+)|(inc.|inciso)?\s*(((?<!\w)(I|II|III)(?!\w)|(?<!\w)(IV|V|VI|VII|VIII|IX|X)(?!\w))|\d\d+))',
        'ali': r'([a-z](,\s+[a-z](?!\w))*)',
        'ite': r'((da|do)\s+(Lei(\s+(n\.nº))?\s+\d+(\.\d{3})?\/(\d\d){1,2}))',
    }

    output_ocurrences = []
    count = 0

    ld = r'((da|do)\s+((lei\s+(n\.|nº)?\s+\d+(\.\d{3})?\/(\d\d){1,2})?)|(([A-Z]{1,}|[A-Z][a-z]+)(\s+[A-Z][a-z]+)?))?'
    pattern = r'((arts\.|artigos)?\s+(\dº|\d\d+)((,\s+(\dº|\d\d+))*\s+e\s+(\dº|\d\d+))?|(art\.|artigo)?\s+(\dº|\d\d+)), (§§\s+(\dº|\d\d+)((,\s+(\dº|\d\d+))*\s+e\s+(\dº|\d\d+))?|§\s+(\dº|\d\d+)), ((incs\.|incisos)?\s*(((?<!\w)(I|II|III)(?!\w)|(?<!\w)(IV|V|VI|VII|VIII|IX|X)(?!\w))|\d\d+)(,\s+(((?<!\w)(I|II|III)(?!\w)|(?<!\w)(IV|V|VI|VII|VIII|IX|X)(?!\w))|\d\d+))*\s+e\s+(((?<!\w)(I|II|III)(?!\w)|(?<!\w)(IV|V|VI|VII|VIII|IX|X)(?!\w))|\d\d+)|(inc.|inciso)?\s*(((?<!\w)(I|II|III)(?!\w)|(?<!\w)(IV|V|VI|VII|VIII|IX|X)(?!\w))|\d\d+)), ([a-z](,\s+[a-z](?!\w))*), ((da|do)\s+(Lei(\s+(n\.nº))?\s+\d+(\.\d{3})?\/(\d\d){1,2}))'

    for row in csv_data:
        string = ' '.join(row[1:])
        count += search_patterns(string, p)

    print(count)
    
    #return output_ocurrences

def search_patterns(string, p):
    count = 0
    ld = r'((da|do)\s+((lei\s+(n\.|nº)?\s+\d+(\.\d{3})?\/(\d\d){1,2})?)|(([A-Z]{1,}|[A-Z][a-z]+)(\s+[A-Z][a-z]+)?))?'

    pattern_construct = ''
    for e in p:
        pattern_construct += p[e] + r', '
        if re.search(pattern_construct, string):
            for x in re.finditer(pattern_construct, string):
                print(x[0])
            count += 1

    return count


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
