from janome.tokenizer import Tokenizer

def extract_subject(sentence):
    t = Tokenizer()
    tokens = t.tokenize(sentence)
    norm = ''
    
    for token in tokens:
        
        surface = token.surface
        part1, part2, part3, part4 = token.part_of_speech.split(',')
        print(surface, part1, part2, part3, part4)
        if len(norm) and part2 == '格助詞':
            return norm

        if part1 == '名詞' and part2 != '非自立':
            norm += surface
        else:
            norm = ''

    return 0
