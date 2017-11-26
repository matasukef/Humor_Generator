import sys
import argparse

from gensim.models import KeyedVectors

class word_sim(object):
    __slots__ = ['word_dict',
                 'model'
            ]

    def __init__(self, word_dict='wikipedia'):
        self.word_dict = word_dict
        if self.word_dict == 'wikipedia':
            sys.path.append('..')
            from ENV import W2V_WIKIPEDIA
            self.model = KeyedVectors.load_word2vec_format(W2V_WIKIPEDIA, binary=True)

    def get_words(self, subject, img_sim_words):
        low_sim_words = {}

        for norm in img_sim_words:
            res = self.model.wv.similarity(subject, norm)
            low_sim_words[norm] = round(float(res), 3)

        low_sim_words = sorted(low_sim_words.items(), key=lambda low_sim_words: low_sim_words[1])
        
        return low_sim_words

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--word_dict', '-d', type=str, default="wikipedia",
                        help="type of dictionary")
    parser.add_argument('--subject', '-s', type=str, default="男性",
                        help="Subject to compare with proper norms")
    parser.add_argument('--norms', '-n', type=str, default=['イヌ', 'カンガルー', 'カカシ', 'サボテン'],
                        help="proper norms to compare with subject")
    args = parser.parse_args()
    
    word_model = word_sim(args.word_dict)
    subject = args.subject
    proper_norms = args.norms
    
    low_sim_words = word_model.get_words(subject, proper_norms)

    for word, sim in low_sim_words:
        print(word, sim)
