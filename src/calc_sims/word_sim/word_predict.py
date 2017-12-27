import os
import argparse
import numpy as np

from gensim.models import KeyedVectors


class word_sim(object):
    __slots__ = ['word2vec_model_path',
                 'model',
                 ]

    def __init__(
        self,
        word2vec_model_path,
        binary
    ):

        self.word2vec_model_path = word2vec_model_path

        if binary:
            self.model = KeyedVectors.load_word2vec_format(
                self.word2vec_model_path, binary=binary)
        else:
            self.model = KeyedVectors.load(self.word2vec_model_path)

    def __getMedianIndex(self, sim_words):
        sims = np.asarray([word['sim'] for word in sim_words])
        med_value = np.median(sims)
        min_idx = np.abs(sims - med_value).argmin()

        return min_idx

    def __calc_sims(self, subject, img_sim_words):
        sim_words = []

        for norms in img_sim_words:
            for norm in norms:
                # try to check norm is exist in word2vec dict and calc sim
                try:
                    sim = self.model.wv.similarity(subject, norm)
                    sim_words.append({'norm': norms, 'sim': round(abs(sim), 10)})
                    break
                # raise except and not to add norm to dict if doensn't exist
                except KeyError:
                    continue

        sim_words = sorted(sim_words, key=lambda x: x['sim'])

        return sim_words

    def get_norms(self, subject, img_sim_words, num=5, sim_type='high'):

        sim_words = self.__calc_sims(subject, img_sim_words)

        # fix output num to length of img_sim_words if exceeds.
        num = len(sim_words) if len(sim_words) < num else num

        if sim_type == 'high':
            return sim_words[::-1][:num]

        elif sim_type == 'med':
            med_index = self.__getMedianIndex(sim_words)
            half_num, even = divmod(num, 2)
            start_idx = med_index - half_num
            end_idx = med_index + half_num + even

            return sim_words[start_idx: end_idx]

        elif sim_type == "mid":
            half_num, even = divmod(num, 2)
            start_idx = num - half_num
            end_idx = num + half_num + even

            return sim_words[start_idx: end_idx]

        elif sim_type == 'low':
            return sim_words[:num]

        elif sim_type == 'rand':
            return list(np.random.choice(sim_words, num, replace=False))

        else:
            raise TypeError(
                'Variable of sim_type is not one of these (high, low, rand)')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--word2vec_model_path', type=str, default=os.path.join('..', '..', '..', 'data', 'word2vec', 'models', 'ja_wikipedia_neolog.model'),
                        help="word2vec model path")
    parser.add_argument('--subject', '-s', type=str, default="女性",
                        help="Subject to compare with proper norms")
    parser.add_argument('--norms', '-nor', type=str, default=[['イヌ', '犬', 'ドッグ'], ['カンガルー'], ['カカシ', 'かかし'], ['サボテン', 'カクタス'], ['ネコ', 'ねこ', '猫'], ['コアラ'], ['マントヒヒ'], ['小鳥', '鳥'], ['ゴキブリ'], ['ザリガニ'], ['コックローチ']],
                        help="proper norms to compare with subject")
    parser.add_argument('--num', '-n', type=int, default=5,
                        help="the number of output")
    parser.add_argument('--sim', '-st', type=str, default="low", choices=['high', 'low', 'mid', 'rand', 'med'],
                        help="sim type")
    parser.add_argument('--binary', '-bin', action="store_true",
                        help="use binary data")
    args = parser.parse_args()

    word_model = word_sim(args.word2vec_model_path, args.binary)
    sim_words = word_model.get_norms(
        args.subject, args.norms, args.num, args.sim)

    print('')
    for sim_word in sim_words:
        print(sim_word['sim'], sim_word['norm'])
