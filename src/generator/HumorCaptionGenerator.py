import os
import sys
import argparse
import random

from get_subject import get_subject

sys.path.append('..')
from img_sim.img_predict import img_sim
from word_sim.word_predict import word_sim
from image_caption.CaptionGenerator import CaptionGenerator

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
