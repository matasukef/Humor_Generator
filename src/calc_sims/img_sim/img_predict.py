import sys
import os
import argparse
import numpy as np
import chainer
import chainer.functions as F
from chainer import cuda
from chainer import serializers
sys.path.append('../common')
from img_proc import Img_proc

class img_sim(object):
    __slots__ = ['img_proc',
                'MODEL_PATH',
                'WORDS_DICT', 
                'WORDS_DICT_JP',
                'model',
                'synsets',
                'synsets_jp',
                'gpu_id'
            ]

    def __init__(self, model='ResNet', gpu_id=-1):
        self.img_proc = Img_proc("imagenet")
        
        if model == 'ResNet':
            from CNN.ResNet50 import ResNet
            from ENV import MODEL_RESNET, WORDS_RESNET, WORDS_RESNET_JP
            self.MODEL_PATH = MODEL_RESNET
            self.WORDS_DICT = WORDS_RESNET
            self.WORDS_DICT_JP = WORDS_RESNET_JP
            self.model = ResNet()
        
        elif model == 'VGG16':
            from CNN.VGG16 import VGG16
            from ENV import MODEL_VGG16, WORDS_VGG16, WORDS_VGG16_JP
            self.MODEL_PATH = MODEL_VGG16
            self.WORDS_DICT = WORDS_VGG16
            self.WORDS_DICT_JP = WORDS_VGG16_JP
            self.model = VGG16()
       
        elif model == 'AlexNet':
            from CNN.AlexNet import AlexNet
            from ENV import MODEL_ALEXNET, WORDS_ALEXNET, WORDS_ALEXNET_JP
            self.MODEL_PATH = MODEL_ALEXNET
            self.WORDS_DICT = WORDS_ALEXNET
            self.WORDS_DICT_JP = WORDS_ALEXNET_JP
            self.model == AlexNet()

        serializers.load_hdf5(self.MODEL_PATH, self.model)

#merge synset to load once
# set path to synset and set init 
        with open(self.WORDS_DICT, 'r') as f:
            self.synsets = f.read().split('\n')[:-1]
        
        
        with open(self.WORDS_DICT_JP, 'r') as f:
            self.synsets_jp = f.read().split('\n')[:-1]
        self.gpu_id = gpu_id
        

    def similarity(self, img, num=5, lang='en'):
        img_arr = self.img_proc.load_img(img)

        if self.gpu_id >= 0:
            cuda.get_device(args.gpu).use()
            self.model.to_gpu()
            img_arr = cuda.to_gpu(img_arr, device=args.gpu)

        with chainer.using_config('train', False):
            pred = self.model(img_arr, None).data
        
        if self.gpu_id >= 0:
            pred = cuda.to_cpu(pred)

        if lang == 'en':
            for i in np.argsort(pred)[0][-1::-1][:num]:
                print(self.synsets[i], pred[0][i])
        else:
            for i in np.argsort(pred)[0][-1::-1][:num]:
                print(self.synsets_jp[i], pred[0][i])

    def get_words(self, img, num, lang='en', sim='high'):
        words = []
        img_arr = self.img_proc.load_img(img)

        if self.gpu_id >= 0:
            cuda.get_device(args.gpu).use()
            self.model.to_gpu()
            img_arr = cuda.to_gpu(img_arr, device=args.gpu)

        with chainer.using_config('train', False):
            pred = self.model(img_arr, None).data
        
        if self.gpu_id >= 0:
            pred = cuda.to_cpu(pred)

        if lang == 'en':
            for i in np.argsort(pred)[0][-1::-1][:num]:
                sim_word = self.synsets[i][10:].split(',')[0]
                words.append(sim_word)
        elif lang == 'jp':
            for i in np.argsort(pred)[0][-1::-1][:num]:
                sim_pair = self.synsets_jp[i].split()
                sim_words = sim_pair[1:]
                words.append(sim_words)

        return words

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--img', '-i', type=str, default=os.path.join('..', '..', 'sample_imgs', 'test.jpg'),
                        help="image you want to predict")
    parser.add_argument('--gpu', '-g', type=int, default=0,
                        help="GPU ID(put -1 if you don't use gpu)")
    args = parser.parse_args()

    img_model = img_sim(model='ResNet', gpu_id=args.gpu)
    #img_model.similarity(args.img, 5)
    #img_model.similarity(args.img, 5, lang='jp')
    results1 = img_model.get_words(args.img, 5)
    results2 = img_model.get_words(args.img, 5, lang='jp')

    #print(results1)
    print(results2)
