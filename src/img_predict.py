import sys
import os
import argparse
import numpy as np
import chainer
import chainer.functions as F
from chainer import cuda
from chainer import serializers
from img_proc import Img_proc
from ENV import (
        MODEL_RESNET,
        MODEL_VGG16,
        MODEL_ALEXNET,
        VOCAB_RESNET,
        VOCAB_VGG16,
        VOCAB_ALEXNET
        )
    

class img_sim(object):
    def __init__(self, model='ResNet', gpu_id=-1):
        self.img_proc = Img_proc("imagenet")
        if model == "ResNet":
            from CNN.ResNet50 import ResNet
            self.model = ResNet()
            serializers.load_hdf5(MODEL_RESNET, self.model)
        elif model == 'VGG16':
            from CNN.VGG16 import VGG16
            self.model = VGG16()
            serializers.load_hdf5(MODEL_VGG16, self.model)
        elif model == 'AlexNet':
            from CNN.AlexNet import AlexNet
            self.model == AlexNet()
            serializers.load_hdf5(MODEL_ALEXNET, self.model)
        
        self.gpu_id = gpu_id
        
        with open(VOCAB_RESNET, 'r') as f:
            self.synsets = f.read().split('\n')[:-1]

    def similarity(self, img, num=5):
        img_arr = self.img_proc.load_img(img)

        if self.gpu_id >= 0:
            cuda.get_device(args.gpu).use()
            self.model.to_gpu()
            img_arr = cuda.to_gpu(img_arr, device=args.gpu)

        with chainer.using_config('train', False):
            pred = self.model(img_arr, None).data
        
        if self.gpu_id >= 0:
            pred = cuda.to_cpu(pred)

        for i in np.argsort(pred)[0][-1::-1][:num]:
            print(self.synsets[i], pred[0][i])

    def get_words(self, img, num):
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

        for i in np.argsort(pred)[0][-1::-1][:num]:
            sim_word = self.synsets[i][10:].split(',')[0]
            words.append(sim_word)

        return words

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--img', '-i', type=str, default=os.path.join('..', 'sample_imgs', 'test.jpg'),
                        help="image you want to predict")
    parser.add_argument('--gpu', '-g', type=int, default=-1,
                        help="GPU ID(put -1 if you don't use gpu)")
    args = parser.parse_args()

    img_model = img_sim(model='ResNet', gpu_id=args.gpu)
    img_model.similarity(args.img, 5)
    results = img_model.get_words(args.img, 5)

    print(results)
