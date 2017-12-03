import os
import sys
import argparse
import random
import random
import numpy as np
from janome.tokenizer import Tokenizer

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
                feature=True,
                gpu_id=0
            ):

        self.lang = lang
        self.cnn_model_type=cnn_model_type
        self.beamsize=beamsize
        self.depth_limit=depth_limit
        self.word_dict=word_dict
        self.feature = feature
        self.gpu_id = gpu_id
        
        self.t = Tokenizer(mmap=True)
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
        img_sim_words = self.img_word_model.get_img_sim_norms(
                                                            img=img,
                                                            num=num,
                                                            cutoff=cutoff,
                                                            sim_type=sim_type
                                                        )

        return img_sim_words

    def _calc_word_sim(self, subject, img_sim_words, num=5, sim_type='low'):
        word_sim_words = self.img_word_model.get_word_sim_norms(
                                                            subject=subject,
                                                            img_sim_words=img_sim_words,
                                                            num=num,
                                                            sim_type=sim_type
                                                        )
        
        return word_sim_words

    def _calc_img_word_sim(self, img, subject, multiple = 5, num=5, cutoff=0, img_sim='high', word_sim='low'):
        #change it to get dict of humor_scores and img_word_norms
        result_norms = self.img_word_model.get_img_word_sim_norms(
                                                        img=img,
                                                        subject=subject,
                                                        multiple=multiple,
                                                        num=num,
                                                        cutoff=cutoff,
                                                        img_sim=img_sim,
                                                        word_sim=word_sim
                                                    )

        return result_norms

    '''
    def __get_subject(self, captions):
        tmp_norms = []
        norm = ''
        norms = []
        
        for caption in captions:
            sen = caption['sentence']
            tokens = self.t.tokenize(sen)

            for token in tokens:
                surface =token.surface
                pos = token.part_of_speech.split(',')
                if pos[0] == '名詞':
                    tmp_norms.append(surface)
                    norm += surface
                elif len(norm) and surface == 'が':
                    norms.append(norm)
                    break
                elif pos[0] is not '名詞':
                    norm = ''
        
        return tmp_norms
    '''

    def __get_subject(self, captions):
            tmp_norms = []
            
            for caption in captions:
                norms = []
                norm = ''
                sen = caption['sentence']
                tokens = self.t.tokenize(sen)

                for token in tokens:
                    surface =token.surface
                    pos = token.part_of_speech.split(',')
                    if pos[0] == '名詞' and pos[1] != '非自立':
                        norm += surface
                    elif len(norm) and surface == 'が':
                        norms.append(norm)
                        break
                    elif pos[0] is not '名詞':
                        if len(norm):
                            norms.append(norm)
                        norm = ''
                
                tmp_norms.append(norms[-1])

            return tmp_norms


    def __to_colloquial(self, captions):
        colloq_captions = []

        for caption in captions:
            sen = caption['sentence']
            tokens = self.t.tokenize(sen)

            last_token = tokens[-1]
            last_surface = last_token.surface
            last_pos  = last_token.part_of_speech.split(',')

            if last_surface =='いる':
                caption['sentence'] = caption['sentence'][:-2]  + 'いますね！'
            elif last_surface == 'ある':
                caption['sentence'] = caption['sentence'][:-2]  + 'すね！'
            elif last_pos[0] == '名詞':
                caption['sentence'] = caption['sentence'] + 'ですね！'

            colloq_captions.append(caption)

        return colloq_captions

    def generate(self, img, num=5, multiple = 5, cutoff=1, img_sim='high', word_sim='low', colloquial=False):
        sim_dict = []
        humor_captions = []

        captions, img_feature = self._generate_captions(img)
        subjects = self.__get_subject(captions)
        
        if colloquial:
            captions = self.__to_colloquial(captions)

        #check subjects are same or not to reduce calc costs
        
        if self.feature:
            img= img_feature
        
        #tempolary use subjects[0] not subjects
        for subject in subjects:
            result_norms = self._calc_img_word_sim(
                                        img=img,
                                        subject=subject,
                                        multiple=multiple,
                                        num=num,
                                        cutoff=cutoff,
                                        img_sim=img_sim,
                                        word_sim=word_sim
                                    )

            sim_dict.append(result_norms)
        
        for caption, subject in zip(captions, subjects):
            cap = caption['sentence']

            for prop_norms in sim_dict:
                print(subject)
                humor_caps = [cap.replace(subject, random.choice(random.choices(norm['norm'])), 1).replace(' ', '') for norm in prop_norms['img_word_sim_words'] ]
                prop_norms['caption'] = caption
                prop_norms['humor_captions'] = humor_caps
                prop_norms['subject'] = subject
                humor_captions.append(prop_norms)
        
        return humor_captions

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--img', '-i', type=str, default=os.path.join('..', '..', 'sample_imgs', 'test.jpg'),
                        help="input image")
    parser.add_argument('--lang', '-l', type=str, default='jp', choices = ['jp', 'en', 'ch'],
                        help="choose language to generate captions")
    parser.add_argument('--cnn_model_type', '-ct', type=str, default='ResNet', choices=['ResNet', 'VGG16', 'AlexNet'],
                        help="CNN model type")
    parser.add_argument('--beamsize', '-b', type=int, default=1,
                        help="beamsize of neural image caption")
    parser.add_argument('--depth_limit', '-dl', type=int, default=50, 
                        help="max limit of generating tokens when constructing captions")
    parser.add_argument('--word_dict', type=str, default='jp_wiki_neolog', choices=['jp_wiki_neolog', 'jp_wiki_ipadic'],
                        help="word2vce dictionary")
    parser.add_argument('--img_multiply', '-mt', type=int, default=5,
                        help="multiply by num size of image classes is generated")
    parser.add_argument('--output_size', type=int, default=5,
                        help="output size")
    parser.add_argument('--cutoff', '-c',type=int, default=1,
                        help="the number of ignoring top n img sim word")
    parser.add_argument('--img_sim', '-im', type=str, default='high', choices=['high', 'low', 'rand'],
                        help="similarity of img sim")
    parser.add_argument('--word_sim', '-ws', type=str, default='low', choices=['high', 'low', 'rand'],
                        help="similarity of word sim")
    parser.add_argument('--colloquial', '-co', action='store_true',
                        help="return captions as colloquial")
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
                            feature=args.no_feature,
                            gpu_id=args.gpu
                        )

    humor_captions = model.generate(
                            img=args.img,
                            multiple=args.img_multiply,
                            num=args.output_size,
                            cutoff=args.cutoff,
                            img_sim=args.img_sim,
                            word_sim=args.word_sim,
                            colloquial=args.colloquial)
    

    print('caption results\n')
    for i, cap in enumerate(humor_captions):
        captions = cap['humor_captions']
        img_word_sim_words = cap['img_word_sim_words']
        img_sim_words = cap['img_sim_words']
        word_sim_words = cap['word_sim_words']

        scores = [img_word['score'] for img_word in img_word_sim_words]
        img_word_norms = [img_word['norm'] for img_word in img_word_sim_words]
        
        img_sim = [ img['sim'] for img in img_sim_words ]
        img_norms = [ img['norm'] for img in img_sim_words ]
        
        word_sim = [ word['sim'] for word in word_sim_words ]
        word_norms = [ word['norm'] for word in word_sim_words ]

        print('caption ', i)
        print('Original Caption:')
        print(cap['caption']['log_likelihood'], cap['caption']['sentence'])
        print('replaced with ', cap['subject'])

        print('\nHumor Captions')
        for cap in captions:
            print(cap)

        print('\nhumor score')
        for i_w_n, score in zip(img_word_norms, scores):
            print(score, i_w_n)

        print('\nimage sim')
        for i_n, i_s in zip(img_norms, img_sim):
            print(i_s, i_n)

        print('\nword sim')
        for w_n, w_s in zip(word_norms, word_sim):
            print(w_s, w_n)
