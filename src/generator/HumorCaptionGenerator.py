import os
import sys
import argparse
import random
from janome.tokenizer import Tokenizer

from get_subject import get_subject

sys.path.append('..')
from img_sim.img_predict import img_sim
from word_sim.word_predict import word_sim
from calc_sim.img_word_predict import img_word_sim
from image_caption.CaptionGenerator import CaptionGenerator

class HumorCaptionGenerator(object):
    def __init__(self,
                lang='jp',
                cnn_model_type='ResNet',
                beamsize=1,
                depth_limit=50,
                word_dict='ja_wikipedia_neolog',
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

    def _generate_caption(self, img):
        captions =  self.caption_model.generate_sentences(img)
        
        return captions, prob


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

    def __get_subject(self, sentences):
        norm = ''
        norms = []
        
        for sen in sentences:

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
        humor_captions = []

        captions = self._generate_captions(img)
        subjects = self.__get_subject(captions)

        for subject in subjects:
            sim_words= self._calc_img_word_sim(
                                        img=img,
                                        subject=subject,
                                        num=num,
                                        cutoff=cutoff,
                                        img_sim=img_sim,
                                        word_sim=word_sim
                                    )
            
            
        for caption, subject in captions, subjects:
            
            for prop_norm in sim_words:
                pass

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
    parser.add_argument('--word2vec_dict', type=str, default='wikipedia',
                        help="word2vce dictionary")
    parser.add_argument('--img_sim_limit', '-isl', type=int, default=5,
                        help="max output size of words by calculating image sim")
    parser.add_argument('--output_size', type=int, default=5,
                        help="output size")
    parser.add_argument('--gpu', '-g', type=int, default=-1,
                        help="GPU ID (put -1 if you don't use gpu)")
    
    args = parser.parse_args()

    caption_generator = CaptionGenerator(
                        lang=args.lang,
                        cnn_model_type=args.cnn_model_type,
                        beamsize=args.beamsize,
                        depth_limit=args.depth_limit,
                        gpu_id=args.gpu,
                    )

    img_model = img_sim(
                model=args.cnn_model_type,
                gpu_id = args.gpu
            )

    word_model = word_sim(
                word_dict=args.word2vec_dict
            )

    get_subject = get_subject()

    captions = caption_generator.generate_sentences(args.img)
    caption = captions[0]['sentence']
    print(caption)
    subject = get_subject.extract(caption)
    high_img_sim_words = img_model.get_words(args.img, num=args.img_sim_limit, lang=args.lang)
    low_img_sim_words = word_model.get_words(subject[0], high_img_sim_words)

    humor_captions = []

    for word, sim in low_img_sim_words:
        humor_cap = caption.replace(subject, word)
        humor_captions.append(humor_cap)
    
    for cap in humor_captions:
        print(cap)
