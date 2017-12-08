import os
import sys
import argparse
import random
import random
import numpy as np
import pandas as pd
from janome.tokenizer import Tokenizer

sys.path.append('../../src/calc_sims/img_sim')
sys.path.append('../../src/calc_sims/word_sim')
sys.path.append('../../src/image_caption')
sys.path.append('../../src/generator')
sys.path.append('../../src/')

from generator.HumorCaptionGenerator import HumorCaptionGenerator

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--img_dir', '-i', type=str, default=os.path.join('..', 'static', 'images', 'test2015'),
                        help="input image")
    parser.add_argument('--output_csv_dir', type=str, default=os.path.join('..', 'static', 'data'))
    parser.add_argument('--experiment1', type=str, default='experiment1.csv')
    parser.add_argument('--experiment2', type=str, default='experiment2.csv')
    parser.add_argument('--experiment3', type=str, default='experiment3.csv')
    parser.add_argument('--cnn_model_path', type=str, default=os.path.join('..', '..', 'data', 'models', 'cnn', 'ResNet50.model'),
                        help="CNN model path")
    parser.add_argument('--cnn_model_type', type=str, default='ResNet', choices=['ResNet', 'VGG16', 'AlexNet'],
                        help="CNN model type")
    parser.add_argument('--rnn_model_path', type=str, default=os.path.join('..', '..', 'data', 'models', 'rnn', 'STAIR_jp_256_Adam.model'),
                        help="RNN model path")
    parser.add_argument('--word2vec_model_path', type=str, default=os.path.join('..', '..', 'data', 'word2vec', 'models', 'ja_wikipedia_neolog.model'),
                        help="Word2vec model path")
    parser.add_argument('--nic_dict_path', type=str, default=os.path.join('..', '..', 'data', 'nic_dict', 'dict_STAIR_jp_train.pkl'),
                        help="Neural image caption dictionary path")
    parser.add_argument('--class_table_path', type=str, default=os.path.join('..', '..', 'data', 'wordnet', 'resnet_synsets_jp.txt'),
                        help="class table path")
    parser.add_argument('--beamsize', '-b', type=int, default=1,
                        help="beamsize of neural image caption")
    parser.add_argument('--depth_limit', '-dl', type=int, default=50, 
                        help="max limit of generating tokens when constructing captions")
    parser.add_argument('--first_word', type=str, default='<S>',
                        help="first word")
    parser.add_argument('--hidden_dim', type=int, default=512,
                        help="dimension of hidden layers")
    parser.add_argument('--mean', type=str, default="imagenet",
                        help="method to preprocess images")
    parser.add_argument('--no_feature', '-f', action='store_false',
                        help="don't use image features to calc img sim class")
    parser.add_argument('--img_multiply', '-mt', type=int, default=5,
                        help="multiply by num size of image classes is generated")
    parser.add_argument('--output_size', type=int, default=5,
                        help="output size")
    parser.add_argument('--cutoff', '-c',type=int, default=1,
                        help="the number of ignoring top n img sim word")
    parser.add_argument('--colloquial', '-co', action='store_true',
                        help="return captions as colloquial")
    parser.add_argument('--gpu', '-g', type=int, default=-1,
                        help="GPU ID (put -1 if you don't use gpu)")
    
    args = parser.parse_args()

    model = HumorCaptionGenerator(
                            rnn_model_path=args.rnn_model_path,
                            cnn_model_path=args.cnn_model_path,
                            word2vec_model_path=args.word2vec_model_path,
                            nic_dict_path=args.nic_dict_path,
                            class_table_path=args.class_table_path,
                            cnn_model_type=args.cnn_model_type,
                            beamsize=args.beamsize,
                            depth_limit=args.depth_limit,
                            first_word=args.first_word,
                            hidden_dim=args.hidden_dim,
                            mean=args.mean,
                            feature=args.no_feature,
                            gpu_id=args.gpu
                        )

    
    images = os.listdir(args.img_dir)

    #experiment1
    experiment1_path = os.path.join(args.output_csv_dir, args.experiment1)
    experiment1_header = 'no, images, captions, humor_captions' + '\n'
    experiment1_body = ''

    with open(experiment1_path, 'w') as f:
        pass

    
    for image in enumerate(images):
        img_path = os.path.join(args.img_dir, image)

        result = model.generate(
                            img = img_path,
                            multiple = args.img_multiply,
                            num = args.output_size,
                            cutoff = args.cutoff,
                            img_sim = 'high',
                            word_sim = 'low',
                            colloquial = True
                        )

"""

    humor_captions = model.generate(
                            img=args.img,
                            multiple=args.img_multiply,
                            num=args.output_size,
                            cutoff=args.cutoff,
                            img_sim=args.img_sim,
                            word_sim=args.word_sim,
                            colloquial=args.colloquial)
    

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

"""
