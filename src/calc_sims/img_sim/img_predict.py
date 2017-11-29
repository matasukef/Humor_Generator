import sys
import os
import argparse
import numpy as np
import chainer
import chainer.functions as F
from chainer import cuda
from chainer import serializers
sys.path.append('../..')
from common.img_proc import Img_proc

class img_sim(object):
    __slots__ = ['img_proc',
                'MODEL_PATH',
                'WORDS_DICT', 
                'model',
                'synsets',
                'feature',
                'gpu_id'
            ]

    def __init__(self, model='ResNet', lang="jp", feature=False, gpu_id=-1):
        self.img_proc = Img_proc("imagenet")
        #use features to predict output class
        self.feature = feature
        
        if not self.feature:
            self.MODEL_PATH, self.model = self.__choose_model(model)    
            self.WORDS_DICT = self.__choose_lang(lang)

            serializers.load_hdf5(self.MODEL_PATH, self.model)

            with open(self.WORDS_DICT, 'r') as f:
                self.synsets = f.read().split('\n')[:-1]
            
            self.gpu_id = gpu_id
            
    def __choose_model(self, model_type):

        if model_type == 'ResNet':
            from CNN.ResNet50 import ResNet
            from ENV import MODEL_RESNET
            MODEL_PATH = MODEL_RESNET
            model = ResNet()
        
        elif model_type == 'VGG16':
            from CNN.VGG16 import VGG16
            from ENV import MODEL_VGG16
            MODEL_PATH = MODEL_VGG16
            model = VGG16()
       
        elif model_type == 'AlexNet':
            from CNN.AlexNet import AlexNet
            from ENV import MODEL_ALEXNET
            MODEL_PATH = MODEL_ALEXNET
            model = AlexNet()

        return MODEL_PATH, model


    def __choose_lang(self, lang='jp'):
        if lang == 'jp':
            from ENV import NORM_LIST_JP
            WORDS_DICT = NORM_LIST_JP
        elif lang == 'en':
            from ENV import NORM_LIST_EN
            WORDS_DICT = NORM_LIST_EN

        return WORDS_DICT

    def __calc_pred(self, img):

        img_arr = self.img_proc.load_img(img)

        if self.gpu_id >= 0:
            cuda.get_device(args.gpu).use()
            self.model.to_gpu()
            img_arr = cuda.to_gpu(img_arr, device=args.gpu)

        with chainer.using_config('train', False):
            pred = self.model(img_arr, None).data

        if self.gpu_id >= 0:
            pred = cuda.to_cpu(pred)

        return pred

    def get_norms(self, img, num=5, cutoff=0, sim_type='high'):
        sims = []
        words = []

        if self.feature:
            pred = self.feature
        else:
            pred = self.__calc_pred(img)
        
        if sim_type == 'high':
            for i in np.argsort(pred)[0][::-1][cutoff:num+cutoff]:
                sims.append(pred[0][i])
                words.append(self.synsets[i].split(' ', 1)[1].split(','))
        elif sim_type == 'low':
            for i in np.argsort(pred)[0][::-1][-num:]:
                sims.append(pred[0][i])
                words.append(self.synsets[i].split(' ', 1)[1].split(','))
        elif sim_type == 'rand':
            for i in np.random.choice(np.argsort(pred)[0][::-1], num):
                sims.append(pred[0][i])
                words.append(self.synsets[i].split(' ', 1)[1].split(','))
        
        return sims, words

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--img', '-i', type=str, default=os.path.join('..', '..', '..', 'sample_imgs', 'test.jpg'),
                        help="image you want to predict")
    parser.add_argument('--gpu', '-g', type=int, default=-1,
                        help="GPU ID(put -1 if you don't use gpu)")
    parser.add_argument('--lang', '-l', type=str, default='jp',
                        help="language to output")
    parser.add_argument('--model_type', type=str, default='ResNet', choices=['ResNet', 'VGG16', 'AlexNet'],
                        help="model type")
    parser.add_argument('--num', '-n', type=int, default=5, 
                        help="the number of output")
    parser.add_argument('--sim', type=str, default='high', choices=['high', 'low', 'rand'],
                        help="output sim type")
    parser.add_argument('--cutoff', '-c', type=int, default=0, 
                        help="the number of ignoring top n similar class.\
                                This option is valid only when sim is high.")
    parser.add_argument('--feature', '-f', action='store_true',
                        help="use features to output class")
    args = parser.parse_args()

    img_model = img_sim(model=args.model_type, lang=args.lang, gpu_id=args.gpu, feature=args.feature)
    sims, words = img_model.get_norms(args.img, num=args.num, cutoff=args.cutoff, sim_type=args.sim)

    for sim, word in zip(sims, words):
        print(sim, word)
