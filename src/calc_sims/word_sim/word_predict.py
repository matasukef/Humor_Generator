import sys
import argparse
import numpy as np

from gensim.models import KeyedVectors

class word_sim(object):
    __slots__ = ['word_dict',
                 'model'
            ]

    def __init__(self, word_dict='jp_wiki_ipadic'):
        self.word_dict = word_dict
        if self.word_dict == 'jp_wiki_ipadic':
            sys.path.append('../..')
            from ENV import W2V_WIKIPEDIA_IPADIC
            self.model = KeyedVectors.load(W2V_WIKIPEDIA_IPADIC)
            #self.model = KeyedVectors.load_word2vec_format(W2V_WIKIPEDIA, binary=True)
        elif self.word_dict == 'jp_wiki_neolog':
            sys.path.append('../..')
            from ENV import W2V_WIKIPEDIA_NEOLOG
            self.model = KeyedVectors.load(W2V_WIKIPEDIA_NEOLOG)
        else:
            raise NameError('name ' + self.word_dict + ' is not defined in dict type')


    def __calc_sims(self, subject, img_sim_words):
        sims_dict = {}
        sims = []
        words = []
        
        for norms in img_sim_words:
            for norm in norms:
                #try to check norm is exist in word2vec dict and calc sim
                try:
                    sim = self.model.wv.similarity(subject, norm)
                    sims_dict[sim] = norms
                    break
                #raise except and not to add norm to dict if doensn't exist
                except KeyError:
                    continue

        sims_dict = sorted(sims_dict.items(), key=lambda x: x[0])

        #sort words based on sims
        for sim, word in sims_dict:
            sims.append(sim)
            words.append(word)

        return sims, words
                
    def get_norms(self, subject, img_sim_words, num=5, sim_type='high'):

        sims, words= self.__calc_sims(subject, img_sim_words)
        
        #fix output num to length of img_sim_words if exceeds.
        if len(img_sim_words) < num:
            num = len(img_sim_words)

        if sim_type == 'high':
            return sims[::-1][:num], words[::-1][:num]
        elif sim_type == 'low':
            return sims[:num], words[:num]
        elif sim_type == 'rand':
            pair = list(zip(sims, words,))
            np.random.shuffle(pair)
            sims, words = zip(*pair)
            return sims[:num], words[:num]
        else:
            raise TypeError('Variable of sim_type is not one of these (high, low, rand)')

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--word_dict', '-d', type=str, default="jp_wiki_ipadic", choices=['jp_wiki_ipadic', 'jp_wiki_neolog'],
                        help="type of dictionary")
    parser.add_argument('--subject', '-s', type=str, default="男性",
                        help="Subject to compare with proper norms")
    parser.add_argument('--norms', '-nor', type=str, default=[['イヌ', '犬', 'ドッグ', 'tmp_word4except'], ['カンガルー'], ['カカシ', 'tmp_word4test_except2', 'かかし'], ['tmp_word4test_except3', 'サボテン', 'カクタス']],
                        help="proper norms to compare with subject")
    parser.add_argument('--num', '-n', type=int, default=5,
                        help="the number of output")
    parser.add_argument('--sim_type', '-st', type=str, default="low", choices=['high', 'low', 'rand'],
                        help="sim type")
    args = parser.parse_args()
    
    word_model = word_sim(args.word_dict)
    subject = args.subject
    proper_norms = args.norms
    
    sims, words = word_model.get_norms(subject, proper_norms, args.num, args.sim_type)

    for sim, word in zip(sims, words):
        print(sim, word)
