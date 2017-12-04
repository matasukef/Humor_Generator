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
                'model',
                'synsets',
                'feature',
                'gpu_id',
                'cnn_model_path',
                'cnn_model_type',
                'class_table_path',
                'mean'
            ]

    def __init__(
            self, 
            cnn_model_path,
            class_table_path,
            cnn_model_type='ResNet',
            mean='imagenet',
            feature=False,
            gpu_id=-1
        ):

        self.cnn_model_path = cnn_model_path
        self.cnn_model_type = cnn_model_type
        self.class_table_path = class_table_path
        self.mean = mean
        self.feature = feature
        self.gpu_id = gpu_id
        
        self.img_proc = Img_proc(mean)
        
        if cnn_model_type == 'ResNet':
            from CNN.ResNet50 import ResNet
            self.model = ResNet()
        elif cnn_model_type == 'VGG16':
            from CNN.VGG16 import VGG16
            self.model = VGG16()
        elif cnn_model_type == 'AlexNet':
            from CNN.AlexNet import AlexNet
            self.model = AlexNet()
        
        serializers.load_hdf5(cnn_model_path, self.model)


        with open(class_table_path, 'r') as f:
            self.synsets = f.read().split('\n')[:-1]
        

    def __getMedianIndex(self, pred_list):
        #get nearest value with num in list
        
        med_value = np.median(pred_list)
        min_idx = np.abs(np.asarray(pred_list) - med_value).argmin()
        
        return min_idx

    def __calc_pred(self, img):
        if self.feature:
            
            if self.gpu_id >= 0:
                cuda.get_device(self.gpu_id).use()
                self.model.to_gpu()
                img = cuda.to_gpu(img, device=self.gpu_id)

            with chainer.using_config('train', False):
                pred = self.model.pred_from_feature(img).data
            
            if self.gpu_id >= 0:
                pred = cuda.to_cpu(pred)
        
        else:
            img_arr = self.img_proc.load_img(img)

            if self.gpu_id >= 0:
                cuda.get_device(args.gpu).use()
                self.model.to_gpu()
                img_arr = cuda.to_gpu(img_arr, device=args.gpu)

            with chainer.using_config('train', False):
                pred = self.model(img_arr, None).data

            if self.gpu_id >= 0:
                pred = cuda.to_cpu(pred)
            
        return pred[0]

    def get_norms(self, img, num=5, cutoff=0, sim_type='high'):
        sim_words = []

        pred = self.__calc_pred(img)

        #sorted pred index
        sorted_pred_index = np.argsort(pred)[::-1]
        
        if sim_type == 'high':
            for i in sorted_pred_index[cutoff : num+cutoff]:
                norm = self.synsets[i].split(' ', 1)[1].split(',')
                sim_words.append( {'norm': norm, 'sim': round(float(pred[i]), 10)} )
        
        elif sim_type == 'mid':
            med_index = self.__getMedianIndex(pred)
            half_num, even = divmod(num, 2) 
            start_idx = med_index - half_num + cutoff
            end_idx = med_index + half_num + even + cutoff

            for i in sorted_pred_index[start_idx : end_idx]:
                norm = self.synsets[i].split(' ', 1)[1].split(',')
                sim_words.append( {'norm': norm, 'sim': round(float(pred[i]), 10)} )
       
        elif sim_type == 'low':
            start_idx = -num - cutoff
            end_idx = -cutoff if cutoff != 0 else len(pred)
            for i in sorted_pred_index[start_idx : end_idx][::-1]:
                norm = self.synsets[i].split(' ', 1)[1].split(',')
                sim_words.append( {'norm': norm, 'sim': round(float(pred[i]), 10)} )
        
        elif sim_type == 'rand':
            for i in np.random.choice(sorted_pred_index, num):
                norm = self.synsets[i].split(' ', 1)[1].split(',')
                sim_words.append( {'norm': norm, 'sim': round(float(pred[i]), 10)} )
        
        return sim_words

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--img', '-i', type=str, default=os.path.join('..', '..', '..', 'sample_imgs', 'test.jpg'),
                        help="image you want to predict")
    parser.add_argument('--gpu', '-g', type=int, default=-1,
                        help="GPU ID(put -1 if you don't use gpu)")
    parser.add_argument('--class_table_path', type=str, default=os.path.join('..', '..', '..', 'data', 'wordnet', 'resnet_synsets_jp.txt'),
                        help="class table path to output probability of image classification")
    parser.add_argument('--cnn_model_path', type=str, default=os.path.join('..', '..', '..', 'data', 'models', 'cnn', 'ResNet50.model'),
                        help="CNN model path")
    parser.add_argument('--cnn_model_type', type=str, default='ResNet', choices=['ResNet', 'VGG16', 'AlexNet'],
                        help="model type")
    parser.add_argument('--mean', type=str, default='imagenet',
                        help="method to preprocess images")
    parser.add_argument('--num', '-n', type=int, default=5, 
                        help="the number of output")
    parser.add_argument('--sim', type=str, default='high', choices=['high', 'low', 'mid', 'rand'],
                        help="output sim type")
    parser.add_argument('--cutoff', '-c', type=int, default=0, 
                        help="the number of ignoring top n similar class.\
                                This option is valid only when sim is high.")
    parser.add_argument('--feature', '-f', action='store_true',
                        help="use features to output class")
    args = parser.parse_args()

    img_model = img_sim(
                cnn_model_path=args.cnn_model_path,
                cnn_model_type=args.cnn_model_type, 
                class_table_path=args.class_table_path,
                gpu_id=args.gpu, 
                mean=args.mean,
                feature=args.feature
            )

    sim_words = img_model.get_norms(args.img, num=args.num, cutoff=args.cutoff, sim_type=args.sim)

    print(sim_words)
    for sim_word in sim_words:
        print(sim_word['sim'], sim_word['norm'])
