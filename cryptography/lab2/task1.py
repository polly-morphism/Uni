# Текст програми, що реалізує криптосистему Віженера
alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"


def encode_vizner(keyword, text):
    encoded = ""
    text = text.lower()
    keyword = keyword.lower()
    key_pos = 0
    for i in range(len(text)):
        if not text[i].isalpha():
            encoded += text[i]
        else:
            en_low = alphabet.index(keyword[key_pos % len(keyword)])
            en_sym = text[i].translate(
                str.maketrans(alphabet, alphabet[en_low:] + alphabet[:en_low])
            )
            encoded += en_sym
            key_pos += 1
    return encoded


print(encode_vizner("поліна", "верзун"))


def decode_vizner(keyword, text):
    decoded = ""
    text = text.lower()
    keyword = keyword.lower()
    key_pos = 0
    for i in range(len(text)):
        if not text[i].isalpha():
            decoded += text[i]
        else:
            dec_low = alphabet.index(keyword[key_pos % len(keyword)])
            dec_sym = text[i].translate(
                str.maketrans(alphabet[dec_low:] + alphabet[:dec_low], alphabet)
            )
            decoded += dec_sym
            key_pos += 1
    return decoded


print(decode_vizner("щястя", "внцєпрідя"))
