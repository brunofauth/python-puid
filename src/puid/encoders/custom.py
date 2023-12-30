def custom(characters):
    char_codes = [ord(char) for char in characters]
    return lambda n: char_codes[n]
