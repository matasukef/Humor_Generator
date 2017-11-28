from janome.tokenizer import Tokenizer

class get_subject(object):
    def __init__(self):
        self.t = Tokenizer()

    def extract(self, sentence):


        norm = ''
        tokens = self.t.tokenize(sentence)
        
        for token in tokens:
            surface = token.surface
            pos = token.part_of_speech.split(',')
            if pos[0] == '名詞':
                norm += surface
            elif len(norm) and surface == 'が':
                return norm
                break
            elif pos[0] is not '名詞':
                norm = ''
        
        return norm

'''
    def extract(self, sentences):

        norms = []
        for sentence in sentences:

            norm = ''
            tokens = self.t.tokenize(sentence)
            
            for token in tokens:
                surface = token.surface
                pos = token.part_of_speech.split(',')
                if pos[0] == '名詞':
                    norm += surface
                elif len(norm) and surface == 'が':
                    norms.append(norm)
                    break
                elif pos[0] is not '名詞':
                    norm = ''
            
        return norms
''' 
