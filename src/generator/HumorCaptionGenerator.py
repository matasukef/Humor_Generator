import os
import sys
import argparse
import random
import random
import numpy as np
from janome.tokenizer import Tokenizer

from get_subject import get_subject

sys.path.append('../calc_sims/img_sim')
sys.path.append('../calc_sims/word_sim')
sys.path.append('../image_caption')
sys.path.append('..')
from calc_sims.img_word_predict import img_word_sim
from image_caption.CaptionGenerator import CaptionGenerator

class HumorCaptionGenerator(object):
    __slots__ = ['lang',
                'cnn_model_type',
                'beamsize',
                'depth_limit',
                'word_dict',
                'img_sim_limit',
                'feature',
                'gpu_id',
                't',
                'caption_model',
                'img_word_model'
            ]

    def __init__(self,
                lang='jp',
                cnn_model_type='ResNet',
                beamsize=1,
                depth_limit=50,
                word_dict='jp_wiki_neolog',
                img_sim_limit=10,
                feature=True,
                gpu_id=0
            ):

        self.lang = lang
        self.cnn_model_type=cnn_model_type
        self.beamsize=beamsize
        self.depth_limit=depth_limit
        self.word_dict=word_dict
        self.img_sim_limit=img_sim_limit
        self.feature = feature
        self.gpu_id = gpu_id

        self.t = Tokenizer()
        self.caption_model = CaptionGenerator(
                                lang=self.lang,
                                cnn_model_type=self.cnn_model_type,
                                beamsize=self.beamsize,
                                depth_limit=self.depth_limit,
                                gpu_id=self.gpu_id

                                            
                )

        self.img_word_model = img_word_sim(
                                cnn_model_type=self.cnn_model_type,
                                lang=self.lang,
                                word_dict=self.word_dict,
                                feature=self.feature,
                                gpu_id=self.gpu_id
                            )

    def _generate_captions(self, img):
        captions, img_feature =  self.caption_model.generate_sentences(img)
        
        return captions, img_feature


    def _calc_img_sim(self, img, num=5, cutoff=1, sim_type='high'):
        img_sims, img_norms = self.img_word_model.get_img_sim_norms(
                                                            img=img,
                                                            num=num,
                                                            cutoff=cutoff,
                                                            sim_type=sim_type
                                                        )

        return img_sims, img_norms

    def _calc_word_sim(self, subject, img_sim_words, num=5, sim_type='low'):
        word_sims, word_norms =  self.img_word_model.get_word_sim_norms(
                                                            subject=subject,
                                                            img_sim_words=img_sim_words,
                                                            num=num,
                                                            sim_type=sim_type
                                                        )
        
        return word_sims, word_norms

    def _calc_img_word_sim(self, img, subject, num=5, cutoff=0, img_sim='high', word_sim='low'):
        #change it to get dict of humor_scores and img_word_norms
        sim_words = self.img_word_model.get_img_word_sim_norms(
                                                        img=img,
                                                        subject=subject,
                                                        num=num,
                                                        cutoff=cutoff,
                                                        img_sim=img_sim,
                                                        word_sim=word_sim
                                                    )



        return sim_words

    def __get_subject(self, captions):
        norm = ''
        norms = []
        
        for caption in captions:
            sen = caption['sentence']
            tokens = self.t.tokenize(sen)

            for token in tokens:
                surface =token.surface
                pos = token.part_of_speech.split(',')
                if pos[0] == '名詞':
                    norm += surface
                elif len(norm) and surface == 'が':
                    norms.append(norm)
                    break
                elif pos[0] is not '名詞':
                    norm = ''

        return norms

    def generate(self, img, num=5, cutoff=1, img_sim='high', word_sim='low'):
        sim_dict = []
        humor_captions = []

        captions, img_feature = self._generate_captions(img)
        subjects = self.__get_subject(captions)
        
        #check subjects are same or not to reduce calc costs
        
        if self.feature:
            img= img_feature

        #tempolary use subjects[0] not subjects
        for subject in subjects[0]:
            sim_words= self._calc_img_word_sim(
                                        img=img,
                                        subject=subject,
                                        num=num,
                                        cutoff=cutoff,
                                        img_sim=img_sim,
                                        word_sim=word_sim
                                    )

            sim_dict.append(sim_words)
        
        for caption, subject in zip(captions, subjects):
            cap = caption['sentence']

            for prop_norms in sim_dict:
                norms = prop_norms['img_word_norms']
                score = prop_norms['humor_scores']
                img_prop = prop_norms['img_norms']
                img_prop_sims = prop_norms['img_sims']
                word_prop = prop_norms['word_norms']
                word_prop_sims = prop_norms['word_sims']
                humor_caps = [cap.replace(subject, random.choice(random.choices(norm))).replace(' ', '') for norm in norms ]
                #humor_cap = cap.replace(subject, random.choice(norms))
                humor_captions.append({'humor_caption': humor_caps, 'img_word_norm': norms, 'score': score, 'img_norm': img_prop, 'img_sim': img_prop_sims, 'word_norm': word_prop, 'word_sim': word_prop_sims})

        return humor_captions

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--img', '-i', type=str, default=os.path.join('..', '..', 'sample_imgs', 'test.jpg'),
                        help="input image")
    parser.add_argument('--lang', '-l', type=str, default='jp', choices = ['jp', 'en', 'ch'],
                        help="choose language to generate captions")
    parser.add_argument('--cnn_model_type', '-ct', type=str, default='ResNet', choices=['ResNet', 'VGG16', 'AlexNet'],
                        help="CNN model type")
    parser.add_argument('--beamsize', '-b', type=int, default=3,
                        help="beamsize of neural image caption")
    parser.add_argument('--depth_limit', '-dl', type=int, default=50, 
                        help="max limit of generating tokens when constructing captions")
    parser.add_argument('--word_dict', type=str, default='jp_wiki_neolog', choices=['jp_wiki_neolog', 'jp_wiki_ipadic'],
                        help="word2vce dictionary")
    parser.add_argument('--img_sim_limit', '-isl', type=int, default=5,
                        help="max output size of words by calculating image sim")
    parser.add_argument('--output_size', type=int, default=5,
                        help="output size")
    parser.add_argument('--cutoff', '-c',type=int, default=1,
                        help="the number of ignoring top n img sim word")
    parser.add_argument('--img_sim', '-im', type=str, default='high', choices=['high', 'low', 'rand'],
                        help="similarity of img sim")
    parser.add_argument('--word_sim', '-ws', type=str, default='low', choices=['high', 'low', 'rand'],
                        help="similarity of word sim")
    parser.add_argument('--no_feature', '-f', action='store_false',
                        help="don't use image features to calc img sim class")
    parser.add_argument('--gpu', '-g', type=int, default=-1,
                        help="GPU ID (put -1 if you don't use gpu)")
    
    args = parser.parse_args()

    model = HumorCaptionGenerator(
                            lang=args.lang,
                            cnn_model_type=args.cnn_model_type,
                            beamsize=args.beamsize,
                            depth_limit=args.depth_limit,
                            word_dict=args.word_dict,
                            img_sim_limit=args.img_sim_limit,
                            feature=args.no_feature,
                            gpu_id=args.gpu
                        )

    humor_captions = model.generate(
                            img=args.img,
                           num=args.output_size,
                           cutoff=args.cutoff,
                           img_sim=args.img_sim,
                           word_sim=args.word_sim)
    

    print('caption results\n')
    for cap in humor_captions:
        captions = cap['humor_caption']
        img_word_norms = cap['img_word_norm']
        img_norms = cap['img_norm']
        word_norms = cap['word_norm']
        scores = cap['score']
        img_sim = cap['img_sim']
        word_sim = cap['word_sim']

        print(captions)
        print(img_word_norms)
        print(img_norms)
        print(word_norms)
        print(scores)
        print(img_sim)
        print(word_sim)
