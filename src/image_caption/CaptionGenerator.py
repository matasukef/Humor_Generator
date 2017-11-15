import os
import sys
import numpy as np
import pickle
import argparse
from copy import deepcopy
import chainer
from chainer import cuda
import chainer.functions as F
from chainer import cuda
from chainer import serializers

sys.path.append('..')
from img_proc import Img_proc
from Image2CaptionDecoder import Image2CaptionDecoder

sys.path.append('../CNN')

import heapq

class CaptionGenerator(object):
    def __init__(self, lang='jp', cnn_model_type="ResNet", beamsize=3, depth_limit=50, gpu_id=-1):
        self.gpu_id = gpu_id
        self.beamsize = beamsize
        self.depth_limit = depth_limit
        self.img_proc = Img_proc(mean_type='imagenet')
        self.first_word = '<S>'

        if cnn_model_type == 'ResNet':
            from CNN.ResNet50 import ResNet
            from ENV import MODEL_RESNET
            
            self.cnn_model = ResNet()
            serializers.load_hdf5(MODEL_RESNET, self.cnn_model)
        
        elif cnn_model_type == 'VGG16':
            from CNN.VGG16 import VGG16
            from ENV import MODEL_VGG16
            
            self.cnn_model = VGG16()
            serializers.load_hdf5(MODEL_VGG16, self.cnn_model)
       
        elif cnn_model_type == 'AlexNet':
            from CNN.AlexNet import AlexNet
            from ENV import MODEL_ALEXNET
            
            self.cnn_model = AlexNet()
            serializers.load_hdf5(MODEL_ALEXNET, self.cnn_model)

       
        if lang == 'jp':
            from ENV import CAP_VOCAB_JP, CAP_RNN_MODEL_JP
            
            self.index2token = self.parse_dic(CAP_VOCAB_JP)
            self.CAP_RNN_MODEL = CAP_RNN_MODEL_JP
        
        elif lang == 'en':
            from ENV import CAP_VOCAB_EN, CAP_RNN_MODEL_EN
            
            self.index2token = self.parse_dic(CAP_VOCAB_EN)
            self.CAP_RNN_MODEL = CAP_RNN_MODEL_EN
        
        elif lang == 'ch':
            from ENV import CAP_VOCAB_CH, CAP_RNN_MODEL_CH
            
            self.index2token = self.parse_dic(CAP_VOCAB_CH)
            self.CAP_RNN_MODEL = CAP_RNN_MODEL_CH

        self.rnn_model = Image2CaptionDecoder(len(self.token2index), hidden_dim=512)
        serializers.load_hdf5(self.CAP_RNN_MODEL, self.rnn_model)
        
        #Gpu configuration
        global xp
        if self.gpu_id >= 0:
            xp = cuda.cupy
            cuda.get_device(gpu_id).use()
            self.cnn_model.to_gpu()
            self.rnn_model.to_gpu()
        else:
            xp=np

    def parse_dic(self, dict_path):
        with open(dict_path, 'rb') as f:
            self.token2index = pickle.load(f)

        return { v:k for k, v in self.token2index.items() }

    def successor(self, current_state):
        word=[xp.array([current_state["token"][-1]], dtype=xp.int32)]
        hx = current_state['hidden']
        cx = current_state['cell']
    
        #predict next word
        with chainer.using_config('train', False):
            hy, cy, next_words = self.rnn_model(hx, cx, word)
        
        word_dist = F.softmax(next_words[0]).data[0]
        k_best_next_sentences = []
        for i in range(self.beamsize):
            next_word_idx = int(xp.argmax(word_dist))
            k_best_next_sentences.append(
                    {
                        "hidden": hy,
                        "cell": cy,
                        "token": deepcopy(current_state['token']) + [next_word_idx],
                        "cost": current_state['cost'] - xp.log(word_dist[next_word_idx])
                    }
                )
            word_dist[next_word_idx] = 0

        return hy, cy, k_best_next_sentences

    def beam_search(self, init_state):
        
        found_tokens = []
        top_k_states = [init_state]
        while (len(found_tokens) < self.beamsize):
            new_top_k_states = []
            for state in top_k_states:
                hy, cy, k_best_next_states = self.successor(state)
                for next_state in k_best_next_states:
                    new_top_k_states.append(next_state)
            selected_top_k_states=heapq.nsmallest(self.beamsize, new_top_k_states, key=lambda x: x['cost'])

            top_k_states=[]
            for state in selected_top_k_states:
                if state['token'][-1] == self.token2index['</S>'] or len(state['token']) == self.depth_limit:
                    found_tokens.append(state)
                else:
                    top_k_states.append(state)

        return sorted(found_tokens, key=lambda x: x['cost'])

    def generate_from_img_feature(self, img_feature):
        if self.gpu_id >= 0:
            img_feature = cuda.to_gpu(img_feature)

        batch_size = 1
        hx = xp.zeros((self.rnn_model.n_layers, batch_size, self.rnn_model.hidden_dim), dtype=xp.float32)
        cx = xp.zeros((self.rnn_model.n_layers, batch_size, self.rnn_model.hidden_dim), dtype=xp.float32)
        
        with chainer.using_config('train', False):
            hy, cy = self.rnn_model.input_cnn_feature(hx, cx, img_feature)

        init_state = {
                "hidden": hy,
                "cell": cy,
                "token": [self.token2index[self.first_word]],
                "cost": 0,
                }

        captions = self.beam_search(init_state)

        caption_candidates = []
        for caption in captions:
            sentence = [self.index2token[word_index] for word_index in caption['token']]
            log_likelihood = -float(caption['cost']) #negative log likelihood
            caption_candidates.append({'sentence': sentence, 'log_likelihood': log_likelihood})

        return caption_candidates

    def generate_from_img(self, img_array):
        if self.gpu_id >= 0:
            img_array = cuda.to_gpu(img_array)
        with chainer.using_config('train', False):
            img_feature = self.cnn_model(img_array, 'feature').data.reshape(1, 1, 2048)

        return self.generate_from_img_feature(img_feature)
    
    def generate(self, img_path):
        img = self.img_proc.load_img(img_path)
        return self.generate_from_img(img)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', '-rm', type=str, default='jp',
                        help="RNN model path")
    parser.add_argument('--cnn_model_type', '-ct', type=str, choices=['ResNet', 'VGG16', 'AlexNet'], default="ResNet",
                        help="CNN model type")
    parser.add_argument('--beamsize', '-b', type=int, default=3,
                        help="beamsize")
    parser.add_argument('--depth_limit', '-dl', type=int, default=50,
                        help="max limit of generating tokens when constructing captions")
    parser.add_argument('--gpu', '-g', type=int, default=0, 
                        help="set GPU ID(negative value means using CPU)")
    parser.add_argument('--img', '-i', type=str, default=os.path.join('..', '..', 'sample_imgs', 'test.jpg'),
                        help="path to test image (default is set as sample_img1.jpg)")
    args = parser.parse_args()
    
    
    caption_generator = CaptionGenerator(
            lang = args.lang,
            cnn_model_type=args.cnn_model_type,
            beamsize = args.beamsize,
            depth_limit = args.depth_limit,
            gpu_id = args.gpu,
        )

    captions = caption_generator.generate(args.img)
    for i, caption in enumerate(captions):
        print('caption{0}: {1}'.format(i, caption['sentence']))
        print('log: ', caption['log_likelihood'])
