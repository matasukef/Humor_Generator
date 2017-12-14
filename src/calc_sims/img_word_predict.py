import os
import sys
import argparse

sys.path.append('..')
sys.path.append('img_sim')
sys.path.append('word_sim')
from img_predict import img_sim
from word_predict import word_sim
# from img_sim.img_predict import img_sim
# from word_sim.word_predict import word_sim


class img_word_sim(object):
    __slots__ = ['img_model',
                 'word_model',
                 'cnn_model_path',
                 'cnn_model_type',
                 'word2vec_model_path',
                 'class_table_path',
                 'feature',
                 'gpu_id',
                 'mean'
                 ]

    def __init__(
        self,
        cnn_model_path,
        word2vec_model_path,
        class_table_path,
        word2vec_binary_data=True,
        cnn_model_type='ResNet',
        feature=False,
        gpu_id=-1,
        mean='imagenet'
    ):

        self.cnn_model_path = cnn_model_path
        self.word2vec_model_path = word2vec_model_path
        self.class_table_path = class_table_path
        self.cnn_model_type = cnn_model_type
        self.feature = feature
        self.gpu_id = gpu_id
        self.mean = mean

        self.img_model = img_sim(
            cnn_model_path=cnn_model_path,
            cnn_model_type=cnn_model_type,
            class_table_path=class_table_path,
            gpu_id=gpu_id,
            mean=mean,
            feature=feature
        )

        self.word_model = word_sim(
            word2vec_model_path=word2vec_model_path,
            binary=word2vec_binary_data
        )

    def get_img_sim_norms(
            self,
            img,
            num=5,
            cutoff=0,
            sim_type='high'
    ):
        return self.img_model.get_norms(img, num, cutoff, sim_type)

    def get_word_sim_norms(
            self,
            subject,
            img_sim_words,
            num=5,
            sim_type='low'
    ):

        img_sim_norms = []
        for img_sim_word in img_sim_words:
            norm = img_sim_word['norm']
            img_sim_norms.append(norm)

        return self.word_model.get_norms(subject, img_sim_norms, num, sim_type)

    def get_img_word_sim_norms(
            self,
            img,
            subject,
            num=5,
            cutoff=0,
            img_sim='high',
            word_sim='low'
    ):

        img_sim_words = self.get_img_sim_norms(img, num, cutoff, img_sim)
        word_sim_words = self.get_word_sim_norms(
            subject, img_sim_words, num, word_sim)

        img_word_sim_words = self.__calc_score(
                img_sim_words,
                word_sim_words,
                img_sim, word_sim
        )

        result_norms = {'img_word_sim_words': img_word_sim_words,
                        'img_sim_words': img_sim_words,
                        'word_sim_words': word_sim_words
                        }

        return result_norms

    def __calc_score(self, img_sim_words, word_sim_words, img_sim, word_sim):
        sim_words = []

        for word_sim_word in word_sim_words:

            # it would be more efficient
            i_sim = [img_sim_word['sim']
                     for img_sim_word in img_sim_words if img_sim_word['norm'] == word_sim_word['norm']]

            if img_sim == 'low' and word_sim == 'low':
                score = (1 - i_sim[0]) * (1 - word_sim_word['sim'])
            elif img_sim == 'low' and word_sim == 'high':
                score = (1 - i_sim[0]) * word_sim_word['sim']
            elif img_sim == 'high' and word_sim == 'low':
                score = i_sim[0] * (1 - word_sim_word['sim'])
            elif img_sim == 'high' and word_sim == 'high':
                score = i_sim[0] * word_sim_word['sim']
            else:
                # temporary use this score metrics
                # because it's difficult to caluculate scores for mid sim
                score = i_sim[0] * (1 - word_sim_word['sim'])

            sim_words.append({'score': round(score, 10),
                              'norm': word_sim_word['norm']})

        sim_words = sorted(sim_words, key=lambda x: x['score'], reverse=True)

        return sim_words


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--img', '-i', type=str, default=os.path.join('..', '..', 'sample_imgs', 'test.jpg'),
                        help="image you want to predict")
    parser.add_argument('--cnn_model_path', type=str, default=os.path.join('..', '..', 'data', 'models', 'cnn', 'ResNet50.model'),
                        help="CNN model path")
    parser.add_argument('--cnn_model_type', '-cmt', type=str, default='ResNet', choices=['ResNet', 'VGG16', 'AlexNet'],
                        help="CNN model type")
    parser.add_argument('--word2vec_model_path', type=str, default=os.path.join('..', '..', 'data', 'word2vec', 'models', 'ja_wikipedia_neolog.model'),
                        help="type of dictionary for word2vec")
    parser.add_argument('--word2vec_binary_data', action='store_true',
                        help="help binary data for word2vec model")
    parser.add_argument('--class_table_path', type=str, default=os.path.join('..', '..', 'data', 'wordnet', 'resnet_synsets_jp_modified.txt'),
                        help="class table path to output prob of image class")
    parser.add_argument('--mean', type=str, default='imagenet',
                        help="method to preprocess images")
    parser.add_argument('--feature', '-f', action='store_true',
                        help="use features to output class")
    parser.add_argument('--subject', '-s', type=str, default='男性',
                        help="subject to compare with proper norms")
    parser.add_argument('--norms', '-nr', type=str, default=[['イヌ', '犬', 'ドッグ', '飼い犬'], ['カカシ', 'かかし'], ['サボテン', 'カクタス'], ['カンガルー']],
                        help="proper norms to compare with subject")
    parser.add_argument('--num', '-n', type=int, default=5,
                        help="the number of output")
    parser.add_argument('--img_cutoff', '-ic', type=int, default=1,
                        help="the number of cutoff for top n sim image")
    parser.add_argument('--img_sim', '-is', type=str, default="high", choices=['high', 'low', 'rand', 'mid', 'med'],
                        help="output img sim type")
    parser.add_argument('--word_sim', '-ws', type=str, default="low", choices=['high', 'low', 'rand', 'mid', 'med'],
                        help="output word sim type")
    parser.add_argument('--gpu', '-g', type=int, default=-1,
                        help="GPU ID(put -1 if you don't use gpu)")
    args = parser.parse_args()

    img_word_model = img_word_sim(
        cnn_model_path=args.cnn_model_path,
        word2vec_model_path=args.word2vec_model_path,
        word2vec_binary_data=args.word2vec_binary_data,
        cnn_model_type=args.cnn_model_type,
        class_table_path=args.class_table_path,
        gpu_id=args.gpu,
        mean=args.mean,
        feature=args.feature
    )

    img_sim_words = img_word_model.get_img_sim_norms(img=args.img,
                                                     num=args.num,
                                                     cutoff=args.img_cutoff,
                                                     sim_type=args.img_sim
                                                     )

    print('img sim result\n')
    print('sim: ', args.img_sim)
    print('sim\t\tnorm')

    for img_sim_word in img_sim_words:
        print(round(img_sim_word['sim'], 10), '\t', img_sim_word['norm'])

    word_sim_words = img_word_model.get_word_sim_norms(subject=args.subject,
                                                       img_sim_words=img_sim_words,
                                                       num=args.num,
                                                       sim_type=args.word_sim
                                                       )
    print('')
    print('word sim result\n')
    print('sim: ', args.word_sim)
    print('sim\t\tnorm')
    for word_sim_word in word_sim_words:
        print(round(word_sim_word['sim'], 10), '\t', word_sim_word['norm'])

    result_norms = img_word_model.get_img_word_sim_norms(img=args.img,
                                                         subject=args.subject,
                                                         num=args.num,
                                                         cutoff=args.img_cutoff,
                                                         img_sim=args.img_sim,
                                                         word_sim=args.word_sim
                                                         )

    print('')
    print('img word sim result\n')
    print('compare with ', args.subject)
    print('img_sim: ', args.img_sim)
    print('word_sim: ', args.word_sim)
    print('sim\t\tnorm')

    for img_word_sim_word in result_norms['img_word_sim_words']:
        print(round(img_word_sim_word['score'], 5),
              '\t', img_word_sim_word['norm'])
