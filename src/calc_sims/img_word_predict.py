import os
import sys
import argparse

sys.path.append('..')
from img_sim.img_predict import img_sim
from word_sim.word_predict import word_sim

class img_word_sim(object):
    __slots__ = ['img_model',
                 'word_model'
            ]
    
    def __init__(self, cnn_model_type='ResNet', lang='jp', word_dict='jp_wiki', feature=False, gpu_id=-1):
        self.img_model = img_sim(model=cnn_model_type,
                                lang=lang,
                                feature=feature,
                                gpu_id=gpu_id
                            )
        
        self.word_model = word_sim(word_dict=word_dict)

    def get_img_sim_norms(self, img, num=5, cutoff=0, sim_type='high'):
        return self.img_model.get_norms(img, num, cutoff, sim_type)

    def get_word_sim_norms(self, subject, img_sim_words, num=5, sim_type='low'):
        return self.word_model.get_norms(subject, img_sim_words, num, sim_type)
        
    def get_img_word_sim_norms(self, img, subject, num=5, cutoff=0, img_sim='high', word_sim='low'):
        
        img_sims, img_norms = self.img_model.get_norms(img, num, cutoff, img_sim)
        word_sims, word_norms = self.word_model.get_norms(subject, img_norms, num, word_sim)

        humor_scores, img_word_norms = self.__calc_score(img_sims, img_norms, word_sims, word_norms)

        result_norms = {'img_word_norms': img_word_norms, 'humor_scores': humor_scores, 'img_norms': img_norms, 'img_sims': img_sims, 'word_norms': word_norms, 'word_sims': word_sims}

        return result_norms

    def __calc_score(self, img_sims, img_norms, word_sims, word_norms):
        sims_dict = {}
        humor_scores = []
        img_word_norms = []

        for words, w_sim in zip(word_norms, word_sims):
            i_sim = img_sims[img_norms.index(words)]
            
            score = i_sim * (1 - w_sim)
            sims_dict[score] = words

        sims_dict = sorted(sims_dict.items(), key=lambda x: x[0], reverse=True)

        for score, norms in sims_dict:
            humor_scores.append(score)
            img_word_norms.append(norms)

        return humor_scores, img_word_norms

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--img', '-i', type=str, default=os.path.join('..', '..', 'sample_imgs', 'test.jpg'),
                        help="image you want to predict")
    parser.add_argument('--cnn_model_type', '-cmt', type=str, default='ResNet', choices=['ResNet', 'VGG16', 'AlexNet'],
                        help="CNN model type")
    parser.add_argument('--lang', '-l', type=str, default='jp',
                        help="language to output class")
    parser.add_argument('--word_dict', '-d', type=str, default='jp_wiki_ipadic', choices=['jp_wiki_ipadic', 'jp_wiki_neolog'],
                        help="type of dictionary for word2vec")
    parser.add_argument('--subject', '-s', type=str, default='男性',
                        help="subject to compare with proper norms")
    parser.add_argument('--norms', '-nr', type=str, default=[['イヌ', '犬', 'ドッグ', '飼い犬'], ['カカシ', 'かかし'], ['サボテン', 'カクタス'], ['カンガルー']],
                        help="proper norms to compare with subject")
    parser.add_argument('--num', '-n', type=int, default=5,
                        help="the number of output")
    parser.add_argument('--img_cutoff', '-ic', type=int, default=1,
                        help="the number of cutoff for top n sim image")
    parser.add_argument('--img_sim', '-is', type=str, default="high", choices=['high', 'low', 'rand'],
                        help="output img sim type")
    parser.add_argument('--word_sim', '-ws', type=str, default="low", choices=['high', 'low', 'rand'],
                        help="output word sim type")
    parser.add_argument('--feature', '-f', action='store_true',
                        help="use features to output class")
    parser.add_argument('--gpu', '-g', type=int, default=-1,
                        help="GPU ID(put -1 if you don't use gpu)")
    args = parser.parse_args()

    img_word_model = img_word_sim(cnn_model_type=args.cnn_model_type,
                                lang=args.lang,
                                word_dict=args.word_dict,
                                feature=args.feature,
                                gpu_id=args.gpu
                            )

    img_sims, img_norms = img_word_model.get_img_sim_norms(img=args.img,
                                                       num=args.num,
                                                       cutoff=args.img_cutoff,
                                                       sim_type=args.img_sim
                                                    )

    print('img sim result\n')
    print('sim: ', args.img_sim)
    print('sim\t\tnorm')
    for sim, norm in zip(img_sims, img_norms):
        print(round(sim, 5), '\t', norm)

    word_sims, word_norms = img_word_model.get_word_sim_norms(subject=args.subject,
                                                            img_sim_words=img_norms,
                                                            num=args.num,
                                                            sim_type=args.word_sim
                                                            )
    print('')
    print('word sim result\n')
    print('sim: ', args.word_sim)
    print('sim\t\tnorm')
    for sim, norm in zip(word_sims, word_norms):
        print(round(sim, 5), '\t', norm)
    
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

    for score, norm in zip(result_norms['humor_scores'], result_norms['img_word_norms']):
        print(round(score, 5), '\t', norm)
