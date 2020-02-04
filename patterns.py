# Ataque por método de Kasiski a cifrado de Vigenère
# Realizado por Pedro Leiva
import json


def get_cypher_text(file):
    try:
        data = open(file, 'rt', encoding='UTF-8')
        content = data.read().replace(" ", "").replace("\n", "")

        return get_patterns(content)
    except Exception as e:
        print("Error: No se pudo procesar el archivo:", e)
    finally:
        data.close()


def get_patterns(content, min_length=3, min_count=2):
    pattern = dict()

    try:
        for sub_length in range(min_length, int(len(content) / min_count)):
            for i in range(0, len(content) - sub_length):
                sub = content[i:i + sub_length]
                cnt = content.count(sub)
                if cnt >= min_count and sub not in pattern:
                    pattern[sub] = cnt

        return get_distance(content, pattern)
    except Exception as e:
        print("Error: No se pudo procesar la cadena a evaluar:", e)


def get_distance(content, patterns):
    pattern_indexes = dict()
    pattern_distances = dict()

    try:
        for key, repetitions in patterns.items():
            start = int()
            cant = list()
            for i in range(repetitions):
                if start <= len(content):
                    cant.append(content.index(key, start, len(content)))
                    start += cant[-1] + len(key)
            if key not in pattern_indexes:
                pattern_indexes[key] = cant
        for key, indexes in pattern_indexes.items():
            distance = list()
            for i in range(0, len(indexes)):
                if (i + 1) < len(indexes):
                    distance.append(indexes[i + 1] - indexes[i])
            if key not in pattern_distances:
                pattern_distances[key] = distance

        return get_greatest_common_divisor(content, pattern_distances)
    except Exception as e:
        print("Error: No se pudo procesar el patron:", e)


def set_gcd(x, y):
    while y:
        x, y = y, x % y

    return x


def get_greatest_common_divisor(content, numbers):
    best_patterns = dict()
    list_distances = list()

    try:
        for key in sorted(numbers, key=len, reverse=True):
            if len(max(numbers, key=len)) == len(key):
                best_patterns[key] = numbers[key]
        for value in best_patterns.values():
            for i in value:
                list_distances.append(i)
        if len(list_distances) >= 2:
            gcd = set_gcd(list_distances[0], list_distances[1])
            if len(list_distances) > 2:
                for i in range(2, len(list_distances)):
                    gcd = set_gcd(gcd, list_distances[i])
        else:
            gcd = list_distances[-1]

        return get_sub_cryptograms(content, gcd)
    except Exception as e:
        print("Error: No se pudo procesar la operación (MCD):", e)


def get_sub_cryptograms(content, gcd):
    sub_cryptograms = dict()
    initial_count = int()

    try:
        for i in range(4):
            chain = ''
            for position in range(initial_count, len(content), gcd):
                chain += content[position]
            sub_cryptograms[i + 1] = chain
            initial_count += 1

        return get_alphabet_counter(content, sub_cryptograms)
    except Exception as e:
        print("Error: No se pudo procesar la elaboración del sub-criptograma:", e)


def get_alphabet_counter(content, sub_cryptograms):
    alphabet = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    repeated_letters = dict()

    try:
        for key, value in sub_cryptograms.items():
            count_repeated = list()
            for letter in alphabet:
                count_repeated.append(value.count(letter))
            repeated_letters[key] = count_repeated

        return get_comparison_aeo_rule(content, repeated_letters, alphabet)
    except Exception as e:
        print("Error en la comparación con el alfabeto:", e)


def get_comparison_aeo_rule(content, repeated_letters, alphabet):
    comparison = dict()

    try:
        for key, value in repeated_letters.items():
            first_letter = list()
            for number in value:
                alphabet_length = len(value)
                number0 = value.index(number)
                number4 = (number0 + 4) % alphabet_length
                number11 = (number4 + 11) % alphabet_length
                first_letter.append(value[number0] + value[number4] + value[number11])
            comparison[key] = first_letter

        return get_key(content, comparison, alphabet)

    except Exception as e:
        print("Error en la comparación con la regla AEO:", e)


def get_key(content, aeo_comparison, alphabet):
    key = str()

    try:
        for value in aeo_comparison.values():
            max_value = max(value)
            key_index = value.index(max_value)
            key += alphabet[key_index]

        return decrypt(content, key, alphabet)
    except Exception as e:
        print("Error al obtener la llave:", e)


def decrypt(content, key, alphabet):
    content_length = len(content)
    key_length = len(key)
    multiplier = content_length // key_length
    product = key_length * multiplier
    remainder = content_length - product
    complete_key = str()

    if remainder != 0:
        complete_key += key * multiplier + key[0:remainder]
    else:
        complete_key += key * multiplier

    content_key = [list(content), list(complete_key)]

    relational_content = [(content_key[0][i], content_key[1][i]) for i in range(0, len(content_key[0]))]

    lte = []
    alpha = list(alphabet)

    return relational_content


# Esto ya no cuenta

def get_frequency_comparison(alphabet, repeated_letters):
    ubication = "C:\\Users\\pleiva\\OneDrive - Universidad Francisco Gavidia\\Documentos\\frequency_table.txt"
    comparison = dict()

    frequency_table_file = open(ubication, 'rt', encoding='UTF-8')
    frequency_table = json.loads(frequency_table_file.read().replace("\n", " "))

    for key, value in repeated_letters.items():
        multiplied_result = list()
        for letter in alphabet:
            multiplied_operator = value[alphabet.index(letter)] * frequency_table[letter]
            multiplied_result.append(round(multiplied_operator, 2))
        comparison[key] = multiplied_result

    return get_eao_rule(alphabet, comparison)


def get_eao_rule(alphabet, frequency_comparison):
    eao_rule = dict()
    eao_result = list()

    for letter in alphabet:
        eao_operation = ((alphabet.index(letter) + 4) % len(alphabet)) + \
                        ((alphabet.index(letter) + 15) % len(alphabet))
        eao_result.append(eao_operation)

    for key, value in frequency_comparison.items():
        multiply_results = list()
        for num1, num2 in zip(eao_result, value):
            multiply_results.append(round(num1 * num2, 2))
        eao_rule[key] = multiply_results

    return eao_rule


# x = input("Ubicación del archivo a evaluar: ")
print(get_cypher_text('C:\\Users\\pleiva\\OneDrive - Universidad Francisco Gavidia\\Documentos\\test.txt'))
