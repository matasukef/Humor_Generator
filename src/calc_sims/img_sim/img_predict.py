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

    def __check_duplicate(self, norms, known_norms):
        DUPLICATE = True
        for norm in norms:
            if norm in known_norms:
                DUPLICATE = False
                break

        return DUPLICATE

    def __get_sim_words(self, pred, start_idx, num, cutoff=0, dsc=True):
        sim_words = []
        known_words = []
        
        if dsc:
            sorted_pred_index = np.argsort(pred)[::-1]
        else:
            sorted_pred_index = np.argsort(pred)

        for i in sorted_pred_index[start_idx:]:
            if len(sim_words) < num + cutoff:
                norms = self.synsets[i].split(' ', 1)[1].split(',')

                if self.__check_duplicate(norms, known_words):
                    # add norms to known_words to avoid appending known sim words to sim_words
                    for norm in norms:
                        known_words.append(norm)

                    sim_words.append( {'norm': norms, 'sim': round(float(pred[i]), 10)} )
            else:
                break

        return sim_words[cutoff:]

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
        #cutoff parameter is only available when sim_type is high or low

        pred = self.__calc_pred(img)

        if sim_type == 'high':
            sim_words = self.__get_sim_words(pred, 0, num, cutoff=cutoff, dsc=True)

        elif sim_type == 'med':
            med_index = self.__getMedianIndex(pred)
            half_num, even = divmod(num, 2) 
            start_idx = med_index - half_num

            sim_words = self.__get_sim_words(pred, start_idx, num, cutoff=0, dsc=True)

        elif sim_type == 'mid':
            half_num, even = divmod(num, 2)
            start_idx = int(len(pred) / 2) - half_num
            
            sim_words = self.__get_sim_words(pred, start_idx, num, cutoff=0, dsc=True)
            
        elif sim_type == 'low':
            sim_words = self.__get_sim_words(pred, 0, num, cutoff=cutoff, dsc=False)
            
        elif sim_type == 'rand':
            sim_words = []

            sorted_pred_index = np.argsort(pred)
            
            for i in np.random.choice(sorted_pred_index, num):
                norms = self.synsets[i].split(' ', 1)[1].split(',')
                sim_words.append( {'norm': norms, 'sim': round(float(pred[i]), 10)} )
        
        return sim_words

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--img', '-i', type=str, default=os.path.join('..', '..', '..', 'sample_imgs', 'test.jpg'),
                        help="image you want to predict")
    parser.add_argument('--gpu', '-g', type=int, default=-1,
                        help="GPU ID(put -1 if you don't use gpu)")
    parser.add_argument('--class_table_path', type=str, default=os.path.join('..', '..', '..', 'data', 'wordnet', 'resnet_synsets_jp_modified.txt'),
                        help="class table path to output probability of image classification")
    parser.add_argument('--cnn_model_path', type=str, default=os.path.join('..', '..', '..', 'data', 'models', 'cnn', 'ResNet50.model'),
                        help="CNN model path")
    parser.add_argument('--cnn_model_type', type=str, default='ResNet', choices=['ResNet', 'VGG16', 'AlexNet'],
                        help="model type")
    parser.add_argument('--mean', type=str, default='imagenet',
                        help="method to preprocess images")
    parser.add_argument('--num', '-n', type=int, default=5, 
                        help="the number of output")
    parser.add_argument('--sim', type=str, default='high', choices=['high', 'low', 'mid', 'rand', 'med'],
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

    for sim_word in sim_words:
        print(sim_word['sim'], sim_word['norm'])
