# Comando que busca por citações de leis brasileiras em arquivos CSV, e retorna
# o número de cada linha com uma ou mais ocorrência e a ocorrência, a uma saída
# específica. Caso nenhuma saída seja especificada, a saída padrão será usada
# (STDOUT).

import sys, re, csv, unidecode


# Função de busca de ocorrências de citações de leis.
def scan(csv_data):
    p = {
        'art': r'((artigos?|arts?\.)\s+((\dº|\d\d+)((,\s+(\dº|\d\d+))*\s+e\s+(\dº|\d\d+))?))?',
        'par': r'(§§\s+(\dº|\d\d+)((,\s+(\dº|\d\d+))*\s+e\s+(\dº|\d\d+))|§\s+(\dº|\d\d+))?',
        'inc': r'((incs\.|incisos)?\s*(((?<!\w)(I|II|III)(?!\w)|(?<!\w)(IV|V|VI|VII|VIII|IX|X)(?!\w))|\d\d+)(,\s+(((?<!\w)(I|II|III)(?!\w)|(?<!\w)(IV|V|VI|VII|VIII|IX|X)(?!\w))|\d\d+))*\s+e\s+(((?<!\w)(I|II|III)(?!\w)|(?<!\w)(IV|V|VI|VII|VIII|IX|X)(?!\w))|\d\d+)|(inc.|inciso)?\s*(((?<!\w)(I|II|III)(?!\w)|(?<!\w)(IV|V|VI|VII|VIII|IX|X)(?!\w))|\d\d+))?',
        'ali': r'([a-z],((\s+[a-z],)*\s+e\s+[a-z],)?)?',
        'ite': r'(\d+, (\d+\s+e\s+\d+))?',
        'disp': r'((da|do)\s+(((Lei(\s+(n\.nº))?\s+\d+(\.\d{3})?\/(\d\d){1,2}))|([A-Z][a-z]+(\s+[a-z]+)?(\s+[A-Z][a-z]+)*|[A-Z]+)))',
        'sep1': r'(,\s+)?',
        'sep2': r'(,?\s+)?',
    }

    row_matches = []
    for row in csv_data:
        string = ' '.join(row[1:])
        no_diacritics = unidecode.unidecode(string)
        no_diacritics = re.sub(r"(\d)o", r"\1º", no_diacritics)
        row_matches.append((row[0], search_patterns(no_diacritics, p)))

    del row_matches[0]

    return row_matches

def search_patterns(string, p):
    count = 0
    matches = []

    # Ordem decrescente, do geral ao particular.
    pattern1 = p['art'] + p['sep1'] + p['par'] + p['sep1'] + p['inc'] + p['sep1'] + p['ali'] + p['sep1'] + p['ite'] + p['sep2'] + p['disp']
    pattern = r'((artigos?|arts?\.)?\s+((\dº|\d\d+)((,\s+(\dº|\d\d+))*\s+e\s+(\dº|\d\d+))?)(,\s+|\s+e\s+)?(,\s+|\s+e\s+)?((§§\s+(\dº|\d\d+)((,\s+(\dº|\d\d+))*\s+e\s+(\dº|\d\d+))?|§\s+(\dº|\d\d+))?(,\s+))*(((incs\.|incisos)?\s*(((?<!\w)(I|II|III)(?!\w)|(?<!\w)(IV|V|VI|VII|VIII|IX|X)(?!\w))|\d\d+)(,\s+(((?<!\w)(I|II|III)(?!\w)|(?<!\w)(IV|V|VI|VII|VIII|IX|X)(?!\w))|\d\d+))*\s+e\s+(((?<!\w)(I|II|III)(?!\w)|(?<!\w)(IV|V|VI|VII|VIII|IX|X)(?!\w))|\d\d+)|(inc.|inciso)?\s*(((?<!\w)(I|II|III)(?!\w)|(?<!\w)(IV|V|VI|VII|VIII|IX|X)(?!\w))|\d\d+))?(,\s+)?)*e?)([a-z],(\s+[a-z],)*)?((,?\s+)?(da|do)\s+(((Lei(\s+(n\.nº))?\s+\d+(\.\d{3})?\/(\d\d){1,2}))|([A-Z][a-z]+(\s+[a-z]+)?(\s+[A-Z][a-z]+)*|[A-Z]+)))?'

    if re.search(pattern, string):
        m = re.finditer(pattern, string)
        for i in m:
            matches.append(i.group(0))
            count += 1

    return (count, matches)


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
        results = []
        with open(sys.argv[1], 'r') as input_data:
            csv_data = csv.reader(input_data, delimiter=' ', quotechar='|')
            results = scan(csv_data)

        num_args = check_args()
        if num_args == 2:
            for x in results:
                print(x)
        else:
            with open(sys.argv[2], 'w') as output_file:
                csv_writer = csv.writer(output_file, delimiter=',')
                for x in results:
                    csv_writer.writerow(x)
    except Exception as err:
        print(err)


if __name__ == "__main__":
    main()
else:
    raise Exception("'dlb.py' não deve ser usado como módulo.")
